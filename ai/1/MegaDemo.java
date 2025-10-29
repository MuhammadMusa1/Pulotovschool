import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Function;

/**
 * MegaDemo — один большой, но автономный Java-файл, который демонстрирует:
 *  - Мини HTTP-сервер (стандартный HttpServer) с несколькими маршрутами
 *  - LRU Cache (на LinkedHashMap)
 *  - EventBus (публикация/подписка)
 *  - Планировщик задач (ScheduledExecutorService)
 *  - Простейший потоковый ThreadPool (ExecutorService) и таймеры
 *  - InMemory "ORM"-репозиторий с авто-ID
 *  - Алгоритмы: Быстрая сортировка, Дейкстра
 *  - Небольшой утилитный JSON-Builder
 *
 * Запуск:
 *   javac MegaDemo.java && java MegaDemo
 * После запуска:
 *   - HTTP: открой http://localhost:8080/hello
 *   - HTTP: открой http://localhost:8080/dijkstra?edges=0-1:4,0-2:1,2-1:2,1-3:1,2-3:5&start=0
 *   - HTTP: открой http://localhost:8080/quicksort?arr=5,4,3,2,1,9
 */
public class MegaDemo {

    // ===================== LRU Cache =====================
    public static class LRUCache<K, V> extends LinkedHashMap<K, V> {
        private final int capacity;
        public LRUCache(int capacity) {
            super(capacity, 0.75f, true);
            this.capacity = capacity;
        }
        @Override
        protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() > capacity;
        }
    }

    // ===================== EventBus =====================
    public static class EventBus {
        private final Map<Class<?>, List<Listener<?>>> listeners = new ConcurrentHashMap<>();

        public <T> void subscribe(Class<T> eventType, Listener<T> listener) {
            listeners.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>()).add(listener);
        }
        public <T> void publish(T event) {
            var subs = listeners.getOrDefault(event.getClass(), List.of());
            for (Listener<?> l : subs) {
                @SuppressWarnings("unchecked")
                Listener<T> casted = (Listener<T>) l;
                casted.on(event);
            }
        }
        public interface Listener<T> { void on(T event); }
    }

    // ===================== InMemory Repository =====================
    public interface Identifiable { long id(); }

    public static class AutoId implements Identifiable {
        private static final AtomicLong SEQ = new AtomicLong(1);
        private final long id = SEQ.getAndIncrement();
        public long id() { return id; }
    }

    public static class User extends AutoId {
        final String name;
        final int age;
        public User(String name, int age) { this.name = name; this.age = age; }
        @Override public String toString() { return "User{" + id() + ", '" + name + "', age=" + age + "}"; }
    }

    public static class InMemoryRepo<T extends Identifiable> {
        private final ConcurrentMap<Long, T> store = new ConcurrentHashMap<>();
        public T save(T entity) { store.put(entity.id(), entity); return entity; }
        public Optional<T> findById(long id) { return Optional.ofNullable(store.get(id)); }
        public List<T> findAll() { return new ArrayList<>(store.values()); }
        public boolean deleteById(long id) { return store.remove(id) != null; }
        public int size() { return store.size(); }
    }

    // ===================== Algorithms =====================
    public static class Algorithms {
        // QuickSort in-place
        public static void quickSort(int[] arr) { quickSort(arr, 0, arr.length - 1); }
        private static void quickSort(int[] a, int l, int r) {
            if (l >= r) return;
            int i = l, j = r;
            int pivot = a[(l + r) >>> 1];
            while (i <= j) {
                while (a[i] < pivot) i++;
                while (a[j] > pivot) j--;
                if (i <= j) {
                    int t = a[i]; a[i] = a[j]; a[j] = t; i++; j--; }
            }
            if (l < j) quickSort(a, l, j);
            if (i < r) quickSort(a, i, r);
        }

        // Dijkstra on adjacency list (0..n-1)
        public static int[] dijkstra(int n, List<List<Edge>> g, int start) {
            int[] dist = new int[n];
            Arrays.fill(dist, Integer.MAX_VALUE/4);
            dist[start] = 0;
            PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
            pq.add(new int[]{start, 0});
            boolean[] used = new boolean[n];
            while (!pq.isEmpty()) {
                int[] cur = pq.poll();
                int v = cur[0];
                if (used[v]) continue;
                used[v] = true;
                for (Edge e : g.get(v)) {
                    if (dist[v] + e.w < dist[e.to]) {
                        dist[e.to] = dist[v] + e.w;
                        pq.add(new int[]{e.to, dist[e.to]});
                    }
                }
            }
            return dist;
        }
        public record Edge(int to, int w) { }
    }

    // ===================== JSON Builder (простенький) =====================
    public static class Json {
        public static String obj(Map<String, ?> map) {
            var sb = new StringBuilder();
            sb.append('{');
            boolean first = true;
            for (var e : map.entrySet()) {
                if (!first) sb.append(',');
                first = false;
                sb.append('"').append(escape(e.getKey())).append('"').append(':').append(val(e.getValue()));
            }
            sb.append('}');
            return sb.toString();
        }
        public static String arr(Collection<?> col) {
            var sb = new StringBuilder();
            sb.append('[');
            boolean first = true;
            for (var v : col) {
                if (!first) sb.append(',');
                first = false;
                sb.append(val(v));
            }
            sb.append(']');
            return sb.toString();
        }
        private static String val(Object v) {
            if (v == null) return "null";
            if (v instanceof Number || v instanceof Boolean) return v.toString();
            if (v instanceof int[]) return arr(Arrays.stream((int[]) v).boxed().toList());
            if (v instanceof Collection<?>) return arr((Collection<?>) v);
            if (v instanceof Map<?,?> m) return obj((Map<String, ?>) m);
            return '"' + escape(v.toString()) + '"';
        }
        private static String escape(String s) {
            return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
        }
    }

    // ===================== Mini HTTP Server =====================
    public static class MiniHttp {
        private HttpServer server;
        public void start(int port) throws IOException {
            server = HttpServer.create(new InetSocketAddress(port), 0);
            server.createContext("/hello", exchange -> ok(exchange, Json.obj(Map.of(
                    "ok", true,
                    "message", "Hi from MegaDemo",
                    "time", Instant.now().toString()
            ))));

            server.createContext("/quicksort", new QuickSortHandler());
            server.createContext("/dijkstra", new DijkstraHandler());

            server.setExecutor(Executors.newCachedThreadPool());
            server.start();
            System.out.println("HTTP server started on http://localhost:" + port);
        }
        public void stop() { if (server != null) server.stop(0); }

        private static void ok(HttpExchange ex, String body) throws IOException {
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            ex.getResponseHeaders().add("Content-Type", "application/json; charset=utf-8");
            ex.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = ex.getResponseBody()) { os.write(bytes); }
        }

        static Map<String, List<String>> queryParams(URI uri) {
            Map<String, List<String>> res = new HashMap<>();
            String q = uri.getRawQuery();
            if (q == null || q.isEmpty()) return res;
            for (String pair : q.split("&")) {
                String[] kv = pair.split("=", 2);
                String k = decode(kv[0]);
                String v = kv.length > 1 ? decode(kv[1]) : "";
                res.computeIfAbsent(k, kk -> new ArrayList<>()).add(v);
            }
            return res;
        }
        static String decode(String s) { return java.net.URLDecoder.decode(s, StandardCharsets.UTF_8); }

        static class QuickSortHandler implements HttpHandler {
            @Override public void handle(HttpExchange ex) throws IOException {
                var params = queryParams(ex.getRequestURI());
                var arrStr = params.getOrDefault("arr", List.of("5,2,9,1,5,6")).get(0);
                int[] arr = Arrays.stream(arrStr.split(",")).filter(p -> !p.isBlank()).mapToInt(Integer::parseInt).toArray();
                Algorithms.quickSort(arr);
                ok(ex, Json.obj(Map.of(
                        "input", arrStr,
                        "sorted", Arrays.toString(arr)
                )));
            }
        }

        static class DijkstraHandler implements HttpHandler {
            @Override public void handle(HttpExchange ex) throws IOException {
                var p = queryParams(ex.getRequestURI());
                String edges = p.getOrDefault("edges", List.of("0-1:4,0-2:1,2-1:2,1-3:1,2-3:5")).get(0);
                int start = Integer.parseInt(p.getOrDefault("start", List.of("0")).get(0));
                // parse edges like "0-1:4,0-2:1" => undirected? сделаем directed
                int maxNode = 0;
                List<int[]> e = new ArrayList<>();
                for (String part : edges.split(",")) {
                    if (part.isBlank()) continue;
                    String[] a = part.split(":");
                    String[] uv = a[0].split("-");
                    int u = Integer.parseInt(uv[0]);
                    int v = Integer.parseInt(uv[1]);
                    int w = Integer.parseInt(a[1]);
                    e.add(new int[]{u, v, w});
                    maxNode = Math.max(maxNode, Math.max(u, v));
                }
                int n = maxNode + 1;
                List<List<Algorithms.Edge>> g = new ArrayList<>();
                for (int i = 0; i < n; i++) g.add(new ArrayList<>());
                for (int[] ee : e) g.get(ee[0]).add(new Algorithms.Edge(ee[1], ee[2]));
                int[] dist = Algorithms.dijkstra(n, g, start);
                ok(ex, Json.obj(Map.of(
                        "n", n,
                        "start", start,
                        "edges", edges,
                        "dist", Arrays.toString(dist)
                )));
            }
        }
    }

    // ===================== Schedulers & ThreadPool =====================
    public static class Async {
        private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
        private final ExecutorService workers = Executors.newFixedThreadPool(Math.max(2, Runtime.getRuntime().availableProcessors() - 1));

        public ScheduledFuture<?> every(Duration period, Runnable task) {
            return scheduler.scheduleAtFixedRate(task, 0, period.toMillis(), TimeUnit.MILLISECONDS);
        }
        public <T> Future<T> submit(Callable<T> c) { return workers.submit(c); }
        public void shutdown() { scheduler.shutdownNow(); workers.shutdownNow(); }
    }

    // ===================== Showcase / Demo =====================
    public static void main(String[] args) throws Exception {
        System.out.println("MegaDemo starting…\n");

        // 1) Репозиторий и пользователи
        InMemoryRepo<User> users = new InMemoryRepo<>();
        users.save(new User("Alice", 30));
        users.save(new User("Bob", 25));
        users.save(new User("Carol", 42));
        System.out.println("Users: " + users.findAll());

        // 2) LRU Cache
        LRUCache<String, String> cache = new LRUCache<>(3);
        cache.put("A", "Alpha"); cache.put("B", "Beta"); cache.put("C", "Gamma");
        cache.get("A"); // A становится самым новым
        cache.put("D", "Delta"); // вытеснит B
        System.out.println("LRU keys: " + cache.keySet()); // ожидаем [C, A, D]

        // 3) EventBus
        EventBus bus = new EventBus();
        bus.subscribe(String.class, s -> System.out.println("[Listener1] " + s));
        bus.subscribe(String.class, s -> System.out.println("[Listener2] len=" + s.length()));
        bus.publish("Hello EventBus!");

        // 4) Async планировщик и воркеры
        Async async = new Async();
        ScheduledFuture<?> ticker = async.every(Duration.ofSeconds(2), new Runnable() {
            int t = 0; final Instant started = Instant.now();
            @Override public void run() {
                t++;
                System.out.println("[TICK] t=" + t + " at " + Duration.between(started, Instant.now()).toSeconds() + "s");
                if (t >= 3) throw new RuntimeException("stop ticks");
            }
        });
        try { Thread.sleep(6500); } catch (InterruptedException ignored) {}
        ticker.cancel(true);

        Future<String> f = async.submit(() -> {
            Thread.sleep(500);
            return "Work result @" + Instant.now();
        });
        System.out.println("Async worker result: " + f.get());

        // 5) Алгоритмы
        int[] arr = {5, 2, 9, 1, 5, 6};
        Algorithms.quickSort(arr);
        System.out.println("QuickSort: " + Arrays.toString(arr));

        List<List<Algorithms.Edge>> g = new ArrayList<>();
        for (int i = 0; i < 4; i++) g.add(new ArrayList<>());
        g.get(0).add(new Algorithms.Edge(1, 4));
        g.get(0).add(new Algorithms.Edge(2, 1));
        g.get(2).add(new Algorithms.Edge(1, 2));
        g.get(1).add(new Algorithms.Edge(3, 1));
        g.get(2).add(new Algorithms.Edge(3, 5));
        int[] dist = Algorithms.dijkstra(4, g, 0);
        System.out.println("Dijkstra from 0: " + Arrays.toString(dist));

        // 6) HTTP сервер
        MiniHttp http = new MiniHttp();
        http.start(8080);

        // 7) Завершение по Ctrl+C
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("\nShutdown…");
            http.stop();
        }));

        // Держим main живым, чтобы сервер работал
        System.out.println("\nСервер запущен. Открой http://localhost:8080/hello");
        // Простейшая блокировка навсегда (пока не выключат процесс)
        new CountDownLatch(1).await();
    }
}

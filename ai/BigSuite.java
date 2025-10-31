import java.io.*;
import java.net.*;
import java.nio.*;
import java.nio.channels.*;
import java.nio.charset.Charset;
import java.nio.file.*;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * BigSuite — второй большой автономный файл на Java, демонстрирует:
 *   1) NIO чат-сервер (многопользовательский, один порт, неблокирующий)
 *   2) Мини-Хранилище CSV с транзакционным снапшотом
 *   3) Markdown→HTML конвертер (очень упрощённый)
 *   4) Простой планировщик Cron-подобных задач (минутная и секундная гранулярность)
 *   5) Вычислитель выражений (шунтирующий двор + RPN)
 *   6) Структуры данных: BloomFilter и Trie (автодополнение)
 *   7) Утилита ZIP (архивация/распаковка)
 *
 * Запуск:
 *   javac BigSuite.java && java BigSuite
 *
 * После запуска появится CLI-меню. Пункты можно пробовать в любом порядке.
 */
public class BigSuite {

    // ======================= 1) NIO чат-сервер =======================
    public static class NioChatServer implements Runnable {
        private final int port;
        private final AtomicBoolean running = new AtomicBoolean(false);
        private Selector selector;
        private ServerSocketChannel server;
        private final Map<SocketChannel, String> names = new HashMap<>();
        private final Charset UTF8 = Charset.forName("UTF-8");

        public NioChatServer(int port) { this.port = port; }

        public void startAsync() {
            if (running.compareAndSet(false, true)) {
                new Thread(this, "nio-chat").start();
            }
        }
        public void stop() { running.set(false); try { selector.wakeup(); } catch (Exception ignored) {} }

        @Override public void run() {
            try {
                selector = Selector.open();
                server = ServerSocketChannel.open();
                server.configureBlocking(false);
                server.bind(new InetSocketAddress(port));
                server.register(selector, SelectionKey.OP_ACCEPT);
                System.out.println("[Chat] Listening on :" + port);
                while (running.get()) {
                    selector.select();
                    Iterator<SelectionKey> it = selector.selectedKeys().iterator();
                    while (it.hasNext()) {
                        SelectionKey key = it.next(); it.remove();
                        if (!key.isValid()) continue;
                        if (key.isAcceptable()) accept();
                        else if (key.isReadable()) read(key);
                    }
                }
            } catch (IOException e) {
                if (running.get()) e.printStackTrace();
            } finally { closeQuietly(); }
        }
        private void accept() throws IOException {
            SocketChannel ch = server.accept();
            ch.configureBlocking(false);
            ch.register(selector, SelectionKey.OP_READ, ByteBuffer.allocate(4096));
            send(ch, "Welcome to NioChat!\nEnter your name: ");
        }
        private void read(SelectionKey key) throws IOException {
            SocketChannel ch = (SocketChannel) key.channel();
            ByteBuffer buf = (ByteBuffer) key.attachment();
            int n = ch.read(buf);
            if (n == -1) { disconnect(ch); return; }
            if (n == 0) return;
            buf.flip();
            String s = UTF8.decode(buf).toString();
            buf.clear();
            for (String line : s.split("\r?\n")) {
                if (line.isBlank()) continue;
                if (!names.containsKey(ch)) {
                    names.put(ch, line.trim());
                    broadcast("* " + names.get(ch) + " joined *\n", ch);
                    send(ch, "Hi, " + names.get(ch) + "! Type /quit to leave.\n");
                } else {
                    if ("/quit".equalsIgnoreCase(line.trim())) { disconnect(ch); return; }
                    String msg = "[" + names.get(ch) + "] " + line + "\n";
                    broadcast(msg, ch);
                }
            }
        }
        private void broadcast(String msg, SocketChannel except) {
            ByteBuffer out = UTF8.encode(msg);
            for (SocketChannel c : new ArrayList<>(names.keySet())) {
                if (c != except) try { c.write(out.asReadOnlyBuffer()); } catch (IOException e) { disconnect(c); }
            }
            System.out.print(msg);
        }
        private void send(SocketChannel ch, String msg) throws IOException { ch.write(UTF8.encode(msg)); }
        private void disconnect(SocketChannel ch) {
            String nm = names.remove(ch);
            try { ch.close(); } catch (IOException ignored) {}
            if (nm != null) broadcast("* " + nm + " left *\n", null);
        }
        private void closeQuietly() {
            try { for (SocketChannel c : new ArrayList<>(names.keySet())) c.close(); } catch (IOException ignored) {}
            try { if (server != null) server.close(); } catch (IOException ignored) {}
            try { if (selector != null) selector.close(); } catch (IOException ignored) {}
        }
    }

    // ======================= 2) CSV Store =======================
    public static class CsvStore implements Closeable {
        private final Path file;
        private final List<String> header;
        private final List<List<String>> rows = new ArrayList<>();
        public CsvStore(Path file, List<String> header) throws IOException {
            this.file = file; this.header = new ArrayList<>(header);
            if (Files.exists(file)) load(); else flush();
        }
        public synchronized void put(List<String> row) { rows.add(new ArrayList<>(row)); }
        public synchronized List<List<String>> all() { return new ArrayList<>(rows); }
        public synchronized void snapshot() throws IOException { flush(); }
        private void load() throws IOException {
            try (BufferedReader br = Files.newBufferedReader(file)) {
                String first = br.readLine(); // header
                String line;
                while ((line = br.readLine()) != null) {
                    rows.add(parseCsvLine(line));
                }
            }
        }
        private void flush() throws IOException {
            Path tmp = file.resolveSibling(file.getFileName()+".tmp");
            try (BufferedWriter bw = Files.newBufferedWriter(tmp)) {
                bw.write(String.join(",", header)); bw.newLine();
                for (var r : rows) { bw.write(escapeCsv(r)); bw.newLine(); }
            }
            Files.move(tmp, file, StandardCopyOption.REPLACE_EXISTING, StandardCopyOption.ATOMIC_MOVE);
        }
        private static String escape(String s) { return s.replace("\"", "\"\""); }
        private static String escapeCsv(List<String> r) {
            List<String> out = new ArrayList<>();
            for (String v : r) {
                if (v.contains(",") || v.contains("\"") || v.contains("\n")) out.add("\"" + escape(v) + "\"");
                else out.add(v);
            }
            return String.join(",", out);
        }
        private static List<String> parseCsvLine(String line) {
            List<String> res = new ArrayList<>();
            StringBuilder cur = new StringBuilder();
            boolean quoted = false;
            for (int i=0;i<line.length();i++) {
                char c = line.charAt(i);
                if (quoted) {
                    if (c == '"') {
                        if (i+1 < line.length() && line.charAt(i+1) == '"') { cur.append('"'); i++; }
                        else quoted = false;
                    } else cur.append(c);
                } else {
                    if (c == '"') quoted = true;
                    else if (c == ',') { res.add(cur.toString()); cur.setLength(0); }
                    else cur.append(c);
                }
            }
            res.add(cur.toString());
            return res;
        }
        @Override public void close() throws IOException { snapshot(); }
    }

    // ======================= 3) Markdown → HTML =======================
    public static class Markdown {
        public static String toHtml(String md) {
            String[] lines = md.split("\r?\n");
            StringBuilder html = new StringBuilder();
            boolean inList = false;
            for (String ln : lines) {
                if (ln.startsWith("# ")) html.append(h(1, ln.substring(2)));
                else if (ln.startsWith("## ")) html.append(h(2, ln.substring(3)));
                else if (ln.startsWith("### ")) html.append(h(3, ln.substring(4)));
                else if (ln.startsWith("- ")) {
                    if (!inList) { html.append("<ul>"); inList = true; }
                    html.append("<li>").append(inline(ln.substring(2))).append("</li>");
                } else {
                    if (inList) { html.append("</ul>"); inList = false; }
                    if (!ln.isBlank()) html.append("<p>").append(inline(ln)).append("</p>");
                }
            }
            if (inList) html.append("</ul>");
            return html.toString();
        }
        private static String h(int level, String text) { return "<h"+level+">"+inline(text)+"</h"+level+">"; }
        private static String inline(String s) {
            s = esc(s);
            s = s.replaceAll("\\*\\*(.+?)\\*\\*", "<strong>$1</strong>");
            s = s.replaceAll("\\*(.+?)\\*", "<em>$1</em>");
            s = s.replaceAll("`([^`]+)`", "<code>$1</code>");
            s = s.replaceAll("\\[(.+?)\\]\\((.+?)\\)", "<a href=\"$2\">$1</a>");
            return s;
        }
        private static String esc(String s) { return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"); }
    }

    // ======================= 4) Cron-подобный планировщик =======================
    public static class MiniCron implements Closeable {
        private final ScheduledExecutorService ses = Executors.newScheduledThreadPool(1);
        private final List<Job> jobs = new CopyOnWriteArrayList<>();
        public Job schedule(String expr, Runnable task) {
            Job j = new Job(expr, task); jobs.add(j); j.scheduleNext(); return j;
        }
        @Override public void close() { ses.shutdownNow(); }
        public class Job {
            final String expr; final Runnable task; volatile ScheduledFuture<?> sf;
            public Job(String expr, Runnable task) { this.expr = expr; this.task = task; }
            void scheduleNext() {
                long delay = delayToNext(expr);
                sf = ses.schedule(() -> { try { task.run(); } finally { scheduleNext(); } }, delay, TimeUnit.MILLISECONDS);
            }
            public void cancel() { if (sf!=null) sf.cancel(true); jobs.remove(this); }
        }
        // expr: "*/5s" каждые 5 секунд; "m@15" каждую минуту в 15-й сек; "h@10:30" каждый час в 10:30 не поддержим, упростим
        private static long delayToNext(String expr) {
            Instant now = Instant.now();
            if (expr.endsWith("s") && expr.startsWith("*/")) {
                long sec = Long.parseLong(expr.substring(2, expr.length()-1));
                long millis = sec*1000;
                long next = ((now.toEpochMilli()/millis)+1)*millis;
                return next - now.toEpochMilli();
            } else if (expr.startsWith("m@")) { // m@SS — в каждую минуту в секунду SS
                int ss = Integer.parseInt(expr.substring(2));
                ZonedDateTime z = ZonedDateTime.ofInstant(now, ZoneId.systemDefault());
                ZonedDateTime n = z.withSecond(ss).withNano(0);
                if (!n.isAfter(z)) n = n.plusMinutes(1);
                return Duration.between(z, n).toMillis();
            } else {
                // по умолчанию раз в минуту
                long millis = 60_000;
                long next = ((now.toEpochMilli()/millis)+1)*millis;
                return next - now.toEpochMilli();
            }
        }
    }

    // ======================= 5) Вычислитель выражений =======================
    public static class ExprEval {
        // Поддержка + - * / ^ и скобок, функции: sin, cos, sqrt, ln
        public static double eval(String s) { return evalRpn(toRpn(tokenize(s))); }
        private static List<String> tokenize(String s) {
            List<String> t = new ArrayList<>(); StringBuilder num = new StringBuilder(); StringBuilder id = new StringBuilder();
            for (int i=0;i<s.length();i++) {
                char c = s.charAt(i);
                if (Character.isWhitespace(c)) continue;
                if (Character.isDigit(c) || c=='.') { num.append(c); continue; }
                if (Character.isLetter(c)) { id.append(c); continue; }
                if (num.length()>0) { t.add(num.toString()); num.setLength(0);} 
                if (id.length()>0) { t.add(id.toString()); id.setLength(0);} 
                t.add(String.valueOf(c));
            }
            if (num.length()>0) t.add(num.toString());
            if (id.length()>0) t.add(id.toString());
            return t;
        }
        private static int prec(String op) { return switch (op) { case "+","-"->1; case "*","/"->2; case "^"->3; default->-1; }; }
        private static boolean rightAssoc(String op) { return "^".equals(op); }
        private static List<String> toRpn(List<String> t) {
            List<String> out = new ArrayList<>(); Deque<String> st = new ArrayDeque<>();
            for (String x : t) {
                if (x.matches("[0-9.]+")) out.add(x);
                else if (x.matches("[a-zA-Z]+")) st.push(x);
                else if ("(".equals(x)) st.push(x);
                else if (")".equals(x)) {
                    while (!st.isEmpty() && !"(\".equals(st.peek())) out.add(st.pop());
                    if (!st.isEmpty() && "(\".equals(st.peek())) st.pop();
                    if (!st.isEmpty() && st.peek().matches("[a-zA-Z]+")) out.add(st.pop());
                } else { // operator
                    while (!st.isEmpty() && prec(st.peek())>=0 && (prec(st.peek())>prec(x) || (!rightAssoc(x) && prec(st.peek())==prec(x)))) out.add(st.pop());
                    st.push(x);
                }
            }
            while (!st.isEmpty()) out.add(st.pop());
            return out;
        }
        private static double evalRpn(List<String> rpn) {
            Deque<Double> st = new ArrayDeque<>();
            for (String x : rpn) {
                switch (x) {
                    case "+" -> st.push(st.pop()+st.pop());
                    case "-" -> { double b=st.pop(), a=st.pop(); st.push(a-b);} 
                    case "*" -> st.push(st.pop()*st.pop());
                    case "/" -> { double b=st.pop(), a=st.pop(); st.push(a/b);} 
                    case "^" -> { double b=st.pop(), a=st.pop(); st.push(Math.pow(a,b));}
                    default -> {
                        if (x.matches("[0-9.]+")) st.push(Double.parseDouble(x));
                        else st.push(applyFn(x, st.pop()));
                    }
                }
            }
            return st.pop();
        }
        private static double applyFn(String fn, double v) {
            return switch (fn.toLowerCase()) { case "sin"->Math.sin(v); case "cos"->Math.cos(v); case "sqrt"->Math.sqrt(v); case "ln"->Math.log(v); default->throw new IllegalArgumentException("Unknown fn "+fn); };
        }
    }

    // ======================= 6) BloomFilter и Trie =======================
    public static class BloomFilter {
        private final BitSet bits; private final int size; private final int k;
        public BloomFilter(int size, int k) { this.size=size; this.k=k; this.bits=new BitSet(size); }
        public void add(String s) { for (int i=0;i<k;i++) bits.set(hash(s,i)); }
        public boolean mightContain(String s) { for (int i=0;i<k;i++) if (!bits.get(hash(s,i))) return false; return true; }
        private int hash(String s, int i) { return Math.abs(Objects.hash(s, i)) % size; }
    }
    public static class Trie {
        static class Node { Map<Character, Node> ch = new HashMap<>(); boolean end; }
        private final Node root = new Node();
        public void add(String w) { Node n=root; for (char c: w.toCharArray()) n=n.ch.computeIfAbsent(c,k->new Node()); n.end=true; }
        public List<String> autocomplete(String prefix, int limit) { Node n=root; for (char c: prefix.toCharArray()) { n=n.ch.get(c); if (n==null) return List.of(); } List<String> out=new ArrayList<>(); dfs(n,new StringBuilder(prefix),out,limit); return out; }
        private void dfs(Node n, StringBuilder cur, List<String> out, int limit) { if (out.size()>=limit) return; if (n.end) out.add(cur.toString()); for (var e: n.ch.entrySet()) { cur.append(e.getKey()); dfs(e.getValue(), cur, out, limit); cur.setLength(cur.length()-1);} }
    }

    // ======================= 7) ZIP Utils =======================
    public static class ZipUtil {
        public static void zip(Path dir, Path zip) throws IOException {
            try (FileOutputStream fos = new FileOutputStream(zip.toFile()); java.util.zip.ZipOutputStream zos = new java.util.zip.ZipOutputStream(fos)) {
                Files.walk(dir).filter(Files::isRegularFile).forEach(p -> {
                    String entryName = dir.relativize(p).toString().replace('\\','/');
                    try { zos.putNextEntry(new java.util.zip.ZipEntry(entryName)); Files.copy(p, zos); zos.closeEntry(); } catch (IOException e) { throw new UncheckedIOException(e); }
                });
            }
        }
        public static void unzip(Path zip, Path dir) throws IOException {
            try (java.util.zip.ZipInputStream zis = new java.util.zip.ZipInputStream(new FileInputStream(zip.toFile()))) {
                java.util.zip.ZipEntry e; while ((e = zis.getNextEntry()) != null) { Path out = dir.resolve(e.getName()); Files.createDirectories(out.getParent()); Files.copy(zis, out, StandardCopyOption.REPLACE_EXISTING); zis.closeEntry(); }
            }
        }
    }

    // ======================= CLI Showcase =======================
    public static void main(String[] args) throws Exception {
        System.out.println("BigSuite — запускаем демонстрацию возможностей.\n");
        Scanner sc = new Scanner(System.in);

        // 1) Поднимем чат-сервер на фоне
        NioChatServer chat = new NioChatServer(9090);
        chat.startAsync();

        // 2) Инициализируем CSV Store
        Path dbPath = Paths.get("bigsuite_users.csv");
        try (CsvStore store = new CsvStore(dbPath, List.of("id","name","created"))) {
            store.put(List.of(UUID.randomUUID().toString(), "Alice", Instant.now().toString()));
            store.put(List.of(UUID.randomUUID().toString(), "Bob", Instant.now().toString()));
            store.snapshot();
        }

        // 3) Планировщик: каждую минуту в 15-й секунде печатаем пинг
        MiniCron cron = new MiniCron();
        var job = cron.schedule("m@15", () -> System.out.println("[Cron] tick @ "+ LocalTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss"))));

        // 4) Trie и BloomFilter подготовим
        Trie trie = new Trie();
        String[] words = {"hello","help","helium","heap","heart","heat","heavy","java","javascript","javelin"};
        for (String w : words) trie.add(w);
        BloomFilter bf = new BloomFilter(2048, 3);
        for (String w : words) bf.add(w);

        while (true) {
            System.out.println("\n=== MENU ===");
            System.out.println("1) Markdown → HTML");
            System.out.println("2) Eval expression");
            System.out.println("3) CSV: list users");
            System.out.println("4) Trie autocomplete");
            System.out.println("5) BloomFilter test");
            System.out.println("6) ZIP dir");
            System.out.println("7) UNZIP file");
            System.out.println("8) Info");
            System.out.println("0) Exit");
            System.out.print("> ");
            String cmd = sc.nextLine().trim();
            try {
                switch (cmd) {
                    case "1" -> {
                        System.out.println("Введите markdown (пустая строка — конец):");
                        StringBuilder md = new StringBuilder();
                        while (true) { String ln = sc.nextLine(); if (ln.isBlank()) break; md.append(ln).append('\n'); }
                        String html = Markdown.toHtml(md.toString());
                        System.out.println("HTML:\n" + html);
                    }
                    case "2" -> {
                        System.out.print("Expr (пример: sin(1)+2^3*4): ");
                        String e = sc.nextLine();
                        System.out.println("= " + ExprEval.eval(e));
                    }
                    case "3" -> {
                        try (CsvStore store = new CsvStore(dbPath, List.of("id","name","created"))) {
                            for (var r : store.all()) System.out.println(r);
                        }
                    }
                    case "4" -> {
                        System.out.print("Prefix: "); String p = sc.nextLine();
                        System.out.println("→ " + trie.autocomplete(p, 10));
                    }
                    case "5" -> {
                        System.out.print("Word to check: "); String w = sc.nextLine();
                        System.out.println("mightContain = " + bf.mightContain(w));
                    }
                    case "6" -> {
                        System.out.print("Dir to ZIP: "); Path d = Paths.get(sc.nextLine());
                        System.out.print("Zip file: "); Path z = Paths.get(sc.nextLine());
                        ZipUtil.zip(d, z); System.out.println("Zipped → " + z.toAbsolutePath());
                    }
                    case "7" -> {
                        System.out.print("Zip file: "); Path z = Paths.get(sc.nextLine());
                        System.out.print("Output dir: "); Path d = Paths.get(sc.nextLine());
                        ZipUtil.unzip(z, d); System.out.println("Unzipped → " + d.toAbsolutePath());
                    }
                    case "8" -> {
                        System.out.println("Чат-сервер: подключайтесь telnet/netcat к 127.0.0.1 9090");
                        System.out.println("Cron: задание m@15 печатает в 15-ю сек. каждой минуты");
                        System.out.println("DB: файл " + dbPath.toAbsolutePath());
                    }
                    case "0" -> {
                        System.out.println("Bye!");
                        chat.stop(); cron.close();
                        return;
                    }
                    default -> System.out.println("Неизвестная команда");
                }
            } catch (Exception ex) {
                System.out.println("Ошибка: " + ex.getMessage());
            }
        }
    }
}
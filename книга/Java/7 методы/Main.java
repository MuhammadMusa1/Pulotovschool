public class Main {
    public static void main(String[] args) {
        Main obj = new Main();
        int result = obj.add(5, 3);
        System.out.println("Result: " + result);
    }

    public int add(int a, int b) {
        return a + b;
    }
}
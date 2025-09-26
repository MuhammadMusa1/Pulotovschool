public class Calculator {
    public static void main(String[] args) {
        Calculator calc = new Calculator();
        int sum = calc.add(10, 20);
        int difference = calc.subtract(30, 15);
        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
    }

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }
}

public class Average {
    public static void main(String[] args) {
        double num1 = 4.5;
        double num2 = 3.0;
        double num3 = 5.5;

        double sum = num1 + num2 + num3;
        double average = sum / 3;

        double max = Math.max(num1, Math.max(num2, num3));
        double min = Math.min(num1, Math.min(num2, num3));

        System.out.println("Number 1: " + num1);
        System.out.println("Number 2: " + num2);
        System.out.println("Number 3: " + num3);
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);
        System.out.println("Max: " + max);
        System.out.println("Min: " + min);
    }
}
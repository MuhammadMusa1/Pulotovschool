import java.util.ArrayList;
import java.util.Random;

public class RandomNumbers {
    public static void main(String[] args) {
        ArrayList<Integer> numbers = new ArrayList<>();
        Random rand = new Random();

        for (int i = 0; i < 10; i++) {
            numbers.add(rand.nextInt(100)); // Добавляем случайные числа от 0 до 99
        }

        int sum = calculateSum(numbers);
        System.out.println("Numbers: " + numbers);
        System.out.println("Sum: " + sum);
    }

    public static int calculateSum(ArrayList<Integer> numbers) {
        int sum = 0;
        for (int number : numbers) {
            sum += number;
        }
        return sum;
    }
}
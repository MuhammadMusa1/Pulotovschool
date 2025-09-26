public class ArrayExample {
    public static void main(String[] args) {
        try {
            int[] numbers = {1, 2, 3};
            int number = getNumber(numbers, 5); // Это вызовет ArrayIndexOutOfBoundsException
            System.out.println("Number: " + number);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("ArrayIndexOutOfBoundsException caught: " + e.getMessage());
        } finally {
            System.out.println("This block is always executed.");
        }
    }

    public static int getNumber(int[] array, int index) {
        return array[index];
    }
}


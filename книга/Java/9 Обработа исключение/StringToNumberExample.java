public class StringToNumberExample {
    public static void main(String[] args) {
        String[] data = {"10", "20", "abc", "30"};

        for (String str : data) {
            try {
                int number = Integer.parseInt(str);
                System.out.println("Converted number: " + number);
            } catch (NumberFormatException e) {
                System.out.println("NumberFormatException caught: " + str + " is not a valid number.");
            }
        }
    }
}

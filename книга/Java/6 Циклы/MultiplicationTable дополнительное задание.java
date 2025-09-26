public class MultiplicationTable {
    public static void main(String[] args) {
        for (int i = 1; i <= 10; i++) {
            for (int j = 1; j <= 10; j++) {
                int result = i * j;
                if (result % 2 == 0) {
                    System.out.print(result + "\t");
                } else {
                    System.out.print("\t");
                }
            }
            System.out.println();
        }
    }
}
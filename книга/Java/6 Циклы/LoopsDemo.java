public class LoopsDemo {
    public static void main(String[] args) {
        for (int i = 0; i < 5; i++) {
            System.out.println("for loop, i = " + i);
        }

        int j = 0;
        while (j < 5) {
            System.out.println("while loop, j = " + j);
            j++;
        }

        int k = 0;
        do {
            System.out.println("do-while loop, k = " + k);
            k++;
        } while (k < 5);
    }
}
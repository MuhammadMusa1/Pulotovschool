import java.util.ArrayList;

public class BubbleSortStrings {

    public static void bubbleSort(ArrayList<String> list) {
        int n = list.size();
        boolean swapped;

        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                // Сравниваем строки лексикографически
                if (list.get(j).compareTo(list.get(j + 1)) > 0) {
                    // Меняем местами
                    String temp = list.get(j);
                    list.set(j, list.get(j + 1));
                    list.set(j + 1, temp);
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }

    public static void main(String[] args) {
        ArrayList<String> words = new ArrayList<>();
        words.add("banana");
        words.add("apple");
        words.add("cherry");
        words.add("date");

        bubbleSort(words);
        System.out.println(words); // [apple, banana, cherry, date]
    }
}
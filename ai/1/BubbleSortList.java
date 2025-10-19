import java.util.ArrayList;

public class BubbleSortList {

    public static void bubbleSort(ArrayList<Integer> list) {
        int n = list.size();
        boolean swapped;

        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (list.get(j) > list.get(j + 1)) {
                    // Меняем местами элементы
                    int temp = list.get(j);
                    list.set(j, list.get(j + 1));
                    list.set(j + 1, temp);
                    swapped = true;
                }
            }
            if (!swapped) break; // Ранний выход, если список уже отсортирован
        }
    }

    // Пример использования
    public static void main(String[] args) {
        ArrayList<Integer> numbers = new ArrayList<>();
        numbers.add(64);
        numbers.add(34);
        numbers.add(25);
        numbers.add(12);
        numbers.add(22);
        numbers.add(11);
        numbers.add(90);

        bubbleSort(numbers);

        System.out.println(numbers); // Вывод: [11, 12, 22, 25, 34, 64, 90]
    }
}
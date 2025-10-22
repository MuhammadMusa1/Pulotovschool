import java.util.ArrayList;
import java.util.Comparator;

public class GenericBubbleSort {

    // Обобщённый метод сортировки
    public static <T> void bubbleSort(ArrayList<T> list, Comparator<T> comparator) {
        int n = list.size();
        boolean swapped;

        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (comparator.compare(list.get(j), list.get(j + 1)) > 0) {
                    // Меняем местами
                    T temp = list.get(j);
                    list.set(j, list.get(j + 1));
                    list.set(j + 1, temp);
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }

    // Пример использования
    public static void main(String[] args) {
        // Строки — по длине (от коротких к длинным)
        ArrayList<String> words = new ArrayList<>();
        words.add("fig");
        words.add("apple");
        words.add("kiwi");
        words.add("banana");

        bubbleSort(words, Comparator.comparing(String::length));
        System.out.println("По длине: " + words); 
        // Вывод: [fig, kiwi, apple, banana]
        class Student {
    String name;
    int grade;

    Student(String name, int grade) {
        this.name = name;
        this.grade = grade;
    }

    @Override
    public String toString() {
        return name + "(" + grade + ")";
    }
}

        // Студенты — по оценке (по убыванию)
        ArrayList<Student> students = new ArrayList<>();
        students.add(new Student("Alice", 88));
        students.add(new Student("Bob", 92));
        students.add(new Student("Charlie", 75));

        bubbleSort(students, Comparator.comparingInt((Student s) -> s.grade).reversed());
        System.out.println("По оценке (убывание): " + students);
        // Вывод: [Bob(92), Alice(88), Charlie(75)]
    }
}
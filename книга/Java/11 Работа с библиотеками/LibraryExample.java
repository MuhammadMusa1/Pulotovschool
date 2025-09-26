import org.apache.commons.lang3.StringUtils;

public class LibraryExample {
    public static void main(String[] args) {
        String str = "Hello World!";
        System.out.println("Original: " + str);

        // Переворачиваем строку с использованием StringUtils
        String reversed = StringUtils.reverse(str);
        System.out.println("Reversed: " + reversed);

        // Проверяем, пустая ли строка
        boolean isEmpty = StringUtils.isEmpty(str);
        System.out.println("Is empty: " + isEmpty);
    }
}

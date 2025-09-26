import org.apache.commons.lang3.StringUtils;

public class ProjectExample {
    public static void main(String[] args) {
        String str1 = "Hello";
        String str2 = " World";
        
        // Объединяем строки
        String concatenated = StringUtils.join(str1, str2);
        System.out.println("Concatenated: " + concatenated);
        
        // Удаляем пробелы в начале и конце строки
        String trimmed = StringUtils.trim(concatenated);
        System.out.println("Trimmed: " + trimmed);
    }
}


import org.apache.commons.lang3.StringUtils;

public class StringArrayExample {
    public static void main(String[] args) {
        String[] strings = {"Hello", "", "World", "Java", ""};

        for (String str : strings) {
            if (StringUtils.isNotEmpty(str)) {
                String reversed = StringUtils.reverse(str);
                System.out.println("Original: " + str + ", Reversed: " + reversed);
            } else {
                System.out.println("Empty string found.");
            }
        }
    }
}

import java.time.Year;

public class MyInfo {
    public static void main(String[] args) {
        System.out.println("My name is [Ваше имя]");
        System.out.println("I am [Ваш возраст] years old");
        System.out.println("My favorite hobby is [Ваше хобби]");

        int currentYear = Year.now().getValue();
        System.out.println("Current year: " + currentYear);
    }
}
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class MyInfo {
    public static void main(String[] args) {
        System.out.println("My name is [Ваше имя]");
        System.out.println("I am [Ваш возраст] years old");

        LocalDateTime now = LocalDateTime.now();
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
        System.out.println("Current date and time: " + dtf.format(now));
    }
}
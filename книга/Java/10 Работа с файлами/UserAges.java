import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class UserAges {
    public static void main(String[] args) {
        String fileName = "users.txt";

        // Создание файла с данными
        try {
            FileWriter writer = new FileWriter(fileName);
            writer.write("Alice, 25\nBob, 17\nCharlie, 19\nDave, 15\nEve, 21");
            writer.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        // Чтение и обработка данных из файла
        try {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            String line;
            System.out.println("Users older than 18:");
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(", ");
                String name = parts[0];
                int age = Integer.parseInt(parts[1]);
                if (age > 18) {
                    System.out.println(name);
                }
            }
            reader.close();
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}

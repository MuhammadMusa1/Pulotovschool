import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;

public class NIOExample {
    public static void main(String[] args) {
        Path path = Paths.get("example.txt");
        try {
            Files.writeString(path, "Hello, world!");
            String content = Files.readString(path);
            System.out.println(content);
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


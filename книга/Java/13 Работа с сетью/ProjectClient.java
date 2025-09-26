import java.io.*;
import java.net.*;

public class ProjectClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 12345)) {
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            out.println("Привет, сервер!");
            String response = in.readLine();
            System.out.println("Ответ от сервера: " + response);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


import java.io.*;
import java.net.*;

public class ProjectServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            System.out.println("Сервер запущен, ожидаем подключения...");
            Socket clientSocket = serverSocket.accept();
            System.out.println("Клиент подключился!");

            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

            String message = in.readLine();
            System.out.println("Получено сообщение от клиента: " + message);

            out.println("Сообщение получено!");

            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


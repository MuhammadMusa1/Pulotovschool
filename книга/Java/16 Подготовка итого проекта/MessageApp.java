public class MessageApp {
    public static void main(String[] args) {
        sendMessage("Привет, мир!");
        receiveMessage();
    }

    public static void sendMessage(String message) {
        System.out.println("Отправка сообщения: " + message);
    }

    public static void receiveMessage() {
        System.out.println("Получено новое сообщение!");
    }
}



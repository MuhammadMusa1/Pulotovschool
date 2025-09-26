import javax.swing.*;

public class SimpleGUI {
    public static void main(String[] args) {
        // Создаем новое окно
        JFrame frame = new JFrame("Простое окно");
        frame.setSize(400, 200);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Создаем панель
        JPanel panel = new JPanel();
        frame.add(panel);
        placeComponents(panel);

        // Отображаем окно
        frame.setVisible(true);
    }

    private static void placeComponents(JPanel panel) {
        panel.setLayout(null);

        // Создаем метку
        JLabel userLabel = new JLabel("User:");
        userLabel.setBounds(10, 20, 80, 25);
        panel.add(userLabel);

        // Создаем текстовое поле
        JTextField userText = new JTextField(20);
        userText.setBounds(100, 20, 165, 25);
        panel.add(userText);

        // Создаем кнопку
        JButton loginButton = new JButton("Login");
        loginButton.setBounds(10, 80, 80, 25);
        panel.add(loginButton);
    }
}


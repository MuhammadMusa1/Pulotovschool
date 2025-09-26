import javax.swing.*;

public class ProjectGUI {
    public static void main(String[] args) {
        // Создаем новое окно
        JFrame frame = new JFrame("Проект GUI");
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
        JLabel label = new JLabel("Введите текст:");
        label.setBounds(10, 20, 100, 25);
        panel.add(label);

        // Создаем текстовое поле
        JTextField textField = new JTextField(20);
        textField.setBounds(120, 20, 165, 25);
        panel.add(textField);

        // Создаем кнопку
        JButton button = new JButton("Нажми меня");
        button.setBounds(10, 80, 120, 25);
        panel.add(button);
    }
}


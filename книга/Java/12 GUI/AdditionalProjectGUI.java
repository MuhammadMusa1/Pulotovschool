import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class AdditionalProjectGUI {
    public static void main(String[] args) {
        // Создаем новое окно
        JFrame frame = new JFrame("Дополнительное задание");
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

        // Создаем кнопку для вывода текста
        JButton printButton = new JButton("Вывести текст");
        printButton.setBounds(10, 80, 150, 25);
        panel.add(printButton);

        // Добавляем действие при нажатии на кнопку
        printButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println("Введенный текст: " + textField.getText());
            }
        });
    }
}


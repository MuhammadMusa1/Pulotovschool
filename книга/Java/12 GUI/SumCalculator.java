import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class SumCalculator {
    public static void main(String[] args) {
        // Создаем новое окно
        JFrame frame = new JFrame("Калькулятор суммы");
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

        // Создаем метку для первого числа
        JLabel label1 = new JLabel("Число 1:");
        label1.setBounds(10, 20, 80, 25);
        panel.add(label1);

        // Создаем текстовое поле для первого числа
        JTextField textField1 = new JTextField(20);
        textField1.setBounds(100, 20, 165, 25);
        panel.add(textField1);

        // Создаем метку для второго числа
        JLabel label2 = new JLabel("Число 2:");
        label2.setBounds(10, 50, 80, 25);
        panel.add(label2);

        // Создаем текстовое поле для второго числа
        JTextField textField2 = new JTextField(20);
        textField2.setBounds(100, 50, 165, 25);
        panel.add(textField2);

        // Создаем кнопку для вычисления суммы
        JButton sumButton = new JButton("Вычислить сумму");
        sumButton.setBounds(10, 80, 150, 25);
        panel.add(sumButton);

        // Добавляем действие при нажатии на кнопку
        sumButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    int num1 = Integer.parseInt(textField1.getText());
                    int num2 = Integer.parseInt(textField2.getText());
                    int sum = num1 + num2;
                    JOptionPane.showMessageDialog(null, "Сумма: " + sum);
                } catch (NumberFormatException ex) {
                    JOptionPane.showMessageDialog(null, "Пожалуйста, введите корректные числа.");
                }
            }
        });
    }
}


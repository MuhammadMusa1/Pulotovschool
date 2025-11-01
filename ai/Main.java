import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Класс Task — описывает задачу
class Task {
    private String title;
    private String description;
    private LocalDate dueDate;
    private boolean completed;

    public Task(String title, String description, LocalDate dueDate) {
        this.title = title;
        this.description = description;
        this.dueDate = dueDate;
        this.completed = false;
    }

    public String getTitle() {
        return title;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void markAsDone() {
        this.completed = true;
    }

    @Override
    public String toString() {
        return (completed ? "[✔]" : "[ ]") + " " + title + " (до " + dueDate + ")";
    }
}

// Класс TaskManager — управляет списком задач
class TaskManager {
    private List<Task> tasks = new ArrayList<>();

    public void addTask(Task task) {
        tasks.add(task);
    }

    public void showAllTasks() {
        if (tasks.isEmpty()) {
            System.out.println("Нет задач.");
            return;
        }
        for (int i = 0; i < tasks.size(); i++) {
            System.out.println((i + 1) + ". " + tasks.get(i));
        }
    }

    public void markTaskAsDone(int index) {
        if (index < 1 || index > tasks.size()) {
            System.out.println("Неверный номер задачи.");
            return;
        }
        tasks.get(index - 1).markAsDone();
        System.out.println("✅ Задача отмечена как выполненная!");
    }
}

// Основной класс программы
public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        TaskManager manager = new TaskManager();

        while (true) {
            System.out.println("\n=== Менеджер задач ===");
            System.out.println("1. Добавить задачу");
            System.out.println("2. Показать задачи");
            System.out.println("3. Отметить задачу как выполненную");
            System.out.println("4. Выход");
            System.out.print("Выберите действие: ");
            int choice = scanner.nextInt();
            scanner.nextLine(); // очистить ввод

            switch (choice) {
                case 1:
                    System.out.print("Введите название задачи: ");
                    String title = scanner.nextLine();
                    System.out.print("Введите описание: ");
                    String desc = scanner.nextLine();
                    System.out.print("Введите дату (в формате ГГГГ-ММ-ДД): ");
                    LocalDate date = LocalDate.parse(scanner.nextLine());
                    manager.addTask(new Task(title, desc, date));
                    System.out.println("✅ Задача добавлена!");
                    break;
                case 2:
                    manager.showAllTasks();
                    break;
                case 3:
                    manager.showAllTasks();
                    System.out.print("Введите номер задачи: ");
                    int num = scanner.nextInt();
                    manager.markTaskAsDone(num);
                    break;
                case 4:
                    System.out.println("👋 До встречи!");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Неверный выбор. Попробуйте снова.");
            }
        }
    }
}

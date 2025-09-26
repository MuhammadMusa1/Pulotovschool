// Main.java
import java.util.Scanner;
import java.util.List;

public class Main {
    private static TaskManager taskManager = new TaskManager();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (true) {
            printMenu();
            int choice = Integer.parseInt(scanner.nextLine());
            switch (choice) {
                case 1:
                    addTask();
                    break;
                case 2:
                    removeTask();
                    break;
                case 3:
                    markTaskAsCompleted();
                    break;
                case 4:
                    listTasks();
                    break;
                case 5:
                    System.out.println("Выход...");
                    return;
                case 6:
                	searchTasks();
                	break;
                case 7:
                	countTasks();
                	break;
                default:
                    System.out.println("Неверный выбор, попробуйте снова.");
            }
        }
    }

    private static void printMenu() {
        System.out.println("Меню:");
        System.out.println("1. Добавить задачу");
        System.out.println("2. Удалить задачу");
        System.out.println("3. Отметить задачу как выполненную");
        System.out.println("4. Список задач");
        System.out.println("5. Выход");
        System.out.println("6. Поиск задачи");
        System.out.println("7. Количество задач");
        System.out.print("Выберите опцию: ");
    }

    private static void addTask() {
        System.out.print("Введите описание задачи: ");
        String description = scanner.nextLine();
        taskManager.addTask(description);
    }

    private static void removeTask() {
        listTasks();
        System.out.print("Введите номер задачи для удаления: ");
        int index = Integer.parseInt(scanner.nextLine());
        taskManager.removeTask(index - 1);
    }

    private static void markTaskAsCompleted() {
        listTasks();
        System.out.print("Введите номер задачи для отметки как выполненной: ");
        int index = Integer.parseInt(scanner.nextLine());
        taskManager.markTaskAsCompleted(index - 1);
    }

    private static void listTasks() {
        System.out.println("Список задач:");
        List<Task> tasks = taskManager.getTasks();
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            System.out.println((i + 1) + ". " + task.getDescription() + (task.isCompleted() ? " (выполнено)" : ""));
        }
    }
    
 // Main.java
    private static void searchTasks() {
        System.out.print("Введите ключевое слово для поиска: ");
        String keyword = scanner.nextLine();
        List<Task> tasks = taskManager.searchTasks(keyword);
        System.out.println("Результаты поиска:");
        for (int i = 0; i < tasks.size(); i++) {
            Task task = tasks.get(i);
            System.out.println((i + 1) + ". " + task.getDescription() + (task.isCompleted() ? " (выполнено)" : ""));
        }
    }
 // Main.java
    private static void countTasks() {
        int completed = taskManager.countCompletedTasks();
        int incomplete = taskManager.countIncompleteTasks();
        System.out.println("Выполненные задачи: " + completed);
        System.out.println("Невыполненные задачи: " + incomplete);
    }
}


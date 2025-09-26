import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class ExtendedDatabase {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/mydatabase";
        String user = "root";
        String password = "password";

        try (Connection connection = DriverManager.getConnection(url, user, password);
             Statement statement = connection.createStatement()) {

            // Обновление данных
            String updateDataSQL = "UPDATE users SET name='Charlie' WHERE name='Alice'";
            statement.executeUpdate(updateDataSQL);

            // Удаление данных
            String deleteDataSQL = "DELETE FROM users WHERE name='Bob'";
            statement.executeUpdate(deleteDataSQL);

            // Выборка данных
            String selectSQL = "SELECT * FROM users";
            ResultSet resultSet = statement.executeQuery(selectSQL);

            while (resultSet.next()) {
                System.out.println("ID: " + resultSet.getInt("id"));
                System.out.println("Name: " + resultSet.getString("name"));
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


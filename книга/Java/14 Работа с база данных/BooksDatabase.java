import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class BooksDatabase {
    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/mydatabase";
        String user = "root";
        String password = "password";

        try (Connection connection = DriverManager.getConnection(url, user, password);
             Statement statement = connection.createStatement()) {

            // Создание таблицы
            String createTableSQL = "CREATE TABLE IF NOT EXISTS books ("
                    + "id INT AUTO_INCREMENT PRIMARY KEY, "
                    + "title VARCHAR(100) NOT NULL, "
                    + "author VARCHAR(100) NOT NULL, "
                    + "year INT NOT NULL)";
            statement.execute(createTableSQL);

            // Вставка данных
            String insertDataSQL = "INSERT INTO books (title, author, year) VALUES "
            		 + "('To Kill a Mockingbird', 'Harper Lee', 1960), "
                     + "('1984', 'George Orwell', 1949)";
             statement.executeUpdate(insertDataSQL);

             // Обновление данных
             String updateDataSQL = "UPDATE books SET year=1961 WHERE title='To Kill a Mockingbird'";
             statement.executeUpdate(updateDataSQL);

             // Удаление данных
             String deleteDataSQL = "DELETE FROM books WHERE title='1984'";
             statement.executeUpdate(deleteDataSQL);

             // Выборка данных
             String selectSQL = "SELECT * FROM books";
             ResultSet resultSet = statement.executeQuery(selectSQL);

             while (resultSet.next()) {
                 System.out.println("ID: " + resultSet.getInt("id"));
                 System.out.println("Title: " + resultSet.getString("title"));
                 System.out.println("Author: " + resultSet.getString("author"));
                 System.out.println("Year: " + resultSet.getInt("year"));
             }

         } catch (Exception e) {
             e.printStackTrace();
         }
     }
 }


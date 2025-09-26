import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class StudentGrades {
    public static void main(String[] args) {
        String inputFileName = "students.txt";
        String outputFileName = "average_grades.txt";

        try {
            BufferedReader reader = new BufferedReader(new FileReader(inputFileName));
            FileWriter writer = new FileWriter(outputFileName);
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(", ");
                String name = parts[0];
                int grade = Integer.parseInt(parts[1]);
                writer.write(name + ": " + grade + "\n");
            }
            reader.close();
            writer.close();
            System.out.println("Successfully calculated and wrote average grades to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class StudentGrades {
    public static void main(String[] args) {
        String inputFileName = "students.txt";
        String outputFileName = "grades_summary.txt";

        try {
            BufferedReader reader = new BufferedReader(new FileReader(inputFileName));
            FileWriter writer = new FileWriter(outputFileName);
            int maxGrade = Integer.MIN_VALUE;
            int minGrade = Integer.MAX_VALUE;
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(", ");
                int grade = Integer.parseInt(parts[1]);
                if (grade > maxGrade) {
                    maxGrade = grade;
                }
                if (grade < minGrade) {
                    minGrade = grade;
                }
            }
            writer.write("Max grade: " + maxGrade + "\n");
            writer.write("Min grade: " + minGrade + "\n");
            reader.close();
            writer.close();
            System.out.println("Successfully wrote grades summary to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


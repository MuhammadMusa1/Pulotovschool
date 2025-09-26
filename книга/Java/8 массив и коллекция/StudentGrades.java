public class StudentGrades {
    public static void main(String[] args) {
        int[] grades = {85, 90, 78, 92, 88};
        double average = calculateAverage(grades);
        System.out.println("Average grade: " + average);
    }

    public static double calculateAverage(int[] grades) {
        int sum = 0;
        for (int grade : grades) {
            sum += grade;
        }
        return (double) sum / grades.length;
    }
}


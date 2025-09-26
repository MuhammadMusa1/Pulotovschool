public class StudentGrades {
    public static void main(String[] args) {
        int[] grades = {85, 90, 78, 92, 88};
        double average = calculateAverage(grades);
        int maxGrade = findMax(grades);
        int minGrade = findMin(grades);
        System.out.println("Average grade: " + average);
        System.out.println("Max grade: " + maxGrade);
        System.out.println("Min grade: " + minGrade);
    }

    public static double calculateAverage(int[] grades) {
        int sum = 0;
        for (int grade : grades) {
            sum += grade;
        }
        return (double) sum / grades.length;
    }

    public static int findMax(int[] grades) {
        int max = grades[0];
        for (int grade : grades) {
            if (grade > max) {
                max = grade;
            }
        }
        return max;
    }

    public static int findMin(int[] grades) {
        int min = grades[0];
        for (int grade : grades) {
            if (grade < min) {
                min = grade;
            }
        }
        return min;
    }
}
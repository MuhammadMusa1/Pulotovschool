public class Rectangle {
    public static void main(String[] args) {
        Rectangle rect = new Rectangle();
        double length = 5.0;
        double width = 3.0;
        double area = rect.calculateArea(length, width);
        double perimeter = rect.calculatePerimeter(length, width);
        System.out.println("Area: " + area);
        System.out.println("Perimeter: " + perimeter);
    }

    public double calculateArea(double length, double width) {
        return length * width;
    }

    public double calculatePerimeter(double length, double width) {
        return 2 * (length + width);
    }
}


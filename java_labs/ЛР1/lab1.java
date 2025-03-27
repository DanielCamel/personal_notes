package ЛР1;

class lab1 {
    public static void main(String[] args) {
        // Начинаем с самой внутренней части
        double value = Math.sqrt(63);
                
        // Двигаемся к внешнему корню
        for (int i = 60; i >= 3; i -= 3) {
            value = Math.sqrt(i + value);
        }

        // Вывод результата
        System.out.printf("Результат: %.6f%n", value);
    }    
}
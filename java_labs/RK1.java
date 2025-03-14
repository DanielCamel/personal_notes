// РК1. Вариант №8. Создать класс «целое число».
import java.util.Locale;
import java.util.Scanner; 

class IntNumber {
    // Поля (атрибуты) класса 
    private int value; // Целое значение

    // Конструктор - создаёт объект на основе целого значения.
    public IntNumber(int value) {
        this.value = value; // имя поля класса и передаваемого в конструктор параметра совпадают.
    }

    // Метод доступа (геттер) для получения значения.
    public int getValue() {
        return value;
    }

    // Метод, проверяющий четность (parity) целого числа
    public boolean СheckParity() {
        boolean IsEven = (value % 2 == 0); // Проверяем, делится ли число на 2 (остаток от деления =0) 
        return IsEven;
    }
    
    // Метод печати параметров объекта
    public void printInfo() {
        System.out.println("Число: " + value + ", Чётность: " + СheckParity());
    }
}

// Класс RK1 (Main)
public class RK1 {
    public static void main(String[] args) {
        // создаём новый объект класса Scanner для считывания данных из консоли
        // System.in - стандартный поток ввода с клавиатуры
        Scanner scanner = new Scanner(System.in).useLocale(Locale.US); // Устанавливаем локаль, которая использует ТОЧКУ как разделитель  

        System.out.print("Сколько целых чисел хотите создать?: ");
        int number_of_int = scanner.nextInt(); // nextInt() - метод для считывания целого числа из консоли.

        // Создание массива объектов IntNumber (выделяем место под него)
        IntNumber[] numbers = new IntNumber[number_of_int];

        System.out.println("Если число чётное - true, иначе - false");
        
        for (int i = 0; i < number_of_int; i++) {
            System.out.print("Введите число #" + (i+1) + ": ");
            int value = scanner.nextInt(); 
            // создаём новый объект класса IntNumber
            // сохраняем созданный объект в i-й элемент массива
            numbers[i] = new IntNumber(value);
        }
        
        // Выводим числа из массива и проверяем их на чётность
        for (IntNumber number : numbers) {
            number.printInfo(); // Печатаем параметры объекта
        }
        scanner.close();
    }
}
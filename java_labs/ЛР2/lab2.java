package ЛР2;
/* 
Стандартный пакет java.util содержит классы, связанные с
коллекциями, датами, случайными числами и I/O
Импортируем класс Scanner из пакета java.util, который
используется для чтения данных (с клавиатуры, из файла, из строки и т.д.).
*/
import java.util.Locale;
import java.util.Scanner; 

// Класс RealNumber - веществ. число с его значением и строковым представлением
class RealNumber {
    // Поля (атрибуты) класса 
    private double value; // Вещественное значение
    private String stringValue; // Строковое представление

    // Конструктор - создаёт объект на основе вещественного значения.
    // У конструктора нет возвращаемого значения
    // Конструктор инициализирует поля; его имя совпадает с именем класса.
    public RealNumber(double value) {
        // this — ключевое слово, которое означает «этот объект»
        this.value = value; // имя поля класса и передаваемого в конструктор параметра совпадают.
        this.stringValue = String.valueOf(value); // метод String.valueOf() преобразует число (double) в строку (String).
    }

    // Метод доступа (геттер) для получения значения.
    public double getValue() {
        return value;
    }

    // Метод доступа (геттер) для получения строкового представления.
    public String getStringValue() {
        return stringValue;
    } 

    // Метод подсчёта количетсва цифр в целой части числа.
    // .split() — метод класса String, который разбивает строку 
    // на части по заданному разделителю и возвращает массив строк. Разделитель — это регулярное выражение (regex).
    // "\\." - экранирование точки. . (точка) - спец. символ в regex, означающий "любой символ"
    public int getIntegerPartLength() {
        String IntegerPart = stringValue.split("\\.")[0]; // Отделяем целую часть - берём нулевой элемент массива [0] 
        return IntegerPart.length();
    }

    // Метод печати параметров объекта
    public void printInfo() {
        System.out.println("Число:" + value + ", Строковое представление: " + stringValue);
    }
}

// Класс Main
class Main {
    public static void main(String[] args) {
        // создаём новый объект класса Scanner для считывания данных из консоли
        // System.in - стандартный поток ввода с клавиатуры
        Scanner scanner = new Scanner(System.in).useLocale(Locale.US); // Устанавливаем локаль, которая использует точку как разделитель  

        // Ввод количества чисел
        System.out.print("Введите количество чисел: ");
        int n = scanner.nextInt(); // nextInt() — метод для считывания целого числа (int) из консоли.

        // Создание массива объектов RealNumber
        RealNumber[] numbers = new RealNumber[n];

        // Ввод значений и создание объектов
        for (int i = 0; i < n; i++) {
            System.out.print("Введите вещественное число: ");
            double value = scanner.nextDouble(); // nextDouble() - метод для считывания числа (double) из консоли.
            // создаём новый объект класса RealNumber, передавая введённое число в конструктор.
            // сохраняем созданный объект в i-й элемент массива
            numbers[i] = new RealNumber(value);
        }

        // Подсчет суммы и общего количества цифр в целых частях
        double sum = 0;
        int totalDigits = 0;

        System.out.println("\nСписок введённых чисел:");
        // Расширенный цикл foreach для перебора элементов массива
        for (RealNumber number : numbers) {
            number.printInfo(); // Печатаем параметры объекта
            sum += number.getValue();
            totalDigits += number.getIntegerPartLength();
        }

        // Вывод результатов
        System.out.println("\nСумма всех введённых чисел " + sum);
        System.out.println("Суммарное количество цифр в целых частяз всех чисел: " + totalDigits);

        scanner.close();
    }
}
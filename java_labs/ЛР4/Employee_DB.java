package ЛР4;

import java.io.*;
import java.util.*;
import java.util.Locale;

// Класс, представляющий сотрудника
class Employee implements Serializable {
    private String fullName;
    private int birthYear;
    private String position;
    private double employmentRate;
    private String hireDate;
    private String SNILS;
    private Map<String, Double> departments;

    // Конструктор
    public Employee(String fullName, int birthYear, String position, double employmentRate, String hireDate, String SNILS) {
        this.fullName = fullName;
        this.birthYear = birthYear;
        this.position = position;
        this.employmentRate = employmentRate;
        this.hireDate = hireDate;
        this.SNILS = SNILS;
        this.departments = new HashMap<>();
    }

    // Геттеры и сеттеры
    public String getSNILS() { return SNILS; }
    public String getFullName() { return fullName; }
    public int getBirthYear() { return birthYear; }
    public void setFullName(String fullName) { this.fullName = fullName; }
    public void setPosition(String position) { this.position = position; }

    // Добавление и удаление сотрудника в подразделениях
    public void addDepartment(String department, double rate) { departments.put(department, rate); }
    public void removeDepartment(String department) { departments.remove(department); }

    @Override
    public String toString() {
        // Отображение сотрудника с нужными полями
        StringBuilder depString = new StringBuilder();
        for (Map.Entry<String, Double> entry : departments.entrySet()) {
            depString.append("\n-> ").append(entry.getKey()).append(" - ставка: ").append(entry.getValue());
        }
        return "ФИО: " + fullName + 
               "\nГод рождения: " + birthYear + 
               "\nДолжность: " + position + 
               "\nСтавка: " + employmentRate + 
               "\nДата приёма: " + hireDate + 
               "\nСНИЛС: " + SNILS + 
               depString.toString();
    }
}

// Класс, представляющий структурное подразделение
class Department implements Serializable {
    private String name;
    private String description;
    private Map<String, Double> positions;

    // Конструктор
    public Department(String name, String description) {
        this.name = name;
        this.description = description;
        this.positions = new HashMap<>();
    }

    // Геттеры и сеттеры
    public String getName() { return name; }
    public void setDescription(String description) { this.description = description; }

    // Управление штатным расписанием
    public void addPosition(String position, double rate) { positions.put(position, rate); }
    public void removePosition(String position) { positions.remove(position); }

        @Override
        public String toString() {
            // Отображение подразделения с нужными полями
            StringBuilder positionString = new StringBuilder();
            for (Map.Entry<String, Double> entry : positions.entrySet()) {
                positionString.append("\n-> ").append(entry.getKey()).append(" - ставка: ").append(entry.getValue());
            }
            return "Название подразделения: " + name + 
                "\nОписание: " + description + 
                positionString.toString();
    }
}

// Класс для управления базой данных сотрудников и подразделений
class Database {
    private Map<String, Employee> employees;
    private Map<String, Department> departments;
    private static final String FILE_NAME = "database.dat";

    // Конструктор: загружает данные из файла
    public Database() {
        employees = new HashMap<>();
        departments = new HashMap<>();
        loadFromFile();
    }

    // Методы управления сотрудниками
    public void addEmployee(Employee employee) {
        employees.put(employee.getSNILS(), employee);
        saveToFile();
    }

    public void removeEmployee(String SNILS) {
        employees.remove(SNILS);
        saveToFile();
    }

    public Employee findEmployeeBySNILS(String SNILS) {
        return employees.get(SNILS);
    }

    public void updateEmployee(String SNILS, String newName) {
        if (employees.containsKey(SNILS)) {
            employees.get(SNILS).setFullName(newName);
            saveToFile();
        }
    }

    // Методы управления подразделениями
    public void addDepartment(Department department) {
        departments.put(department.getName(), department);
        saveToFile();
    }

    public void removeDepartment(String name) {
        departments.remove(name);
        saveToFile();
    }

    // Вывод списков сотрудников и подразделений
    public void listEmployees() {
        for (Employee emp : employees.values()) {
            System.out.println(emp);
            System.out.println("------------------------------------");
        }
    }

    public void listDepartments() {
        for (Department dep : departments.values()) {
            System.out.println(dep);
            System.out.println("------------------------------------");
        }
    }

    // Возвращает список всех подразделений
    public Map<String, Department> getDepartments() {
        return departments;
    }

    // Сохранение и загрузка данных
    private void saveToFile() {
        try (ObjectOutputStream oos = new ObjectOutputStream(
                new BufferedOutputStream(new FileOutputStream(FILE_NAME)))) {
            oos.writeObject(employees);
            oos.writeObject(departments);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void loadFromFile() {
        File file = new File(FILE_NAME);
        if (!file.exists()) return;
        try (ObjectInputStream ois = new ObjectInputStream(
                new BufferedInputStream(new FileInputStream(FILE_NAME)))) {
            employees = (Map<String, Employee>) ois.readObject();
            departments = (Map<String, Department>) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}

// Основной класс для запуска программы с интерактивным меню
public class Employee_DB {
    public static void main(String[] args) {
        Database database = new Database();
        Scanner scanner = new Scanner(System.in);
        scanner.useLocale(Locale.US); // Устанавливаем локаль для корректного ввода чисел с плавающей запятой

        // Добавляем несколько тестовых подразделений
        database.addDepartment(new Department("IT", "Отдел информационных технологий"));
        database.addDepartment(new Department("HR", "Отдел кадров"));
        database.addDepartment(new Department("Marketing", "Отдел маркетинга"));

        while (true) {
            System.out.println("\nМеню:");
            System.out.println("1. Добавить сотрудника");
            System.out.println("2. Вывести всех сотрудников");
            System.out.println("3. Найти сотрудника по СНИЛС");
            System.out.println("4. Изменить имя сотрудника по СНИЛС");
            System.out.println("5. Удалить сотрудника по СНИЛС");
            System.out.println("6. Добавить подразделение");
            System.out.println("7. Вывести все подразделения");
            System.out.println("8. Выйти");
            System.out.print("Выберите действие: ");
            int choice = scanner.nextInt();
            scanner.nextLine();

            switch (choice) {
                case 1:
                    System.out.println("Выберите подразделение:");
                    database.listDepartments();
                    System.out.print("Введите название подразделения: ");
                    String depName = scanner.nextLine();

                    // Проверка наличия подразделения
                    if (database.getDepartments().containsKey(depName)) {
                        System.out.print("ФИО: ");
                        String name = scanner.nextLine();
                        System.out.print("Год рождения: ");
                        int year = scanner.nextInt();
                        scanner.nextLine();
                        System.out.print("Должность: ");
                        String position = scanner.nextLine();
                        System.out.print("Ставка: ");
                        double rate = scanner.nextDouble();
                        scanner.nextLine();  // Чтобы пропустить символ новой строки

                        System.out.print("Дата вступления в должность: ");
                        String hireDate = scanner.nextLine();
                        System.out.print("СНИЛС: ");
                        String snils = scanner.nextLine();

                        // Добавляем сотрудника
                        Employee employee = new Employee(name, year, position, rate, hireDate, snils);
                        employee.addDepartment(depName, rate);  // Добавляем выбранное подразделение
                        database.addEmployee(employee);
                    } else {
                        System.out.println("Подразделение не найдено!");
                    }
                    break;
                case 2:
                    database.listEmployees();
                    break;
                case 3:
                    System.out.print("Введите СНИЛС: ");
                    String searchSnils = scanner.nextLine();
                    System.out.println(database.findEmployeeBySNILS(searchSnils));
                    break;
                case 4:
                    System.out.print("Введите СНИЛС: ");
                    String snilsToUpdate = scanner.nextLine();
                    System.out.print("Новое имя: ");
                    String newName = scanner.nextLine();
                    database.updateEmployee(snilsToUpdate, newName);
                    break;
                case 5:
                    System.out.print("Введите СНИЛС: ");
                    String snilsToDelete = scanner.nextLine();
                    database.removeEmployee(snilsToDelete);
                    break;
                case 6:
                    System.out.print("Название подразделения: ");
                    String depNameNew = scanner.nextLine();
                    System.out.print("Описание: ");
                    String depDesc = scanner.nextLine();
                    Department newDept = new Department(depNameNew, depDesc);
                    
                    System.out.println("Введите штатное расписание (должности и ставки):");
                    while (true) {
                        System.out.print("Должность: ");
                        String position = scanner.nextLine();
                        System.out.print("Ставка: ");
                        double rate = scanner.nextDouble();
                        scanner.nextLine(); // Чистим символ новой строки
                        newDept.addPosition(position, rate);

                        System.out.print("Добавить ещё должность? (y/n): ");
                        String continueAdding = scanner.nextLine();
                        if (!continueAdding.equalsIgnoreCase("y")) {
                            break;
                        }
                    }

                    database.addDepartment(newDept);
                    break;
                case 7:
                    database.listDepartments();
                    break;
                case 8:
                    return;
            }
        }
    }
}

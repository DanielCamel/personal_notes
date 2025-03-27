package ЛР3;

import java.io.*;  // Импорт классов для работы с файлами
import java.nio.charset.StandardCharsets;  // Кодировка UTF-8
import java.security.*;  // Криптографические алгоритмы (пр.,SHA-512)
import java.util.*;  // Коллекции (HashMap, Arrays)
import java.util.Base64;  // Кодирование Base64
import java.util.regex.*;  // Регулярные выражения

// Класс, представляющий пользователя
class User {
    private String login;  // Логин пользователя
    private byte[] passwordHash;  // Хеш пароля
    private byte[] salt;  // Соль для хеширования

    // Конструктор: создаёт нового пользователя, генерируя соль и хешируя пароль
    public User(String login, String password) throws NoSuchAlgorithmException {
        // если передан пустой пароль, то создается пустая соль и хеш,
        // но не выполняется проверка пароля.
        if (password != null && !password.isEmpty()) 
        {
            if (!isValidPassword(password)) {
                throw new SecurityException("Пароль не соответствует политике безопасности");
            }
            this.salt = generateSalt();  // Генерируем случайную соль
            this.passwordHash = hashPassword(password, salt);  // Хешируем пароль с солью
        } else {
            // Если пароль пустой, создаем пустую соль и хеш
            this.passwordHash = new byte[0];
            this.salt = new byte[0];
        }   
            this.login = login;  // Сохраняем логин  
        }

    // Геттер для логина пользователя
    public String getLogin() {
        return login;
    }

    // Проверяет, совпадает ли хеш введенного пароля с сохранённым хешем
    public boolean verifyPassword(String password) throws NoSuchAlgorithmException {
        return Arrays.equals(passwordHash, hashPassword(password, salt));
    }

    // Метод изменения пароля
    public void changePassword(String oldPassword, String newPassword) throws NoSuchAlgorithmException {
            if (!verifyPassword(oldPassword)) {
                throw new SecurityException("Старый пароль неверен");
            // объект исключения выбрасывается в точку, где возникла ошибка
        }
        if (oldPassword.equals(newPassword)) {
            throw new SecurityException("Новый пароль не должен совпадать со старым");
        }
        if (!isValidPassword(newPassword)) {
            throw new SecurityException("Пароль не соответствует политике безопасности");
        }
        this.salt = generateSalt();  // Генерируем новую соль
        this.passwordHash = hashPassword(newPassword, salt);  // Хешируем новый пароль
    }

    // Хеширование пароля с солью
    private static byte[] hashPassword(String password, byte[] salt) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-512");  // Алгоритм SHA-512
        md.update(salt);  // Добавляем соль
        return md.digest(password.getBytes(StandardCharsets.UTF_8));  // Возвращаем хеш пароля
    }

    // Генерация случайной соли (16 байт)
    private static byte[] generateSalt() {
        SecureRandom random = new SecureRandom();
        byte[] salt = new byte[16];
        random.nextBytes(salt);
        return salt;
    }

    // Преобразует объект в строку для сохранения в файл
    public String toFileString() {
        return login + ":" + Base64.getEncoder().encodeToString(salt) + ":" + Base64.getEncoder().encodeToString(passwordHash);
        // return login + ":" + salt + ":" + passwordHash;
    }

    // Восстанавливает объект User из строки (считанной из файла)
    public static User fromFileString(String line) throws NoSuchAlgorithmException {
        String[] parts = line.split(":");
        if (parts.length != 3) {
            throw new IllegalArgumentException("Неверный формат строки");
        }
        String login = parts[0];
        byte[] salt = Base64.getDecoder().decode(parts[1]);
        byte[] passwordHash = Base64.getDecoder().decode(parts[2]);
        
        // Пустой пароль для восстановления
        User user = new User(login, ""); 
        user.salt = salt;
        user.passwordHash = passwordHash;
        return user;
    }

    // Проверка, соответствует ли пароль политике безопасности
    private static boolean isValidPassword(String password) {
        // Проверка длины пароля
        if (password.length() < 8) {
            return false;
        }
        // Регулярное выражение для проверки различных категорий символов
        // Pattern - создание шаблона регулярного выражения
        // Matcher - проверка строки на соответствие шаблону
        Pattern pattern = Pattern.compile("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!$#%]).{8,}$");
        Matcher matcher = pattern.matcher(password);
        return matcher.matches();
    }
}

// Класс для работы с пользователями в файле
class UserDatabase {
    private static final String FILE_NAME = "users.txt";  // Файл хранения пользователей
    private HashMap<String, User> users = new HashMap<>();  // Хранилище пользователей (ключ - логин)

    // Конструктор, который загружает пользователей из файла при создании объекта
    public UserDatabase() {
        try {
            loadUsers();  // Загружаем пользователей из файла
        } catch (IOException | NoSuchAlgorithmException e) {
            System.out.println("Ошибка загрузки пользователей: " + e.getMessage());
        }
    }    

    // Загрузка пользователей из файла
    private void loadUsers() throws IOException, NoSuchAlgorithmException {
        File file = new File(FILE_NAME);
        if (file.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    User user = User.fromFileString(line);  // Восстановление пользователя из строки
                    users.put(user.getLogin(), user);  // Добавляем в коллекцию
                }
            }
        }
    }

    // Регистрация нового пользователя
    public void register(String login, String password, String confirmPassword) throws Exception {
        if (users.containsKey(login)) {
            throw new Exception("Пользователь уже существует");
        }
        if (!password.equals(confirmPassword)) {
            throw new Exception("Пароли не совпадают");
        }
        if (password.isEmpty()) {
            throw new Exception("Пароль не может быть пустым");
        }
        users.put(login, new User(login, password));
        saveUsers();
    }

    // Аутентификация (проверка логина и пароля)
    public boolean authenticate(String login, String password) throws Exception {
        User user = users.get(login);
        return user != null && user.verifyPassword(password);
    }

    // Смена пароля пользователя
    public void changePassword(String login, String oldPassword, String newPassword) throws Exception {
        User user = users.get(login);
        if (user == null) throw new Exception("Пользователь не найден");
        user.changePassword(oldPassword, newPassword);
        saveUsers();
    }

    // Сохранение пользователей в файл
    private void saveUsers() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(FILE_NAME))) {
            for (User user : users.values()) {
                writer.write(user.toFileString());
                writer.newLine();  // Запись новой строки
            }
        } catch (IOException e) {
            // Если произошла ошибка записи, выводим её в консоль
            e.printStackTrace();
        }
    }

}

// Главный класс программы
public class AuthEngine {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        UserDatabase db = new UserDatabase();
        
        boolean running = true;
        while (running) {
            System.out.println("1. Регистрация\n2. Вход\n3. Смена пароля\n4. Выход");
            System.out.print("Выберите действие: ");
            int choice = scanner.nextInt();
            scanner.nextLine();  // Очищаем буфер
            
            try {
                switch (choice) {
                    case 1 -> {
                        System.out.print("Логин: ");
                        String login = scanner.nextLine();
                        System.out.print("Пароль: ");
                        String password = scanner.nextLine();
                        System.out.print("Подтверждение пароля: ");
                        String confirmPassword = scanner.nextLine();
                        db.register(login, password, confirmPassword);
                        System.out.println("Регистрация успешна!");
                    }
                    case 2 -> {
                        System.out.print("Логин: ");
                        String login = scanner.nextLine();
                        System.out.print("Пароль: ");
                        String password = scanner.nextLine();
                        System.out.println(db.authenticate(login, password) ? "Вход выполнен" : "Ошибка входа");
                    }
                    case 3 -> {
                        System.out.print("Логин: ");
                        String login = scanner.nextLine();
                        System.out.print("Старый пароль: ");
                        String oldPassword = scanner.nextLine();
                        System.out.print("Новый пароль: ");
                        String newPassword = scanner.nextLine();
                        db.changePassword(login, oldPassword, newPassword);
                        System.out.println("Пароль изменён");
                    }
                    case 4 -> {
                        System.out.println("Выход...");
                        running = false;
                    }
                    default -> {
                        System.out.println("Ошибка: Введите число от 1 до 4.");
                    }
                }
            } catch (Exception e) {
                System.out.println("Ошибка: " + e.getMessage());
            }
        }
        scanner.close();
    }
}

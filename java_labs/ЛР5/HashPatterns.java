package ЛР5;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

// Абстрактный класс (интерфейс) Hash, реализующий "Шаблонный метод"
abstract class Hash {
    // Абстрактный метод для получения хеша, который переопределяется в подклассах
    public abstract String getHash(String data);

    // Общий метод для преобразования строки в хеш с заданным алгоритмом
    // (Это реализация "ШАБЛОННОГО МЕТОДА: базовый алгоритм одинаков для всех,
    // а конкретные подклассы переопределяют только СПОСОБ его ВЫЗОВА)

    protected String digestJavaHexString(String algorithm, String message) {
        StringBuilder sb = new StringBuilder();
        try {
            MessageDigest md = MessageDigest.getInstance(algorithm);
            md.update(message.getBytes());
            byte[] digest = md.digest();
            for (byte b : digest) {
                sb.append(String.format("%02x", b & 0xff));
            }
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return sb.toString();
    }
}

// Конкретная реализация хеширования с использованием MD5
class MD5Hash extends Hash {
    @Override
    public String getHash(String data) {
        return "MD5: " + digestJavaHexString("MD5", data);
    }
}

// Конкретная реализация хеширования с использованием SHA-256
class SHA256Hash extends Hash {
    @Override
    public String getHash(String data) {
        return "SHA-256: " + digestJavaHexString("SHA-256", data);
    }
}

// Конкретная реализация хеширования с использованием SHA-1
class SHA1Hash extends Hash {
    @Override
    public String getHash(String data) {
        return "SHA-1: " + digestJavaHexString("SHA-1", data);
    }
}

// Конкретная реализация хеширования с использованием SHA-512
class SHA512Hash extends Hash {
    @Override
    public String getHash(String data) {
        return "SHA-512: " + digestJavaHexString("SHA-512", data);
    }
}


// Класс, реализующий паттерн "СТРАТЕГИЯ"

class HashGenerator {
    // Метод принимает объект класса, производного от Hash, и вызывает его метод getHash
    // Этот метод использует "СТРАТЕГИЮ", так как он не знает, какой именно хеш будет вычисляться.
    // Он просто принимает объект типа Hash (интерфейса) и вызывает его метод getHash.
    // Таким образом, реализация алгоритма может быть легко заменена без изменения HashGenerator.
    public String getHash(String data, Hash hash) {
        return hash.getHash(data);
    }
}

// Главный класс
public class HashPatterns {
    public static void main(String[] args) {
        String data = "Хорошего дня!";
        System.out.println("\n" + "Исходный текст: " + data + "\n");
        
        HashGenerator generator = new HashGenerator();
        
        // Использование разных стратегий для хеширования
        Hash md5Hash = new MD5Hash();
        System.out.println(generator.getHash(data, md5Hash));
        
        Hash sha256Hash = new SHA256Hash();
        System.out.println(generator.getHash(data, sha256Hash));
        
        Hash sha1Hash = new SHA1Hash();
        System.out.println(generator.getHash(data, sha1Hash));
        
        Hash sha512Hash = new SHA512Hash();
        System.out.println(generator.getHash(data, sha512Hash));
    }
}

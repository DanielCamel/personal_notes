package com.example;

public class MyCalc {
    // Сложение
    public double getSum(double x, double y) {
        return x + y;
    }

    // Вычитание
    public double getSub(double x, double y) {
        return x - y;
    }

    // Умножение
    public double getMul(double x, double y) {
        return x * y;
    }

    // Деление
    public double getDiv(double x, double y) {
        return x / y;
    }

    // Возведение в степень
    public double getPow(double x, double y) {
        return Math.pow(x, y);
    }

    // Взятие логарифма (аргумент и основание)
    public double getLog(double arg, double base) {
        // Используем преобразование через натуральный логарифм
        return Math.log(arg) / Math.log(base);
    }
}

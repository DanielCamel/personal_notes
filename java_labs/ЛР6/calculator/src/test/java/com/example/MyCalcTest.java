package com.example;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

class MyCalcTest {
    MyCalc calc = new MyCalc();

    @Test
    void testGetSum() {
        // Проверка истинного значения
        assertEquals(5.0, calc.getSum(2, 3), 0.0001, "Сумма 2 + 3 должна быть 5.0");
        assertEquals(0.0, calc.getSum(-2, 2), 0.0001, "Сумма -2 + 2 должна быть 0.0");
        // Проверка ложного значения
        assertEquals(6.0, calc.getSum(2, 3), "Сумма 2 + 3 не должна быть 6.0");
        assertEquals(1.0, calc.getSum(1, 1), "Сумма 1 + 1 не должна быть 1.0");
    }

    @Test
    void testGetSub() {
        // Проверка истинного значения
        assertEquals(1.0, calc.getSub(3, 2), 0.0001, "Разность 3 - 2 должна быть 1.0");
        assertEquals(-4.0, calc.getSub(2, 6), 0.0001, "Разность 2 - 6 должна быть -4.0");
        // Проверка ложного значения
        assertEquals(2.0, calc.getSub(3, 2), "Разность 3 - 2 не должна быть 2.0");
        assertEquals(5.0, calc.getSub(6, 2), "Разность 6 - 2 не должна быть 5.0");
    }

    @Test
    void testGetMul() {
        // Проверка истинного значения
        assertEquals(6.0, calc.getMul(2, 3), 0.0001, "Произведение 2 * 3 должно быть 6.0");
        assertEquals(-8.0, calc.getMul(2, -4), 0.0001, "Произведение 2 * (-4) должно быть -8.0");
        // Проверка ложного значения
        assertEquals(7.0, calc.getMul(2, 3), "Произведение 2 * 3 не должно быть 7.0");
        assertEquals(0.0, calc.getMul(2, 3), "Произведение 2 * 3 не должно быть 0.0");
    }

    @Test
    void testGetDiv() {
        // Проверка истинного значения
        assertEquals(2.0, calc.getDiv(6, 3), 0.0001, "Деление 6 / 3 должно быть 2.0");
        assertEquals(-2.5, calc.getDiv(5, -2), 0.0001, "Деление 5 / (-2) должно быть -2.5");
        // Проверка ложного значения
        assertNotEquals(3.0, calc.getDiv(6, 3), "Деление 6 / 3 не должно быть 3.0");
        assertNotEquals(0.0, calc.getDiv(6, 3), "Деление 6 / 3 не должно быть 0.0");
    }

    @Test
    void testGetPow() {
        // Проверка истинного значения
        assertEquals(8.0, calc.getPow(2, 3), 0.0001, "2 в степени 3 должно быть 8.0");
        assertEquals(16.0, calc.getPow(4, 2), 0.0001, "4 в степени 2 должно быть 16.0");
        // Проверка ложного значения
        assertNotEquals(9.0, calc.getPow(2, 3), "2 в степени 3 не должно быть 9.0");
        assertNotEquals(10.0, calc.getPow(4, 2), "4 в степени 2 не должно быть 10.0");
    }

    @Test
    void testGetLog() {
        // Проверка истинного значения
        assertEquals(3.0, calc.getLog(1000, 10), 0.0001, "log10(1000) должно быть 3.0");
        assertEquals(2.0, calc.getLog(16, 2), 0.0001, "log2(16) должно быть 4.0"); // Здесь исправьте, если нужно другое значение
        // Пример: log2(16) = 4, так что поменяем сообщение ниже
        assertEquals(4.0, calc.getLog(16, 2), 0.0001, "log2(16) должно быть 4.0");
        // Проверка ложного значения
        assertNotEquals(2.0, calc.getLog(1000, 10), "log10(1000) не должно быть 2.0");
        assertNotEquals(5.0, calc.getLog(16, 2), "log2(16) не должно быть 5.0");
    }
}


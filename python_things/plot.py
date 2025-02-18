import matplotlib.pyplot as plt
import numpy as np

# Задаем коэффициенты для прямых вида: y = kx + b
k1 = float(input("Введите угловой коэффициент k1 для первой прямой: "))
b1 = float(input("Введите свободный член b1 для первой прямой: "))

k2 = float(input("Введите угловой коэффициент k2 для второй прямой: "))
b2 = float(input("Введите свободный член b2 для второй прямой: "))

# Находим точку пересечения
if k1 == k2:
    print("Прямые параллельны и не пересекаются.")
    intersection = None
else:
    x_intersection = (b2 - b1) / (k1 - k2)
    y_intersection = k1 * x_intersection + b1
    intersection = (x_intersection, y_intersection)
    print(f"Точка пересечения: x = {x_intersection:.2f}, y = {y_intersection:.2f}")

# Создаем область значений для X
x = np.linspace(-10, 10, 1000)
y1 = k1 * x + b1
y2 = k2 * x + b2

# Строим график
plt.figure(figsize=(8, 6))
plt.plot(x, y1, label=f'PA_b1 = {k1}x1 + {b1}', color='blue')
plt.plot(x, y2, label=f'PA_b2 = {k2}x1 + {b2}', color='green')

# Отмечаем точку пересечения
if intersection:
    plt.scatter(*intersection, color='red', s=100, label=f'Пересечение ({intersection[0]:.2f}, {intersection[1]:.2f})')

# Добавляем оформление
plt.xlabel(' ')
plt.ylabel(' ')
plt.axhline(0, color='black', linewidth=0.7)
plt.axvline(0, color='black', linewidth=0.7)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.title('Пересечение двух прямых')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# Определение ограничений
x = np.linspace(-2, 12, 100)
y1 = (1 - 4*x) / 6  # Прямая 4u1 + 6u2 = 1
y2 = (1 - 5*x) / 3  # Прямая 5u1 + 3u2 = 1
# y1 = (1 - 4*x) / 5  
# y2 = (1 - 6*x) / 3  


# Граничные точки многоугольника решений
vertices = np.array([
    [0, 1/3],  # Пересечение оси u2
    [1/4, 0],  # Пересечение оси u1
    [1/6, 1/18],  # Пересечение двух прямых
    # [0, 1/5],  
    # [1/4, 0], 
    # [1/9, 1/9],  # Пересечение двух прямых
    # [0, 0]
])

# Построение графика
plt.figure(figsize=(8, 6))
plt.plot(x, y1, 'r-', label=r'$4u_1 + 6u_2 = 1$')
plt.plot(x, y2, 'b-', label=r'$5u_1 + 3u_2 = 1$')
# plt.plot(x, y1, 'r-', label=r'$4v_1 + 5v_2 = 1$')
# plt.plot(x, y2, 'b-', label=r'$6v_1 + 3v_2 = 1$')


# Отображение точек пересечения и подписи
labels = ['B', 'D', 'C', 'A']
for (vx, vy), label in zip(vertices, labels):
    plt.plot(vx, vy, 'ko')
    plt.text(vx, vy, f'{label}({vx:.2f}, {vy:.2f})', fontsize=12, verticalalignment='bottom', horizontalalignment='right')

# Линия уровня целевой функции u1 + u2 = 0
x_level = np.linspace(-2, 4, 100)
y_level = -x_level  # Линия уровня для u1 + u2 = 0
plt.plot(x_level, y_level, 'g--', label='Линия уровня')

# Градиент
plt.arrow(0, 0, 0.04, 0.04, head_width=0.01, head_length=0.01, fc='green', ec='green', label='Градиент')

# Подписи
plt.xlim(-0.1, 0.4)
plt.ylim(-0.1, 0.4)
plt.xlabel('$u_1$')
plt.ylabel('$u_2$')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.legend()
plt.title('Графическое решение задачи ЛП')
plt.grid()
plt.show()
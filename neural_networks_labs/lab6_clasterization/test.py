import numpy as np
import matplotlib.pyplot as plt

# Координаты 26 поликлиник (примерные)
clinics = np.array([
    [37.6, 55.7], [37.5, 55.8], [37.7, 55.6], [37.4, 55.9], [37.3, 55.7], 
    [37.8, 55.6], [37.9, 55.8], [37.2, 55.7], [37.5, 55.5], [37.1, 55.6],
    [37.6, 55.5], [37.3, 55.6], [37.4, 55.8], [37.2, 55.8], [37.7, 55.7],
    [37.9, 55.9], [37.8, 55.7], [37.1, 55.5], [37.3, 55.5], [37.4, 55.5],
    [37.7, 55.5], [37.2, 55.6], [37.6, 55.8], [37.5, 55.6], [37.8, 55.9], 
    [37.9, 55.6]
])

# Координаты 12 округов Москвы (центры кластеров)
districts = np.array([
    [37.6, 55.75], [37.4, 55.85], [37.7, 55.65], [37.5, 55.7], [37.3, 55.75],
    [37.8, 55.65], [37.9, 55.8], [37.2, 55.7], [37.5, 55.55], [37.1, 55.6],
    [37.6, 55.55], [37.3, 55.6]
])

# Инициализация весов округов (начальные координаты округов)
weights = np.copy(districts)

# Функция Евклидова расстояния
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((np.array(p1) - np.array(p2))**2))

# Функция для нормализации вектора
def normalize(vector):
    norm = np.linalg.norm(vector)
    return vector / norm if norm != 0 else vector

# Обучение сети Кохонена
num_epochs = 100  # Количество эпох
learning_rate = 0.1  # Скорость обучения

for epoch in range(num_epochs):
    lr = learning_rate * (1 - epoch / num_epochs)  # Уменьшение скорости обучения

    for clinic in clinics:
        # Нормализация входных данных
        input_vector = normalize(clinic)

        # Вычисляем расстояние от поликлиники до каждого округа
        distances = np.array([euclidean_distance(input_vector, w) for w in weights])

        # Побеждает ближайший округ
        winner = np.argmin(distances)

        # Обновляем вес победившего округа
        weights[winner] += lr * (input_vector - weights[winner])

# Присваивание поликлиник к округам
assignments = []
for clinic in clinics:
    distances = np.array([euclidean_distance(clinic, w) for w in weights])
    winner = np.argmin(distances)
    assignments.append(winner)


for c in weights:
    print(c)


# Вывод результатов
for i, clinic in enumerate(clinics):
    print(f"Поликлиника {i+1} ({clinic[0]}, {clinic[1]}) -> Округ {assignments[i] + 1} ")


# Визуализация поликлиник и округов
plt.figure(figsize=(10, 8))

# Отображаем поликлиники
plt.scatter(clinics[:, 0], clinics[:, 1], c='blue', label='Поликлиники', marker='o')

# Отображаем округи (центры кластеров)
plt.scatter(districts[:, 0], districts[:, 1], c='red', label='Округа', marker='x')

# Отображаем связи между поликлиниками и округами
for i, clinic in enumerate(clinics):
    winner = assignments[i]
    plt.plot([clinic[0], districts[winner, 0]], [clinic[1], districts[winner, 1]], 'gray', linestyle='--')

# Настройки графика
plt.title("Распределение поликлиник по округам Москвы")
plt.xlabel("Долгота")
plt.ylabel("Широта")
plt.legend()
plt.grid(True)
plt.show()

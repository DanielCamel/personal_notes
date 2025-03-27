import numpy as np
import matplotlib.pyplot as plt
import itertools

# 1) Определение булевой функции
def boolean_function(x1, x2, x3, x4):
    """
    (x1 or x2 or x3) AND (x2 or x3 or x4)
    """
    part1 = (x1 or x2 or x3)
    part2 = (x2 or x3 or x4)
    return 1 if (part1 and part2) else 0

# 2) Полный набор (16 векторов)
X_list = []
y_list = []
for x1 in [0, 1]:
    for x2 in [0, 1]:
        for x3 in [0, 1]:
            for x4 in [0, 1]:
                X_list.append([x1, x2, x3, x4])
                y_list.append(boolean_function(x1, x2, x3, x4))

X_full = np.array(X_list, dtype=float)  # (16,4)
y_full = np.array(y_list, dtype=float)  # (16,)

# 3) Пример подмножества из 5 векторов
X_sub = np.array([
    [0, 0, 0, 1],  # BF=0
    [0, 0, 1, 0],  # BF=1
    [0, 1, 0, 1],  # BF=1
    [1, 0, 0, 0],  # BF=0
    [1, 0, 0, 1],  # BF=1

], dtype=float)
y_sub = np.array([0, 1, 1, 0, 1], dtype=float)

# 4) Три центра (все векторы с BF=0) из полного набора
X0_full = X_full[y_full == 0]
centers_3 = X0_full.copy()  # 3 центра

# 5) RBF-функция (exp(-||x-c||^2))
def rbf_gaussian(x, center):
    dist = np.linalg.norm(x - center)
    return np.exp(- dist**2)

# 6) Функция обучения (Widrow–Hoff) с подсчётом хэмминговой ошибки
def train_rbf_widrow_hoff_hamming_verbose_eval(
    X_train, y_train,         # обучающая выборка
    X_eval,  y_eval,          # выборка для оценки (eval)
    centers,                  # RBF-центры
    learning_rate=0.3, 
    max_epochs=100, 
    print_table=True
):
    """
    Онлайн-обучение Widrow-Hoff с обновлением весов для обучающих примеров.
    После каждой эпохи считается хэмминговая ошибка на eval-наборе.
    
    Возвращает:
      table_data: список кортежей (эпоха, вектор весов, выходной вектор (eval), ошибка)
      (w, b): итоговые веса и смещение
      hamming_by_epoch: список хэмминговых ошибок по эпохам
    """
    N_train = X_train.shape[0]
    M = centers.shape[0]

    # Инициализация весов и смещения
    w = np.zeros(M)
    b = 0.0

    table_data = []
    hamming_by_epoch = []

    for epoch in range(max_epochs):
        weights = np.copy(w)
        # Обновление весов (онлайн)
        for i in range(N_train):
            phi_i = np.array([rbf_gaussian(X_train[i], centers[j]) for j in range(M)])
            net_i = np.dot(w, phi_i) + b
            e_i = y_train[i] - net_i
            w += learning_rate * e_i * phi_i
            b += learning_rate * e_i

        # Оценка на eval-наборе
        out_vector_eval = []
        hamming_error_eval = 0
        for i in range(X_eval.shape[0]):
            phi_i = np.array([rbf_gaussian(X_eval[i], centers[j]) for j in range(M)])
            net_i = np.dot(w, phi_i) + b
            y_pred = 1 if net_i >= 0 else 0
            out_vector_eval.append(y_pred)
            if y_pred != y_eval[i]:
                hamming_error_eval += 1
        hamming_by_epoch.append(hamming_error_eval)

        # Сохраняем данные в table_data
        table_data.append((epoch+1, weights, out_vector_eval[:], hamming_error_eval))

        # Если ошибка обнулилась — завершаем обучение
        if hamming_error_eval == 0:
            break

    if print_table:
        print("=== Таблица обучения ===")
        print(" Эпоха | Вектор весов              | Выходной вектор          | Ошибка")
        for (ep, w_vec, out_vec, err) in table_data:
            w_rounded = [round(float(v), 3) for v in w_vec]
            out_str = [str(int(o)) for o in out_vec]
            print(f" {ep:<5} | {w_rounded} | {out_str} | {err}")
        print()

    return table_data, w, b, hamming_by_epoch

# 7) Функция для классификации (порог 0)
def rbf_predict_classes(X, centers, w, b):
    N = X.shape[0]
    M = centers.shape[0]
    y_pred = np.zeros(N)
    for i in range(N):
        phi_i = np.array([rbf_gaussian(X[i], centers[j]) for j in range(M)])
        net_i = np.dot(w, phi_i) + b
        y_pred[i] = 1 if net_i >= 0 else 0
    return y_pred

# 8) Функция для поиска минимальной обучающей выборки
def find_minimal_training_set(X_full, y_full, centers, learning_rate=0.3, max_epochs=150):
    """
    Перебирает все подмножества обучающих примеров и возвращает первое (минимальное по размеру), для которого после обучения (до max_epochs) достигается 0 хэмминговая ошибка на полном наборе.
    
    Возвращает:
      indices: индексы выбранных обучающих примеров из полного набора
      X_train_subset: соответствующий массив обучающих примеров
      y_train_subset: соответствующий массив меток
      w, b: итоговые веса и смещение после обучения
      epochs_to_zero: номер эпохи, на которой впервые достигнута 0 ошибка
      hamming_history: список хэмминговых ошибок по эпохам
      table_data_min: сама «таблица» (эпоха, w, выход, ошибка) для найденного подмножества
    Если подходящий набор не найден, возвращается None для всех.
    """
    n = X_full.shape[0]
    for r in range(1, n+1):
        for indices_tuple in itertools.combinations(range(n), r):
            indices = list(indices_tuple)
            X_train_subset = X_full[indices]
            y_train_subset = y_full[indices]
            # Вызываем обучение без печати таблицы, чтобы не засорять вывод
            table_data, w, b, hamming_history = train_rbf_widrow_hoff_hamming_verbose_eval(
                X_train=X_train_subset,
                y_train=y_train_subset,
                X_eval=X_full,
                y_eval=y_full,
                centers=centers,
                learning_rate=learning_rate,
                max_epochs=max_epochs,
                print_table=False
            )
            if hamming_history[-1] == 0:  # значит последняя ошибка == 0
                # Ищем эпоху, на которой впервые ошибка стала 0
                epochs_to_zero = None
                for (ep, _, _, err) in table_data:
                    if err == 0:
                        epochs_to_zero = ep
                        break
                # Возвращаем всё, что нужно
                return indices, X_train_subset, y_train_subset, w, b, epochs_to_zero, hamming_history, table_data

    # Если не нашли
    return None, None, None, None, None, None, None, None

# 9) Основной блок
if __name__ == "__main__":

    # (A) ОБУЧЕНИЕ НА ПОЛНОМ НАБОРЕ (16 векторов), eval = тот же набор
    print("=== (A) Обучение на ПОЛНОМ наборе (16 векторов) ===")
    print("Центры:")
    for c in centers_3:
        print(" ", c)
    print()

    table_data_full, w_full, b_full, hamming_hist_full = train_rbf_widrow_hoff_hamming_verbose_eval(
        X_train=X_full, y_train=y_full,
        X_eval=X_full, y_eval=y_full,
        centers=centers_3,
        learning_rate=0.3,
        max_epochs=100,
        print_table=True
    )

    # Если последняя ошибка = 0, печатаем итоговые коэффициенты
    if hamming_hist_full[-1] == 0:
        w_final_rounded = [round(float(val), 3) for val in w_full]
        b_final_rounded = round(float(b_full), 3)
        print(f"Итоговые коэффициенты: w = {w_final_rounded}, b = {b_final_rounded}\n")

    plt.figure(figsize=(6,4))
    plt.plot(range(1, len(hamming_hist_full)+1), hamming_hist_full, marker='o')
    plt.title("RBF — Полный набор")
    plt.xlabel("Эпоха")
    plt.ylabel("Ошибка")
    plt.grid(True)
    plt.show()

    y_pred_full = rbf_predict_classes(X_full, centers_3, w_full, b_full)
    total_err_full = int(np.sum(np.abs(y_full - y_pred_full)))
    print(f"Итоговая ошибка = {total_err_full}/{len(X_full)}\n")

    # (B) ОБУЧЕНИЕ НА ПОДМНОЖЕСТВЕ (5 векторов)
    print("=== (B) Обучение на подмножестве (5 векторов) ===")
    print("Подмножество:")
    for x_i, y_i in zip(X_sub, y_sub):
        print(f"  {x_i} -> {y_i}")
    #print("\n(Используем те же 3 центра)")

    table_data_sub, w_sub, b_sub, hamming_hist_sub = train_rbf_widrow_hoff_hamming_verbose_eval(
        X_train=X_sub, y_train=y_sub,
        X_eval=X_full, y_eval=y_full,
        centers=centers_3,
        learning_rate=0.3,
        max_epochs=100,
        print_table=True
    )

    # Если последняя ошибка = 0, печатаем итоговые коэффициенты
    if hamming_hist_sub[-1] == 0:
        w_sub_rounded = [round(float(val), 3) for val in w_sub]
        b_sub_rounded = round(float(b_sub), 3)
        print(f"Итоговые коэффициенты: w = {w_sub_rounded}, b = {b_sub_rounded}\n")

    plt.figure(figsize=(6,4))
    plt.plot(range(1, len(hamming_hist_sub)+1), hamming_hist_sub, marker='o', color='orange')
    plt.title("RBF — Подмножество (5 векторов)")
    plt.xlabel("Эпоха")
    plt.ylabel("Ошибка")
    plt.grid(True)
    plt.show()

    y_pred_sub_full = rbf_predict_classes(X_full, centers_3, w_sub, b_sub)
    total_err_sub_full = int(np.sum(np.abs(y_full - y_pred_sub_full)))
    print(f"Итоговая ошибка (подмножество) = {total_err_sub_full}/{len(X_full)}\n")

    print("Таблица классификации (после обучения на 5, предъявляем 16):")
    for i in range(len(X_full)):
        print(f"  X = {X_full[i]}, y_ист = {int(y_full[i])}, y_пред = {int(y_pred_sub_full[i])}")

    # (C) ПОИСК МИНИМАЛЬНОЙ ОБУЧАЮЩЕЙ ВЫБОРКИ + ПЕЧАТЬ ТАБЛИЦЫ
    print("\n=== (C) Поиск минимальной обучающей выборки ===")
    (indices, X_min, y_min, w_min, b_min, epochs_to_zero,
     hamming_history_min, table_data_min) = find_minimal_training_set(
         X_full, y_full, centers_3, learning_rate=0.3, max_epochs=150
     )

    if indices is not None:
        print(f"Найдено минимальное подмножество (размер = {len(indices)}) с нулевой ошибкой на полном наборе.")
        print(f"Индексы обучающих векторов: {indices}")
        print("Сами векторы и их метки:")
        for x, y in zip(X_min, y_min):
            print(f"  {x} -> {y}")
        print(f"\nОбучение достигло 0 ошибки на {epochs_to_zero}-й эпохе.")

        # --- Выводим таблицу обучения для минимальной выборки ---
        print("\n=== Таблица обучения для минимальной выборки ===")
        print(" Эпоха | Вектор весов              | Выходной вектор         | Ошибка")
        for (ep, w_vec, out_vec, err) in table_data_min:
            w_rounded = [round(float(v), 3) for v in w_vec]
            out_str = [str(int(o)) for o in out_vec]
            print(f" {ep:<5} | {w_rounded} | {out_str} | {err}")
        print()

        # Печатаем итоговые коэффициенты (при ошибке=0)
        w_min_rounded = [round(float(val), 3) for val in w_min]
        b_min_rounded = round(float(b_min), 3)
        print(f"Итоговые коэффициенты: w = {w_min_rounded}, b = {b_min_rounded}\n")

        # --- Строим график ошибки ---
        plt.figure(figsize=(6,4))
        plt.plot(range(1, len(hamming_history_min)+1), hamming_history_min, marker='o', color='green')
        plt.title("RBF — Минимальная обучающая выборка")
        plt.xlabel("Эпоха")
        plt.ylabel("Ошибка")
        plt.grid(True)
        plt.show()

        # --- Проверка классификации на всём наборе ---
        y_pred_min = rbf_predict_classes(X_full, centers_3, w_min, b_min)
        total_err_min = int(np.sum(np.abs(y_full - y_pred_min)))
        print(f"Итоговая ошибка (минимальная выборка → полный набор) = {total_err_min}/{len(X_full)}")
    else:
        print("Не удалось найти подмножество, дающее 0 ошибку в пределах 150 эпох обучения.")

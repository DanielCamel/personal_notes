import numpy as np

class BiMatrix:
    def __init__(self, rows, columns, game_type=None):
        """
        Инициализация биматричной игры.
        :param rows: количество строк (стратегий игрока 1)
        :param columns: количество столбцов (стратегий игрока 2)
        :param game_type: тип игры (ordinar, crossroad, prisoner, family)
        """
        self.row = rows
        self.col = columns
        self.game_type = game_type

        # Генерация случайной игры или задание фиксированных матриц
        if game_type == "ordinar":
            self.matrix_A = np.random.randint(-29, 29, size=(rows, columns))
            self.matrix_B = np.random.randint(-29, 29, size=(rows, columns))

        elif game_type == "crossroad":
            self.matrix_A = np.array([[1, 0.7], [2, 0]])
            self.matrix_B = np.array([[1, 2], [0.5, 0]])

        elif game_type == "prisoner":
            self.matrix_A = np.array([[-5, 0], [-10, -1]])
            self.matrix_B = np.array([[-5, -10], [0, -1]])

        elif game_type == "family":
            self.matrix_A = np.array([[4, 0], [0, 1]])
            self.matrix_B = np.array([[1, 0], [0, 4]])

        elif game_type == "my_bimatrix":
            # Задаем значения для биматричной игры
            self.matrix_A = np.array([[5, 10], [8, 6]])  # Платежная матрица первого игрока
            self.matrix_B = np.array([[1, 4], [6, 9]])   # Платежная матрица второго игрока   

    def check_strictly_dominant(self, a, b):
        """
        Находит строго доминирующие стратегии для обоих игроков.
        """
        strictly_dominant_a = set()  # Доминирующие стратегии игрока 1 (строки)
        strictly_dominant_b = set()  # Доминирующие стратегии игрока 2 (столбцы)

        # Проверка доминирующих стратегий для первого игрока (строки)
        for i in range(a.shape[0]):
            for k in range(a.shape[0]):
                if i != k and all(a[i, j] > a[k, j] for j in range(a.shape[1])):
                    strictly_dominant_a.add(i)

        # Проверка доминирующих стратегий для второго игрока (столбцы)
        b_T = b.T  # Транспонируем, чтобы проверять по столбцам
        for j in range(b_T.shape[0]):
            for k in range(b_T.shape[0]):
                if j != k and all(b_T[j, i] > b_T[k, i] for i in range(b_T.shape[1])):
                    strictly_dominant_b.add(j)

        return strictly_dominant_a, strictly_dominant_b
    
    def nash(self, a, b, show = True):
        """
        Находит ситуации равновесия по Нэшу с учетом исправленного определения.
        """

        rows, cols = a.shape
        nash_equilibria = []  # Список для хранения равновесий по Нэшу

        for i in range(rows):
            for j in range(cols):
                payoff_a = a[i, j]
                payoff_b = b[i, j]

                # Проверяем, является ли (i, j) наилучшим ответом игрока A
                best_responses_a = [a[ii, j] for ii in range(rows)]
                if best_responses_a.count(payoff_a) > 1:
                    continue  # Если повторяется, не рассматриваем

                if payoff_a != max(best_responses_a):
                    continue  # Не является наилучшим ответом A

                # Проверяем, является ли (i, j) наилучшим ответом игрока B
                best_responses_b = [b[i, jj] for jj in range(cols)]
                if best_responses_b.count(payoff_b) > 1:
                    continue  # Если повторяется, не рассматриваем

                if payoff_b != max(best_responses_b):
                    continue  # Не является наилучшим ответом B

                # Если оба условия выполняются, добавляем стратегию в список равновесий по Нэшу
                nash_equilibria.append((i, j))

        # Выводим результат
        
        if show:
            if nash_equilibria:
                print("\nСитуации равновесия по Нэшу:")
                for eq in nash_equilibria:
                    print(f"({a[eq]}, {b[eq]})")
            else:
                print("\nРавновесие по Нэшу отсутствует")

        return nash_equilibria

    def pareto(self, a, b, show = True):
        """Находит Парето-оптимальные ситуации и возвращает их в виде списка выигрышей."""
        rows, cols = a.shape
        all_pairs = [(i, j, float(a[i, j]), float(b[i, j])) for i in range(rows) for j in range(cols)]
        pareto_optimal = []  # Список Парето-оптимальных ситуаций

        for (i1, j1, ai, bi) in all_pairs:
            is_pareto_optimal = True
            for (i2, j2, ak, bk) in all_pairs:
                if (ak > ai and bk >= bi) or (ak >= ai and bk > bi):  # Улучшение хотя бы по одному критерию
                    is_pareto_optimal = False
                    break

            if is_pareto_optimal:
                pareto_optimal.append((ai, bi))  # Сохраняем выигрыши
        if show:
            print(f"\nОптимальные по Парето выигрыши: {pareto_optimal}")
        
        # Возвращаем список индексов Парето-оптимальных ситуаций для подсветки
        return [(i, j) for (i, j, _, _) in all_pairs if (float(a[i, j]), float(b[i, j])) in pareto_optimal]

    def mixed_nash(self, a, b):
        """
        Вполне смешанная ситуация равновесия по Нэшу

        :param a: стратегии первого игрока
        :param b: стратегии второго игрока
        """
        try:
            A_inv = np.linalg.inv(a)  # Обратная матрица A
            B_inv = np.linalg.inv(b)  # Обратная матрица B
        except np.linalg.LinAlgError:
            print("Матрицы не являются невырожденными, смешанное равновесие не определено")
            return

        u = np.ones((self.row, 1))  # Вектор из единиц

        # Вычисляем коэффициенты v1 и v2
        v1 = 1 / (u.T @ A_inv @ u)
        v2 = 1 / (u.T @ B_inv @ u)
        
        # Вычисляем стратегии x и y для вполне смешанной ситуации равновесия
        x = (v2 * (u.T @ B_inv)).flatten() # flatten() -> одномерный массив
        y = (v1 * (A_inv @ u)).flatten()

        print("Смешанное равновесие по Нэшу:")
        print(f"Вероятности первого игрока: {np.array2string(np.round(x, 3), precision=3, floatmode='fixed')}")
        print(f"Вероятности второго игрока: {np.array2string(np.round(y, 3), precision=3, floatmode='fixed')}")
        print(f"Равновесные выигрыши: v1 = {np.round(v1,3).item():.3f}, v2 = {np.round(v2, 3).item():.3f}")


    def generate_game(self):
        """Вывод информации об игре: платежная матрица, равновесие по Нэшу, оптимальные по Парето стратегии."""
        a, b = self.matrix_A, self.matrix_B
        self.bimatrix_output(a, b)

        if self.game_type == "ordinar":
            # Рассчитываем равновесие по Нэшу
            self.nash(a, b) 
        else:               
            # Проверяем наличие строго доминирующих стратегий
            strictly_dominant_a, strictly_dominant_b = self.check_strictly_dominant(a, b)

            if (strictly_dominant_a or strictly_dominant_b) and (len(self.nash(a,b)) != 0):
                print("Обнаружены строго доминирующие стратегии. Игра имеет единственное равновесие по Нэшу.")
                # Рассчитываем равновесие для доминирующей стратегии
                self.nash(a, b)
            else:
                # Сначала проверяем равновесие по Нэшу для чистых стратегий
                nash_eq = self.nash(a, b)

                if not nash_eq:
                    print("\nРавновесие по Нэшу для чистых стратегий не найдено. Рассчитываем смешанное равновесие.")
                    self.mixed_nash(a, b)
                if len(nash_eq) == 2:
                    print("\nИгра имеет 2 равновесные по Нэшу ситуации \nРассчитываем вполне смешанное равноверсие в смешанном дополнении игры: ")
                    self.mixed_nash(a, b)

        # Оптимальные по Парето стратегии
        self.pareto(a, b)
        

    def bimatrix_output(self, a, b):
        """Выводит платежную матрицу с подсветкой равновесных стратегий и Парето-оптимальных точек."""
        
        nash_eq = set(self.nash(a, b, show = False))  # Используем множество для быстрого поиска
        pareto_opt = set(self.pareto(a, b, show = False))
        
        # Определяем заголовок в зависимости от типа игры
        game_titles = {
            "prisoner": "Дилемма заключённого",
            "family": "Семейный спор",
            "crossroad": "Перекрёсток",
            "ordinar": "Биматричная игра (10 x 10)"
        }
        title = game_titles.get(self.game_type, "Биматричная игра")

        print(f"\n{title}:")

        for i in range(self.row):
            row_str = ""
            for j in range(self.col):
                cell = f"({a[i, j]:>4}, {b[i, j]:>4})"

                if (i, j) in nash_eq and (i, j) in pareto_opt:
                    cell = f"\033[95m{cell}\033[0m"  # Фиолетовый (совпадение Нэша и Парето)
                elif (i, j) in nash_eq:
                    cell = f"\033[94m{cell}\033[0m"  # Синий (Нэш)
                elif (i, j) in pareto_opt:
                    cell = f"\033[91m{cell}\033[0m"  # Красный (Парето)

                row_str += cell + "  "
            print(row_str)
            

# Основная программа
obj = BiMatrix(10, 10, "ordinar")
obj.generate_game()

game = BiMatrix(2, 2, "prisoner")
game.generate_game()

game = BiMatrix(2, 2, "family")
game.generate_game()

game = BiMatrix(2, 2, "crossroad")
game.generate_game()

game = BiMatrix(2, 2, "my_bimatrix")
game.generate_game()
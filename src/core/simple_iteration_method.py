from math import sqrt

from utils.output_rich import Rich


class SimpleIterationMethod:
    """
    Класс для расчётов методом простой итерации
    """
    # Задания - первая таблица - вариант 3, вторая - вариант 4
    # Метод простой итерации
    # Метод касательных (Ньютона)
    def __init__(self):
        # необходимая точность приближённого решения
        self.accuracy = 0.001
        # количество итераций для поиска приближённого решения
        self.max_iter = 10
        self.t = 1
        # массив со всеми полученными промежуточными (и искомым) приближёнными решениями
        self.list_iterations = []
        # максимальное значение модуля производной на этом отрезке
        self.max_q = 0

    def run(self, a: float, b: float) -> float:
        """
        Метод для запуска процесса поиска решения
        трансцендентного уравнения методом простой итерации

        :param a: Левая граница отрезка
        :param b: Правая граница отрезка

        :return: float - приближённое решение тангенциального уравнения
         методом простых итераций
        """

        Rich.simple_log("Запуск метода простой итерации")
        Rich.print_spacer()
        Rich.simple_log(f"f(x) = 1/(1 + x**4) - {self.t}*x**2")
        Rich.simple_log(f"g(x) = 1 / sqrt({self.t} * (1 + x**4))")
        Rich.debug_log(f"Отрезок: [{a:.3f}, {b:.3f}], e = {self.accuracy}")
        Rich.print_spacer()

        # проверка сходимости
        self.check_convergence(a, b)

        # x0 = середина отрезка - любой x, определяемый как начальное приближение
        x0 = (a + b) / 2
        Rich.debug_log(f"Выберем произвольную точку х0, которую примем за грубое приближение корня: x0 = {x0:.6f}")
        Rich.debug_log("подставим x0 в правую часть уравнения х = g(x)")

        # итерации
        self.list_iterations = [x0]

        Rich.debug_log("Тогда получим некоторое число х1 = g(x0)")

        x_prev = x0
        # Проход по итерациям
        for iteration in range(1, self.max_iter + 1):
            x_next = self.g(x_prev)
            Rich.debug_log(f"x{len(self.list_iterations)}: {x_next:.6f}")

            self.list_iterations.append(x_next)
            delta = abs(x_next - x_prev)
            # промежуточное значение функции для текущего приближённого значения
            residual = abs(self.func(x_next))

            Rich.debug_log(
                f"итерация №{iteration}: x{len(self.list_iterations) - 1} = {x_next:.6f}, "
                f"|дельта x| = {delta:.6f}, |f(x)| = {residual:.6f}"
            )

            # Проверка на достаточную точность приближённого решения и дельты
            # (разницы между двумя последними прибл. реш.)
            if delta < self.accuracy and (abs(x_next - x_prev) <= (1 - self.max_q)/self.max_q*self.accuracy):
                Rich.print_spacer()
                Rich.success_log(
                    f"Сошлось за {iteration} итераций. Приближённое решение X* = {x_next:.6f}, q = {self.max_q:.6f}"
                )
                return x_next

            else:
                Rich.debug_log(f"По найденному значению х{len(self.list_iterations) - 1} "
                               f"определим точку х{len(self.list_iterations)}")
                Rich.print_spacer_points()

            x_prev = x_next

        Rich.warning_log(f"После выполнения доступного количества итераций, "
                         f"приближённое решение необходимой точности не нашлось. x = {x_prev:.6f}")
        return x_prev


    def func(self, x: float) -> float:
        """
        Функция, вычисляющая значение функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение функции f в точке икс
        """

        return 1 / (1 + x ** 4) - x ** 2


    def g(self, x: float) -> float:
        """
        Функция, вычисляющая значение функции g(x) в точке икс
        :param x: принимает значение переменной икс
        :return: значение функции g в точке икс
        """

        return 1 / sqrt(1 + x ** 4)


    def dg(self, x: float) -> float:
        """
        Функция, вычисляющая значение производной функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение производной функции f в точке икс
        """

        return -2 * x ** 3 / ((1 + x ** 4) ** 1.5)


    def check_convergence(self, a: float, b: float, points: int = 20) -> bool:
        """
        Функция для проверки на сходимость метода
        :param a: левая граница отрезка с единственным корнем
        :param b: правая граница отрезка с единственным корнем
        :param points: количество точек, в которых будет находиться и сверяться с 1 значение q
        :return: bool - True, если метод сходится
        """

        Rich.simple_log("Проверка сходимости метода простой итерации")
        max_q, worst_x = 0.0, a
        for i in range(points + 1):
            x = a + (b - a) * i / points
            q = abs(self.dg(x))
            if q > max_q:
                max_q, worst_x = q, x
                self.max_q = q

        Rich.debug_log(f"max |g'(x)| = {max_q:.6f} в точке x = {worst_x:.4f}")
        if max_q < 1:
            Rich.success_log(f"Метод сходится: q = {max_q:.4f} < 1")
            return True
        Rich.warning_log(f"Метод может расходиться: q = {max_q:.4f} ≥ 1")
        return False


simpleIterationMethod = SimpleIterationMethod()

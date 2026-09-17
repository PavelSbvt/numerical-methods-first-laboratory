from math import sqrt

import matplotlib.pyplot as plt

from utils.output_rich import Rich


class SimpleIterationMethod:
    """
    Класс для расчётов методом простой итерации
    """
    # Задания - первая таблица - вариант 3, вторая - вариант 4
    # Метод простой итерации
    # Метод касательных (Ньютона)
    def __init__(self):
        self.accuracy = 0.001
        self.max_iter = 10
        self.t = 1
        self.list_iterations = []

    def run(self, a: float, b: float) -> None:
        """
        Метод для запуска процесса поиска решения
        трансцендентного уравнения методом простой итерации

        :param a: Левая граница отрезка
        :param b: Правая граница отрезка

        :return: None
        """

        Rich.print_spacer()
        Rich.simple_log("Запуск метода простой итерации")
        Rich.simple_log(f"f(x) = 1/(1 + x**4) - {self.t}*x**2")
        Rich.simple_log(f"g(x) = 1 / sqrt({self.t} * (1 + x**4))")
        Rich.debug_log(f"Отрезок: [{a:.3f}, {b:.3f}], e = {self.accuracy}")
        Rich.print_spacer()

        # проверка сходимости
        self.check_convergence(a, b)

        # x0 = середина отрезка
        x0 = (a + b) / 2
        Rich.debug_log(f"x0 = {x0:.6f}")

        # итерации
        self.list_iterations = [x0]
        x_prev = x0
        for iteration in range(1, self.max_iter + 1):
            x_next = self.g(x_prev)
            self.list_iterations.append(x_next)
            delta = abs(x_next - x_prev)
            residual = abs(self.f(x_next))

            Rich.debug_log(
                f"итерация {iteration:>3}: x = {x_next:.6f}, "
                f"|дельта x| = {delta:.6f}, |f(x)| = {residual:.6f}"
            )

            if delta < self.accuracy and residual < self.accuracy:
                Rich.print_spacer()
                Rich.success_log(
                    f"Сошлось за {iteration} итераций. Корень x ≈ {x_next:.6f}"
                )
                return x_next

            x_prev = x_next

        Rich.warning_log(f"После выполнения доступного количества итераций, "
                         f"приближённое решение необходимой1 точности не нашлось. x = {x_prev:.6f}")
        return x_prev

    def f(self, x: float) -> float:
        return 1 / (1 + x ** 4) - x ** 2

    def g(self, x: float) -> float:
        return 1 / sqrt(1 + x ** 4)

    def dg(self, x: float) -> float:
        return -2 * x ** 3 / ((1 + x ** 4) ** 1.5)

    def check_convergence(self, a: float, b: float, points: int = 20) -> bool:
        Rich.simple_log("Проверка сходимости метода простой итерации")
        max_q, worst_x = 0.0, a
        for i in range(points + 1):
            x = a + (b - a) * i / points
            q = abs(self.dg(x))
            if q > max_q:
                max_q, worst_x = q, x

        Rich.debug_log(f"max |g'(x)| = {max_q:.6f} в точке x = {worst_x:.4f}")
        if max_q < 1:
            Rich.success_log(f"Метод сходится: q = {max_q:.4f} < 1")
            return True
        Rich.warning_log(f"Метод может расходиться: q = {max_q:.4f} ≥ 1")
        return False


simpleIterationMethod = SimpleIterationMethod()

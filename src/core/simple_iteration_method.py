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
        pass

    def run(self) -> None:
        """
        Метод для запуска процесса поиска решения
        трансцендентного уравнения методом простой итерации

        :return: None
        """
        Rich.simple_log("Запуск метода простой итерации")

        # Максимально допустимая погрешность расчёта - точность
        accuracy = 0.001

        num_x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # g(x) = x + f(x).
        # функция g(x) определена и дифференцируема на
        # отрезке num_x[0, 10], причём все её значения  g(x) ∈ num_x[0, 10]
        Rich.print_spacer()
        Rich.simple_log(f"g(x) = sqrt(1/(1 + x**4))")
        Rich.debug_log(f"Вычисление значений g(x)∈[{str(min(num_x))},{str(max(num_x))}]")
        Rich.print_spacer()
        for x in num_x:
            g = sqrt(1/(1 + x**4))
            Rich.debug_log(f"g({x}) = {g}")
        Rich.print_spacer()



simple_iteration_method = SimpleIterationMethod()

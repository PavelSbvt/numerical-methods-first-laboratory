from typing import Optional

from utils.output_rich import Rich


def func(x: float, t: int) -> float:
    """
    Функция для вычисления значений f(x, t).

    :param x: Принимает подставляемое значение x
    :param t: Заданное значение

    :return: float - результат вычислений функции от данного x
    """

    return 1 / (1 + x**4) - t * x**2


def derivative_func(x: float, t: int) -> float:
    """
    Производная f'(x, t) = -4x^3 / (1 + x^4)^2 - 2t * x.
    Нужна для проверки единственности корня.

    :param x: Принимает подставляемое значение x
    :param t: Заданное значение

    :return: float - результат вычислений производной функции от данного x
    """
    return -4 * x ** 3 / (1 + x ** 4) ** 2 - 2 * t * x


def checking_uniqueness(t: int, a: float, b: float, points: int = 10) -> bool:
    """
    Проверяет, что f'(x, t) не меняет знак на отрезке [a, b].
    Если знак не меняется — функция монотонна — корень единственный.

    :param t: Заданное значение
    :param a: Левая граница отрезка
    :param b: Правая граница отрезка
    :param points: Сколько точек проверять внутри [a, b]

    :return: bool - True, если корень единственный
    """
    signs = set()
    for i in range(points + 1):
        x = a + (b - a) * i / points
        signs.add(derivative_func(x, t) > 0)

    return len(signs) == 1


def find_bracket(t: int, a: float, b: float, step: float) -> Optional[tuple]:
    """
    Ищет отрезок [x, x + step], где f(x, t) меняет знак.

    :param t: Заданное значение
    :param a: Левая граница поиска
    :param b: Правая граница поиска
    :param step: Шаг поиска

    :return: Optional[tuple] - при удачном поиске вернёт
     (x_left, x_right) или None, если не нашёл
    """

    Rich.simple_log(f"нахождение отрезка, на котором есть единственный "
                    f"корень уравнения")

    x = a
    while x < b:
        if func(x, t) * func(x + step, t) < 0:
            if checking_uniqueness(t, x, x + step):
                Rich.success_log(
                    f"Найден отрезок [{x:.3f}, {x + step:.3f}], "
                    f"f' знак не меняет — корень единственный"
                )
                return x, x + step
            else:
                Rich.warning_log(
                    f"На [{x:.3f}, {x + step:.3f}] f' меняет знак — "
                    f"возможен не один корень, уменьшите шаг"
                )
        x += step
    return None


from utils.output_rich import Rich


class TangentMethod:
    """
    Метод касательных (Ньютона) для f(x, t) = 1/(1+x^4) - t*x^2 = 0.
    Итерационная формула: x_{k+1} = x_k - f(x_k) / f'(x_k).
    """

    def __init__(self) -> None:
        self.accuracy = 0.001
        self.max_iter = 100
        self.t = 1
        self.list_iterations = []


    def f(self, x: float) -> float:
        """
        Функция, вычисляющая значение функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение функции f в точке икс
        """

        return 1 / (1 + x ** 4) - self.t * x ** 2


    def df(self, x: float) -> float:
        """
        Функция, вычисляющая значение первой производной функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение производной функции f в точке икс
        """

        return -4 * x ** 3 / (1 + x ** 4) ** 2 - 2 * self.t * x


    def d2f(self, x: float) -> float:
        """
        Функция, вычисляющая значение второй производной функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение производной функции f в точке икс
        """

        return (20 * x ** 6 - 12 * x ** 2) / (1 + x ** 4) ** 3 - 2 * self.t


    def check_convergence(self, a: float, b: float) -> bool:
        """
        Проверяет условия сходимости метода Ньютона:
        - f(a)·f(b) < 0 (корень на отрезке),
        - f'(x) не меняет знак на [a, b],
        - f''(x) не меняет знак на [a, b].
        """

        Rich.simple_log("Проверка применимости метода касательных (Ньютона)")

        fa, fb = self.f(a), self.f(b)
        if fa * fb >= 0:
            Rich.warning_log(f"f(a)·f(b) ≥ 0 — корень может отсутствовать")
            return False

        Rich.debug_log(f"f(a)·f(b) < 0 — есть корень на отрезке")

        # проверка знаков f' и f'' в нескольких точках (проверка на отсутствие точек
        # перегиба и монотонность)
        signs_df, signs_d2f = set(), set()
        n = 100
        for i in range(n + 1):
            x = a + (b - a) * i / n
            signs_df.add(self.df(x) > 0)
            signs_d2f.add(self.d2f(x) > 0)

        ok_df = len(signs_df) == 1
        ok_d2f = len(signs_d2f) == 1

        Rich.debug_log(f"f'(x) знак постоянен — {ok_df}")
        Rich.debug_log(f"f''(x) знак постоянен — {ok_d2f}")

        return ok_df and ok_d2f


    def choose_x0(self, a: float, b: float) -> float:
        """
        Выбирает x0 из [a, b] так, чтобы f(x0)·f''(x0) > 0.
        :param a: принимает левую границу отрезка
        :param b: принимает правую границу отрезка
        :return: float - вычисленная точка x0
        """

        if self.f(a) * self.d2f(a) > 0:
            x0 = a
        else:
            x0 = b
        Rich.debug_log(f"Выбрано x0 = {x0} (f(x0)·f''(x0) > 0)")
        return x0


    def estimate_m1_M2(self, a: float, b: float) -> tuple[float, float]:
        """
        Оценка m1 = min|f'(x)| и M2 = max|f''(x)| на [a, b].
        :param a: левая граница отрезка
        :param b: правая граница отрезка
        :return: пара чисел с плавающей точкой - минимальное значение первой
         производной и максимально второй
        """
        n = 100
        m1 = float('inf')  # плюс бесконечность
        M2 = 0
        for i in range(n + 1):
            x = a + (b - a) * i / n
            m1 = min(m1, abs(self.df(x)))
            M2 = max(M2, abs(self.d2f(x)))
        return m1, M2


    def run(self, a: float, b: float) -> float:
        Rich.print_spacer()
        Rich.simple_log("Запуск метода касательных (Ньютона)")
        Rich.print_spacer()
        Rich.simple_log(f"f(x) = 1/(1 + x**4) - t*x**2")
        Rich.simple_log(f"f'(x) = -4x^3/(1+x^4)^2 - 2*t*x")
        Rich.simple_log("f''(x) = (20x^6 - 12x^2)/(1+x^4)^3 - 2t.")
        Rich.debug_log(f"Отрезок: [{a:.3f}, {b:.3f}], точность = {self.accuracy}")
        Rich.print_spacer()

        # проверка применимости
        if not self.check_convergence(a, b):
            Rich.warning_log("Условия сходимости не выполнены - возможны неточные данные")

        m1, M2 = self.estimate_m1_M2(a, b)
        eps_prime = (2 * m1 * self.accuracy / M2) ** 0.5
        Rich.debug_log(f"m1 = {m1:.6f}, M2 = {M2:.6f}, ε' = {eps_prime:.6f}")

        # выбор начального приближения
        x0 = self.choose_x0(a, b)
        Rich.debug_log(f"x0 = {x0:.6f}")

        # итерации
        self.list_iterations = [x0]
        x_prev = x0

        for iteration in range(1, self.max_iter + 1):
            f_prev = self.f(x_prev)
            df_prev = self.df(x_prev)

            if abs(df_prev) < 1e-15:
                Rich.warning_log("f'(x) ≈ 0 — деление на ноль, остановка")
                break

            x_next = x_prev - f_prev / df_prev
            self.list_iterations.append(x_next)

            delta = abs(x_next - x_prev)
            residual = abs(self.f(x_next))

            Rich.debug_log(
                f"итерация №{iteration}: x = {x_next:.6f}, "
                f"|Δx| = {delta:.6f}, |f(x)| = {residual:.8f}"
            )

            if delta < eps_prime:
                Rich.print_spacer()
                Rich.success_log(
                    f"Сошлось за {iteration} итераций. Корень x ≈ {x_next:.6f}"
                )
                return x_next

            x_prev = x_next

        Rich.warning_log(
            f"Лимит итераций исчерпан. Последнее x = {x_prev:.6f}"
        )
        return x_prev


tangentMethod = TangentMethod()

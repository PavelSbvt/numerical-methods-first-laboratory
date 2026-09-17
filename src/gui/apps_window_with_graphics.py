import numpy as np

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)

from gui.utils.styles import Style
from utils.output_rich import Rich


class AppWindow(QWidget):
    """
    Окно с графиком метода простой итерации.
    Показывает f(x, t), ось 0x, границы [a, b], корень и итерации.
    """

    def __init__(self, a: float, b: float, t: float = 1.0,
                 x_root: float = None, history: list = None) -> None:
        """
        Конструктор
        :param a: левая граница отрезка с единственным решением
        :param b: правая граница отрезка с единственным решением
        :param t: принимает значение t - определено вариантом (t=c)
        :param x_root: массив с промежуточными решениями уравнения методом
         простых итераций
        :param history: массив со всеми полученными промежуточными
         (и искомым) приближёнными решениями
         :return: None
        """

        super().__init__()

        # сохраняем данные для графика
        self.a = a
        self.b = b
        self.t = t
        # приближённое решение уравнения
        self.x_root = x_root
        # массив со всеми решениями (промежуточными и итоговым)
        self.history = history or []

        self.setWindowTitle("AppWindow")
        self.setMinimumSize(700, 500)
        self.setStyleSheet(f"background-color: {Style.general_background_color};")

        main_vertical_lay = QVBoxLayout()
        self.setLayout(main_vertical_lay)

        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)

        main_vertical_lay.addWidget(toolbar)
        main_vertical_lay.addWidget(self.canvas)   # ← один раз!

        self.draw_plot()
        Rich.success_log("Окно с графиком построено")


    def f(self, x):
        """
        Функция, вычисляющая значение функции f(x, t) в точке икс
        :param x: принимает значение переменной икс
        :return: значение функции f в точке икс
        """

        return 1 / (1 + x ** 4) - self.t * x ** 2


    def g(self, x):
        """
        Функция, вычисляющая значение функции g(x) в точке икс
        :param x: принимает значение переменной икс
        :return: значение функции g в точке икс
        """

        return 1 / np.sqrt(self.t * (1 + x ** 4))


    def draw_plot(self) -> None:
        """
        Рисует g(x), y=x, корень и траекторию итераций.

        :return: None
        """
        
        self.ax.clear()

        pad = 0.3
        x_min = max(0.0, self.a - pad)
        x_max = self.b + pad
        x = np.linspace(x_min, x_max, 500)

        # 1. кривая y = g(x)
        y_g = self.g(x)
        self.ax.plot(x, y_g, color="crimson", linewidth=2,
                     label=f"g(x) = 1/√({self.t}·(1+x⁴))")

        # 2. прямая y = x
        self.ax.plot(x, x, color="black", linewidth=1.5, linestyle="-",
                     label="y = x")

        # 3. границы [a, b]
        self.ax.axvline(self.a, color="green", linestyle="--",
                        linewidth=1, alpha=0.6, label=f"a = {self.a:.3f}")
        self.ax.axvline(self.b, color="green", linestyle="--",
                        linewidth=1, alpha=0.6, label=f"b = {self.b:.3f}")

        # 4. корень — точка пересечения g(x) и y=x
        if self.x_root is not None:
            self.ax.plot(self.x_root, self.x_root, "o", color="blue",
                         markersize=10,
                         label=f"корень x ≈ {self.x_root:.4f}")

        # 5. итерации — «паутинка»
        if len(self.history) > 1:
            hx = self.history
            for k in range(len(hx) - 1):
                xk = hx[k]
                xk1 = hx[k + 1]
                # вертикаль: (x_k, 0) → (x_k, g(x_k))
                self.ax.plot([xk, xk], [xk, xk1],
                             color="orange", linewidth=0.9, alpha=0.8)
                # горизонталь: (x_k, g(x_k)) → (x_{k+1}, g(x_k))
                self.ax.plot([xk, xk1], [xk1, xk1],
                             color="orange", linewidth=0.9, alpha=0.8)

            # отдельно отметим все x_k как точки на оси 0x
            self.ax.plot(hx, [0] * len(hx), "x",
                         color="darkorange", markersize=8,
                         label="xₖ (итерации)")

        # 6. оформление
        self.ax.set_title(f"Метод простой итерации, t = {self.t}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)
        self.ax.legend(loc="best")
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(x_min, x_max)  # одинаковые оси — чтобы y=x был под 45°
        self.ax.set_aspect("equal", adjustable="box")  # квадратные клетки

        self.canvas.draw()

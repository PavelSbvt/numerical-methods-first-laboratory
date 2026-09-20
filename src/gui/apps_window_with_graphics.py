import numpy as np

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
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

    def __init__(self,
                 a: float, b: float,
                 t: float = 1.0,
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

        self.setWindowTitle(f"numerical-methods-first-laboratory")
        self.setMinimumSize(700, 500)
        self.setStyleSheet(f"background-color: {Style.general_background_color};")

        # Работа с вкладками
        self.tab_widget = QTabWidget()

        # Вкладки
        tab_main_widget = QWidget()
        self.tab_second_widget = QWidget()

        # Загрузка вкладок
        self.tab_widget.addTab(tab_main_widget, "Метод касательных (Ньютона)")
        self.tab_widget.addTab(self.tab_second_widget, "Метод простой итерации")

        # основной лейаут
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(self.tab_widget)

        # вкладка 1
        layout_tab1 = QVBoxLayout()
        tab_main_widget.setLayout(layout_tab1)

        # вкладка 2
        main_vertical_lay = QVBoxLayout()
        self.tab_second_widget.setLayout(main_vertical_lay)

        # создание фигуры (размер в дюймах)
        self.figure = Figure(figsize=(6, 4), dpi=100)
        # Добавление на холст оси (axes) — область,
        # в которой будут рисоваться графики функций.
        # 111 - первые ячейка, столбец, строка.
        self.ax = self.figure.add_subplot(111)

        # превращает Figure (математический объект) в Qt-виджет
        self.canvas = FigureCanvasQTAgg(self.figure)
        # панель инструментов над графиком
        toolbar = NavigationToolbar(self.canvas, self)

        main_vertical_lay.addWidget(toolbar)
        main_vertical_lay.addWidget(self.canvas)

        self.figure_tangent = Figure(figsize=(6, 4), dpi=100)
        # Добавление на холст оси (axes) — область,
        # в которой будут рисоваться графики функций.
        # 111 - первые ячейка, столбец, строка.
        self.ax_tangent = self.figure_tangent.add_subplot(111)

        # превращает Figure (математический объект) в Qt-виджет
        self.canvas_tangent = FigureCanvasQTAgg(self.figure_tangent)
        # панель инструментов над графиком
        toolbar_tangent = NavigationToolbar(self.canvas_tangent, self)

        layout_tab1.addWidget(toolbar_tangent)
        layout_tab1.addWidget(self.canvas_tangent)

        # рисование функции
        self.draw_plot_simple_iteration_method()

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


    def draw_plot_simple_iteration_method(self) -> None:
        """
        Рисует g(x), y=x, корень и траекторию итераций для метода простых итераций

        :return: None
        """

        self.ax.clear()
        # ax - объект осей

        # pad - отступ от границ холста, для лучшей видимости
        pad = 0.3
        x_min = max(0.0, self.a - pad)
        x_max = self.b + pad
        x = np.linspace(x_min, x_max, 500)

        # кривая y = g(x)
        y_g = self.g(x)
        # метод ax, который рисует линии на осях
        self.ax.plot(x, y_g, color="red", linewidth=2,
                     label=f"g(x) = 1/√({self.t}·(1+x⁴))")

        # прямая y = x
        self.ax.plot(x, x, color="black", linewidth=1.5, linestyle="-",
                     label="y = x")

        # границы [a, b]
        self.ax.axvline(self.a, color="green", linestyle="--",
                        linewidth=1, alpha=0.6, label=f"a = {self.a:.3f}")
        self.ax.axvline(self.b, color="green", linestyle="--",
                        linewidth=1, alpha=0.6, label=f"b = {self.b:.3f}")

        # корень — точка пересечения g(x) и y=x
        if self.x_root is not None:
            self.ax.plot(self.x_root, self.x_root, "o", color="blue",
                         markersize=5,
                         label=f"корень x ≈ {self.x_root:.4f}")

        # итерации — индикация пути
        if len(self.history) > 1:
            hx = self.history
            for k in range(len(hx) - 1):
                xk = hx[k]
                xk1 = hx[k + 1]
                # вертикаль: (x_k, 0) - (x_k, g(x_k))
                self.ax.plot([xk, xk], [xk, xk1],
                             color="orange", linewidth=1.5, alpha=1)
                # горизонталь: (x_k, g(x_k)) - (x_{k+1}, g(x_k))
                self.ax.plot([xk, xk1], [xk1, xk1],
                             color="orange", linewidth=1.5, alpha=1)

        # оформление
        self.ax.set_title(f"Метод простых итераций, t = {self.t}")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        # включение координатной сетки на графике
        self.ax.grid(True)
        # включение легенды — таблички в углу графика
        self.ax.legend(loc="upper right")
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(x_min, x_max)  # y=x
        self.ax.set_aspect("equal", adjustable="box")  # квадратные клетки
        # команда «перерисовать».
        self.canvas.draw()

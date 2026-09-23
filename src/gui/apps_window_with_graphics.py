import numpy as np

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QScrollArea
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
                 x_root: float = None, x_root_tangent: float = None,
                 history: list = None, history_tangent: list = None) -> None:
        """
        Конструктор
        :param a: левая граница отрезка с единственным решением
        :param b: правая граница отрезка с единственным решением
        :param t: принимает значение t - определено вариантом (t=c)
        :param x_root: приближённое решение, полученное методом простой итерации
        :param x_root_tangent: приближённое решение, полученное методом касательных
        :param history: массив со всеми полученными промежуточными
         (и искомым) приближёнными решениями методом простой итерации
         :param history_tangent: массив со всеми полученными промежуточными
         (и искомым) приближёнными решениями методом касательных
        :return: None
        """

        super().__init__()

        # сохраняем данные для графика
        self.a = a
        self.b = b
        self.t = t
        # приближённое решение уравнения
        self.x_root = x_root
        self.x_root_tangent = x_root_tangent
        # массив со всеми решениями (промежуточными и итоговым)
        self.history = history or []
        self.history_tangent = history_tangent or []

        self.setWindowTitle(f"numerical-methods-first-laboratory")
        self.setMinimumSize(800, 700)
        self.setStyleSheet(f"background-color: {Style.general_background_color};")

        # Работа с вкладками
        self.tab_widget = QTabWidget()

        # Вкладки
        tab_main_widget = QWidget()
        self.tab_second_widget = QWidget()
        third_tab = QWidget()

        # Загрузка вкладок
        self.tab_widget.addTab(tab_main_widget, "Метод касательных (Ньютона)")
        self.tab_widget.addTab(self.tab_second_widget, "Метод простой итерации")
        self.tab_widget.addTab(third_tab, "График функции f(x)")

        # основной лейаут
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # вкладка 1
        layout_tab1 = QVBoxLayout()
        tab_main_widget.setLayout(layout_tab1)

        # вкладка 2
        main_vertical_lay = QVBoxLayout()
        self.tab_second_widget.setLayout(main_vertical_lay)

        # Третья вкладка
        third_layout = QVBoxLayout()
        third_tab.setLayout(third_layout)

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

        # график для функции f(x)
        self.figure_f_func = Figure(figsize=(6, 4), dpi=100)
        self.ax_f_func = self.figure_f_func.add_subplot(111)

        # превращает Figure (математический объект) в Qt-виджет
        self.canvas_f_func = FigureCanvasQTAgg(self.figure_f_func)
        self.canvas_f_func.setMinimumSize(300, 300)
        # панель инструментов над графиком
        toolbar_f_func = NavigationToolbar(self.canvas_f_func, self)

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

        third_layout.addWidget(toolbar_f_func)
        third_layout.addWidget(self.canvas_f_func)

        main_layout.addWidget(self.tab_widget)

        # рисование функции
        self.draw_plot_simple_iteration_method()

        self.draw_tangent_method()

        self.draw_raw_graphic()

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

    def df(self, x):
        """Первая производная f(x, t) = -4x³/(1+x⁴)² - 2t·x."""
        return -4 * x ** 3 / (1 + x ** 4) ** 2 - 2 * self.t * x


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


    def draw_tangent_method(self) -> None:
        """
        Рисует f(x) и касательные в точках итераций метода Ньютона.
        """
        self.ax_tangent.clear()

        pad = 0.3
        x_min = max(0.0, self.a - pad)
        x_max = self.b + pad
        x = np.linspace(x_min, x_max, 500)

        # кривая y = f(x)
        y_f = self.f(x)
        self.ax_tangent.plot(x, y_f, color="blue", linewidth=2,
                             label=f"f(x) = 1/(1+x⁴) − {self.t}·x²")

        # ось Ox
        self.ax_tangent.axhline(0, color="black", linewidth=1, alpha=0.5)

        # касательные в точках итераций
        if len(self.history_tangent) > 1:
            hx = self.history_tangent
            for k in range(len(hx) - 1):
                xk = hx[k]
                fxk = self.f(xk)
                dfxk = self.df(xk)

                # касательная: y = f(xk) + f'(xk)·(x − xk)
                x_tangent = np.linspace(x_min, x_max, 100)
                y_tangent = fxk + dfxk * (x_tangent - xk)
                self.ax_tangent.plot(x_tangent, y_tangent,
                                     color="green", linewidth=1, alpha=0.7)

                # вертикальная линия от (x_k, 0) до (x_k, f(x_k))
                self.ax_tangent.plot([xk, xk], [0, fxk],
                                     color="gray", linewidth=0.8,
                                     linestyle=":", alpha=0.6)

        # корень
        if self.x_root_tangent is not None:
            self.ax_tangent.plot(self.x_root_tangent, 0, "o", color="red",
                                 markersize=8,
                                 label=f"корень x ≈ {self.x_root_tangent:.4f}")
            self.ax_tangent.axvline(self.x_root_tangent, color="red",
                                    linestyle="--", linewidth=1, alpha=0.6)

        # оформление
        self.ax_tangent.set_title(f"Метод касательных (Ньютона), t = {self.t}")
        self.ax_tangent.set_xlabel("x")
        self.ax_tangent.set_ylabel("y")
        self.ax_tangent.grid(True)
        self.ax_tangent.legend(loc="upper right")
        self.ax_tangent.set_xlim(x_min, x_max)
        self.ax_tangent.set_ylim(y_f.min() - 0.5, y_f.max() + 0.5)
        self.canvas_tangent.draw()


    def draw_raw_graphic(self) -> None:
        """
        Функция для рисования графика f(x, t) и индикация на нём найденных корней.
        :return:
        """
        self.ax_f_func.clear()
        # ax - объект осей

        # pad - отступ от границ холста, для лучшей видимости
        pad = 0.3
        x_min = max(0.0, self.a - pad)
        x_max = self.b + pad
        x = np.linspace(x_min, x_max, 500)

        # кривая y = g(x)
        y_f = self.f(x)
        # метод ax, который рисует линии на осях
        self.ax_f_func.plot(x, y_f, color="blue", linewidth=2,
                     label=f"f(x) = 1/(1 + x**4) - {self.t}*x**2")
        if self.x_root is not None:
            self.ax_f_func.plot(
                self.x_root, 0,  # координаты: (x*, 0)
                "o",  # маркер — круг
                color="red",
                markersize=8,
                label=f"корень x ≈ {self.x_root:.4f}"
            )
        if self.x_root_tangent is not None:
            self.ax_f_func.plot(
                self.x_root_tangent, 0,  # координаты: (x*, 0)
                "o",  # маркер — круг
                color="green",
                markersize=8,
                label=f"корень x ≈ {self.x_root_tangent:.4f}"
            )
        # оформление
        self.ax_f_func.set_title(f"исходная функция, t = {self.t}")
        self.ax_f_func.set_xlabel("x")
        self.ax_f_func.set_ylabel("y")
        # включение координатной сетки на графике
        self.ax_f_func.grid(True)
        # включение легенды — таблички в углу графика
        self.ax_f_func.legend(loc="upper right")
        self.ax_f_func.set_xlim(x_min, x_max)
        self.ax_f_func.set_ylim(x_min, x_max)  # y=x
        self.ax_f_func.set_aspect("equal", adjustable="box")  # квадратные клетки
        # команда «перерисовать».
        self.canvas_f_func.draw()

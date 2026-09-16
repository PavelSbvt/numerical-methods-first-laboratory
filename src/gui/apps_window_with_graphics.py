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
    Класс графического интерфейса для отображения
    результатов вычислений и графиков. На PyQt6
    """

    def __init__(self):
        super().__init__()

        self.setObjectName("MainAppWindow")
        self.setMinimumSize(600, 400)
        self.setStyleSheet(f"background-color: {Style.general_background_color};")

        main_vertical_lay = QVBoxLayout()
        self.setLayout(main_vertical_lay)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.figure)
        toolbar = NavigationToolbar(self.canvas, self)
        main_vertical_lay.addWidget(toolbar)
        main_vertical_lay.addWidget(self.canvas)
        main_vertical_lay.addWidget(self.canvas)

        # --- рисуем график ---
        self.draw_plot()

        Rich.success_log("Окно с графиком построено :)")

    def draw_plot(self) -> None:
        """
        Пример отрисовки простого графика.
        """

        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]

        self.ax.clear()  # на случай повторного вызова
        self.ax.plot(x, y, marker="o", color="crimson")
        self.ax.set_title("тестовый график")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.grid(True)

        self.canvas.draw()



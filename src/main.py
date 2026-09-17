import sys

from PyQt6.QtWidgets import QApplication

from core.simple_iteration_method import simpleIterationMethod
from core.utils.function_research import find_bracket
from gui.apps_window_with_graphics import AppWindow
from utils.output_rich import Rich

Rich.print_spacer()
Rich.simple_log("Запуск программы")
Rich.print_spacer()

if __name__ == "__main__":
    # Поиск и получение отрезка
    span = find_bracket(1, 0.0, 2.0, 0.05)

    if span:
        Rich.simple_log(f"отрезок с единственным "
                        f"корнем уравнения: [{span[0]:.3f}, {span[1]:.3f}]")
    else:
        Rich.warning_log(f"Корень не найден на заданном промежутке")

    # Границы
    a_border = span[0]
    b_border = span[1]

    Rich.print_spacer()

    # массив с приближёнными решениями
    x_root = simpleIterationMethod.run(a_border, b_border)

    app = QApplication(sys.argv)

    # окно с графиком и промежуточными решениями тангенциального уравнения
    # методом простых итераций
    app_window = AppWindow(
        a=a_border,
        b=b_border,
        t=simpleIterationMethod.t,
        x_root=x_root,
        history=simpleIterationMethod.list_iterations,
    )

    Rich.debug_log("Показ главного окна")
    app_window.show()

    sys.exit(app.exec())

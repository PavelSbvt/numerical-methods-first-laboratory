import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.simple_iteration_method import simpleIterationMethod
from  core.tangent_method import tangentMethod
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

    # приближённое решение уравнения
    x_root = simpleIterationMethod.run(a_border, b_border)

    app = QApplication(sys.argv)

    # окно с графиком и промежуточными решениями тангенциального уравнения
    # методом простых итераций
    appWindowSimpleIteration = AppWindow(
        a=a_border,
        b=b_border,
        window_title="Метод простых итераций",
        chapter="/simple_iteration_method",
        t=simpleIterationMethod.t,
        x_root=x_root,
        history=simpleIterationMethod.list_iterations,
    )

    appWindowSimpleIteration.show()

    App = QApplication(sys.argv)
    icon_path = Path('resources/images/icons/icon_lab.ico')
    App.setWindowIcon(QIcon(f"{icon_path.as_posix()}"))

    sys.exit(app.exec())

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
    # Поиск и получение отрезка − отделение корня,
    # т.е. нахождение такого отрезка [a, b], на котором существует
    # единственный корень уравнения f(x) = 0.
    span = find_bracket(1, 0.0, 2.0, 0.05)

    if span:
        Rich.debug_log(f"отрезок с единственным "
                        f"корнем уравнения: [{span[0]:.3f}, {span[1]:.3f}]")
    else:
        Rich.warning_log(f"Корень не найден на заданном промежутке")

    # Границы отрезка
    a_border = span[0]
    b_border = span[1]

    Rich.print_spacer()

    # − уточнение корня, т.е. нахождение приближённого решения с заданной
    # точностью при помощи метода простых итераций
    x_root = simpleIterationMethod.run(a_border, b_border)
    x_root_tangent = tangentMethod.run(a_border, b_border)

    App = QApplication(sys.argv)

    # окно с графиком и промежуточными решениями тангенциального уравнения
    # методом простых итераций и методом касательных (Ньютона)
    appWindowSimpleIteration = AppWindow(
        a=a_border,
        b=b_border,
        x_root=x_root,
        x_root_tangent=x_root_tangent,
        history=simpleIterationMethod.list_iterations,
        history_tangent=tangentMethod.list_iterations,
    )

    appWindowSimpleIteration.show()

    icon_path = Path('resources/images/icons/icon_lab.ico')
    App.setWindowIcon(QIcon(f"{icon_path.as_posix()}"))

    sys.exit(App.exec())

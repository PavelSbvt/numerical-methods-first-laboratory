import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.simple_iteration_method import simpleIterationMethod
from core.utils.function_research import find_bracket
from gui.apps_window_with_graphics import AppWindow
from utils.output_rich import Rich

Rich.print_spacer()
Rich.simple_log("Запуск программы")
Rich.print_spacer()

if __name__ == "__main__":
    span = find_bracket(1, 0.0, 100.0, 0.05)

    if span:
        Rich.simple_log(f"отрезок с единственным "
                        f"корнем уравнения: [{span[0]:.3f}, {span[1]:.3f}]")
    else:
        Rich.warning_log(f"Корень не найден на заданном промежутке")

    a_border = span[0]
    b_border = span[1]

    Rich.print_spacer()

    simpleIterationMethod.run(a_border, b_border)

    app = QApplication(sys.argv)
    app_window = AppWindow()

    icon_path = Path('resources/images/icons/icon_pdf_maker_255_size.ico')
    app.setWindowIcon(QIcon(f"{icon_path.as_posix()}"))

    Rich.debug_log("Показ главного окна")
    app_window.show()

    sys.exit(app.exec())

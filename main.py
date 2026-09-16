import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from core.simple_iteration_method import simple_iteration_method
from gui.apps_window_with_graphics import AppWindow
from utils.output_rich import Rich

Rich.print_spacer()
Rich.simple_log("Запуск программы")
Rich.print_spacer()

if __name__ == "__main__":
    simple_iteration_method.run()

    app = QApplication(sys.argv)
    app_window = AppWindow()

    icon_path = Path('resources/images/icons/icon_pdf_maker_255_size.ico')
    app.setWindowIcon(QIcon(f"{icon_path.as_posix()}"))

    Rich.debug_log("Показ главного окна")
    app_window.show()

    sys.exit(app.exec())

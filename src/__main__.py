import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load and apply the stylesheet

    try:
        with open("src/ui/style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Stylesheet not found.")
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

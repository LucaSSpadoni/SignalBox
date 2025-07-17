from app.main_window import MainWindow
from PySide6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # Run the main function to start the application
    # This is the entry point of the application
    main()
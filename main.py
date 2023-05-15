from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QWindow
from calculator import Calculator




if __name__ == '__main__':
    app = QApplication()

    c = Calculator()
    c.show()
    app.exec()
    ...

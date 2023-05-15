""" Create QT Widgets with predefined arguments """
from collections.abc import Callable
from PySide6.QtGui import QAction, QFont
from PySide6.QtWidgets import QPushButton, QWidget, QGridLayout




class QPushButtonFactory:
    """
      Create QPushButton with text and function that will be executed on button 
      click action.
    """
    def __create(self, text: str, onclick: Callable[[QAction], None]) -> QPushButton:
        """
          Returns a QPushButton with the text and function.
        """
        qpushbutton = QPushButton()
        qpushbutton.setText(text)
        qpushbutton.clicked.connect(onclick)
        return qpushbutton

    def __call__(self, text: str, onclick: Callable[[QAction], None]) -> QPushButton:
        return self.__create(text, onclick)




class QGridLayoutFactory:
    """
      Creates a Grid Layout and adds __Widgets to it.
      For this to work consider:
        WidgetWithPosition -> A tuple equal (QWidget, row, col, rowspan, colspan).
    """
    WidgetWithPosition = tuple[QWidget, int, int, int ,int]
    Widgets = list[WidgetWithPosition]
    
    def __create(self, widgets: Widgets) -> QGridLayout:
        """ Returns the QGridLayout with the components added and positioned. """
        gridlayout = QGridLayout()

        for w in widgets:
            gridlayout.addWidget(w[0], w[1], w[2], w[3], w[4])

        return gridlayout
    
    def __call__(self, widgets: Widgets) -> QGridLayout:
        return self.__create(widgets)
    





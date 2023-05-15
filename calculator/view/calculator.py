""" Draw Calculator GUI """
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget
from PySide6.QtGui import Qt, QAction
from PySide6.QtCore import Slot
from .factories import QPushButtonFactory, QGridLayoutFactory
from pathlib import Path
from collections.abc import Callable
from calculator.model.expression import Memory, ExpressionParser, Operations


def _get_stylesheet() -> str:
    """ Return stylesheet absolute path """
    path = Path('.').absolute() / 'calculator'
    path /=  'view' 
    path /= 'style.ss'
    stylesheet = ''

    with open(path) as file:
        for line in file:
            stylesheet += line

    return stylesheet
        

class Calculator(QMainWindow):
    """  Construction of a custom QWindow to compose the calculator's GUI. """

    def __init__(self):
        super().__init__()

        self.__memory = Memory()
        self.__answer = None
        self.__parser = ExpressionParser(self.__memory)

        self.__set_constraints()
        self.setWindowTitle('Calculadora')
        self.setMinimumSize(self.__WIDTH, self.__HEIGHT)
        self.setMaximumSize(self.__WIDTH, self.__HEIGHT)
        self.__initialize_widgets()
        self.setStyleSheet(_get_stylesheet())

    def __set_constraints(self):
        """ Set Constraints 
          __CHARACTER_LIMIT: Maximum display characters that can be used 
                             for calculations.
          __WIDTH : Width of window screen
          __HEIGHT: Height of window screen
        """
        self.__CHARACTER_LIMIT = 10
        self.__WIDTH = 350
        self.__HEIGHT = 300

    def __initialize_widgets(self):
        """ Creates widget objects and places them on the screen"""
        widgets = []
        btfactory = QPushButtonFactory()
        glfactory = QGridLayoutFactory()
        
        # Named widgets
        self.__display = QLabel('')
        self.__display.setAlignment(Qt.AlignmentFlag.AlignRight)
        widgets.append((self.__display, 1, 1, 1, 4))

        # Anonymous Widgets
        widgets.extend(\
              [
                # Adds the buttons keys following the calculator keyboard layout
                #
                #  CALCULATOR LAYOUT
                #  |     DISPLAY      |
                #  |CE     ||C   ||del|
                #  |1/x||x²||sqrt||div|
                #  |7  ||8 ||9   || * |
                #  |4  ||5 ||6   || - |
                #  |1  ||2 ||3   || + |
                #  |+- ||. ||0   || = | 
                #
                (btfactory('CE', self.__btce_onclick), 2, 1, 1, 2),
                (btfactory('C', self.__btc_onclick), 2, 3, 1, 1),
                (btfactory('\u2421', self.__btdel_onclick), 2, 4, 1, 1),
                (btfactory('\u215F', self.__btone_over_x_onclick), 3, 1, 1, 1),
                (btfactory('x²', self.__btsquare_x_onclick), 3, 2, 1, 1),
                (btfactory('\u221Ax', self.__btsquare_root_onclick), 3, 3, 1, 1),
                (btfactory('\u00F7', self.__btdiv_onclick), 3, 4, 1, 1),
                (btfactory('7', self.__bt7_onclick), 4, 1, 1, 1),
                (btfactory('8', self.__bt8_onclick), 4, 2, 1, 1),
                (btfactory('9', self.__bt9_onclick), 4, 3, 1, 1),
                (btfactory('\u00D7', self.__btmultiply_onclick), 4, 4, 1, 1),
                (btfactory('4', self.__bt4_onclick), 5, 1, 1, 1),
                (btfactory('5', self.__bt5_onclick), 5, 2, 1, 1),
                (btfactory('6', self.__bt6_onclick), 5, 3, 1, 1),
                (btfactory('-', self.__btminus_onclick), 5, 4, 1, 1),
                (btfactory('1', self.__bt1_onclick), 6, 1, 1, 1),
                (btfactory('2', self.__bt2_onclick), 6, 2, 1, 1),
                (btfactory('3', self.__bt3_onclick), 6, 3, 1, 1),
                (btfactory('+', self.__btplus_on_click), 6, 4, 1, 1),
                (btfactory('\u00B1', self.__btplus_minus), 7, 1, 1, 1),
                (btfactory('.', self.__btdot), 7, 2, 1, 1),
                (btfactory('0', self.__bt0_onclick), 7, 3, 1, 1),
                (btfactory('=', self.__bteq_onclick), 7, 4, 1, 1)
              ]
            )
        self.setCentralWidget(QWidget()) 
        self.centralWidget().setLayout(glfactory(widgets))    




    ### GUI UTILITY & VALIDATIONS
    def __clear_all(self):
        """ Clear last answer, memory and display"""
        self.__memory.clear()
        self.__answer = None
        self.__display.clear()

    def __to_int_or_float(self, text: str) -> int | float:
        """ Converts display text to int or float depending on user input """
        if self.__is_float(text):
            return float(text)
        return int(text)

    def __put_answer_on_the_display(self):
        """ Put last answer on  display """
        self.__display.setText(f'{self.__answer}')

    def __show_error(self):
        """ Show error string on display """
        self.__display.setText('ERR')

    def __display_clean(self) -> bool:
        """ Checks if display is clean"""
        return len(self.__display.text()) == 0

    def __is_answer_on_the_display(self) -> bool:
        """ Checks if last answers is in display"""
        return str(self.__answer) == self.__display.text()

    def __is_float(self, text: str) -> bool:
        """ Checks if text is float """
        return text.find('.') != -1

    def __is_on_limit(self) -> bool:
        """ 
            Checks if the value present on the display is below the 
            character limit 
        """
        if len(self.__display.text()) > self.__CHARACTER_LIMIT:
            self.__clear_all()
            self.__display.setText('ERR')
            return False
        return True
    
    def __is_doted(self) -> bool:
        """ Checks if a '.' has already been added to the value in the display. """
        return self.__display.text().count('.') > 0




    #### KEY FUNCTIONS
    def __numeric_key(self, text: str): 
        """ 
            Performs common number key behaviors. 
            Consider numeric keys like: 0-9 keys 
        """
        if self.__is_answer_on_the_display():
            self.__display.clear()
        self.__display.setText(self.__display.text() + text)

    def __arithmetic_key_u(self, operation: Callable):
        """ Performs the common behaviors of unary arithmetic operations keys. """
        if self.__display_clean():
            return
        
        if not self.__is_on_limit():
            return
        
        self.__memory.push(operation)
        self.__memory.push(self.__to_int_or_float(self.__display.text()))
        self.__answer = self.__parser.execute()
        self.__put_answer_on_the_display()

    def __arithmetic_key_b(self, operation: Callable):
        """ Performs the common behaviors of binary arithmetic operations keys """
        if self.__display_clean():
            return

        if not self.__is_on_limit():
            return 
        
        self.__memory.push(operation)
        self.__memory.push(self.__to_int_or_float(self.__display.text()))
        self.__display.clear()




    ####################################
    # NUMERIC KEYS EVENTS
    ####################################
    @Slot()
    def __bt0_onclick(self, change): 
        """ Zero key click event """
        self.__numeric_key('0')

    @Slot()
    def __bt1_onclick(self, change): 
        """ One key click event """
        self.__numeric_key('1')

    @Slot()
    def __bt2_onclick(self, change): 
        """ Two key click event """
        self.__numeric_key('2')

    @Slot()
    def __bt3_onclick(self, change):
        """ Three key click event """
        self.__numeric_key('3')

    @Slot()
    def __bt4_onclick(self, change):
        """ Four key click event """
        self.__numeric_key('4')

    @Slot()
    def __bt5_onclick(self, change):
        """ Five key click event """
        self.__numeric_key('5')

    @Slot()
    def __bt6_onclick(self, change):
        """ Five key click event """
        self.__numeric_key('6')

    @Slot()
    def __bt7_onclick(self, change):
        """ Seven key click event """
        self.__numeric_key('7')

    @Slot()
    def __bt8_onclick(self, change):
        """ Eight key click event """
        self.__numeric_key('8')

    @Slot()
    def __bt9_onclick(self, change):
        """ Nine key click event """
        self.__numeric_key('9')




    ############################################
    # ARITHMETIC KEYS EVENTS (BINARY OPERATIONS) 
    ############################################
    @Slot()
    def __btplus_on_click(self, change): 
        """ Plus key click event """
        self.__arithmetic_key_b(Operations.plus)

    @Slot()
    def __btminus_onclick(self, change):
        """ Minus key click event """
        self.__arithmetic_key_b(Operations.minus)

    @Slot()
    def __btmultiply_onclick(self, change):
        """ Multiply key click event """
        self.__arithmetic_key_b(Operations.multiply)

    @Slot()
    def __btdiv_onclick(self, change):
        """ Division key click event """
        self.__arithmetic_key_b(Operations.div_float)



    #############################################
    # ARITHMETIC KEYS EVENTS (UNARY OPERATIONS) 
    #############################################
    Slot()
    def __btone_over_x_onclick(self, change): 
        """ 1/x key click event """
        try:
            self.__arithmetic_key_u(Operations.one_over_x)
        except ZeroDivisionError:
            self.__show_error()
    
    @Slot()
    def __btsquare_x_onclick(self, change):
        """ x² key click event """
        self.__arithmetic_key_u(Operations.square_x)

    @Slot()
    def __btsquare_root_onclick(self, change):
        """ sqrt key click event """
        self.__arithmetic_key_u(Operations.square_root)

    ### RESOLVER
    @Slot()
    def __bteq_onclick(self, change): 
        """ = key click event """
        if self.__memory.size() == 0: 
            return 

        if self.__display_clean():
            return
        
        if not self.__is_on_limit():
            return
        
        try: 
            self.__memory.push(self.__to_int_or_float(self.__display.text()))
            self.__answer = self.__parser.execute()
            self.__put_answer_on_the_display()
        except ZeroDivisionError:
            self.__show_error()




    ####################################
    # UTILITY KEYS EVENTS
    ####################################
    @Slot()
    def __btc_onclick(self, change): 
        """ 'C' key click event """
        self.__display.clear()
    
    @Slot()
    def __btce_onclick(self, change): 
        """ 'CE' key click event """
        self.__clear_all()

    @Slot()
    def __btdel_onclick(self, change):
        """ del key click event """
        self.__display.setText(self.__display.text()[0:-1])

    @Slot()
    def __btplus_minus(self, change):
        """ +- key click event """
        if self.__display_clean():
            return
        x = self.__to_int_or_float(self.__display.text())
        self.__display.setText(f'{Operations.plus_minus(x)}')

    @Slot()
    def __btdot(self, change):
        """ '.' key click event """
        if self.__display_clean():
            return
        
        if self.__is_doted():
            return
        
        self.__display.setText(self.__display.text() + '.')
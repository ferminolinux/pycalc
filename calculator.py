from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Slot




class TextOperations:
    
    @staticmethod
    def to_int_or_float(self, text: str):
        if text.find('.') != -1:
            return float(text)
        return int(text)

    @staticmethod
    def is_under_char_limit(self, text) -> bool:
        if (len(text) > 8):
            raise ValueError()
        return True
    

class MathOperations:

    @staticmethod
    def sum(x, y):
        return x + y
    
    @staticmethod
    def subtraction(x, y):
        return x - y
    
    @staticmethod
    def multiply(x ,y):
        return x * y
    
    @staticmethod
    def idiv(x, y):
        return x // y
    
    @staticmethod
    def fdiv(x, y):
        return x / y
    

class Memory:
    # TODO: adicionar função para adicionar operandos(argumentos) ou operador(função) na pilha
    # TODO: adicionar função para validar se há uma operação no topo da pilha
    # TODO: adicionar função que executa a operação, retirando ela e seus operandos da pilha
    ...


class Calculator(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: adicionar uma instância da classe Memory

        self.__display = QLabel()
        self.__btce  = QPushButton('CE')
        self.__btc  = QPushButton('C')
        self.__btdiv  = QPushButton('/')
        self.__bt7  = QPushButton('7')
        self.__bt8  = QPushButton('8')
        self.__bt9  = QPushButton('9')
        self.__btmult  = QPushButton('*')
        self.__bt4  = QPushButton('4')
        self.__bt5  = QPushButton('5')
        self.__bt6  = QPushButton('6')
        self.__btminus  = QPushButton('-')
        self.__bt1  = QPushButton('1')
        self.__bt2  = QPushButton('2')
        self.__bt3  = QPushButton('3')
        self.__btplus  = QPushButton('+')
        self.__bt0  = QPushButton('0')
        self.__bteq  = QPushButton('=')

        # TODO: Adicionar os botões com as teclas e operações que faltam

        self.__add_events()
        self.__get_main_window()


    def __show_window(self):
        self.__main_window.show()


    def __get_main_window(self):
        layout = QGridLayout()
        self.__draw_widgets(layout)

        widget = QWidget()
        widget.setLayout(layout)

        window = QMainWindow()
        window.setCentralWidget(widget)

        self.__main_window = window

        
    def __draw_widgets(self, layout: QGridLayout):
        layout.addWidget(self.__display, 1, 1, 1, 4)

        layout.addWidget(self.__btce, 2, 1, 1, 2)
        layout.addWidget(self.__btc, 2, 3, 1, 1)
        layout.addWidget(self.__btdiv, 2, 4, 1, 1)

        layout.addWidget(self.__bt7, 3, 1, 1, 1)
        layout.addWidget(self.__bt8, 3, 2, 1, 1)
        layout.addWidget(self.__bt9, 3, 3, 1, 1)
        layout.addWidget(self.__btmult, 3, 4, 1, 1)

        layout.addWidget(self.__bt4, 4, 1, 1, 1)
        layout.addWidget(self.__bt5, 4, 2, 1, 1)
        layout.addWidget(self.__bt6, 4, 3, 1, 1)
        layout.addWidget(self.__btminus, 4, 4, 1, 1)

        layout.addWidget(self.__bt1, 5, 1, 1, 1)
        layout.addWidget(self.__bt2, 5, 2, 1, 1)
        layout.addWidget(self.__bt3, 5, 3, 1, 1)
        layout.addWidget(self.__btplus, 5, 4, 1, 1)

        layout.addWidget(self.__bt0, 6, 1, 1, 2)
        layout.addWidget(self.__bteq, 6, 3, 1, 2)


    def __add_events(self):
        self.__bt7.clicked.connect(self.__numberkey_onclick(self.__bt7.text()))
        self.__bt8.clicked.connect(self.__numberkey_onclick(self.__bt8.text()))
        self.__bt9.clicked.connect(self.__numberkey_onclick(self.__bt9.text()))
        self.__bt4.clicked.connect(self.__numberkey_onclick(self.__bt4.text()))
        self.__bt5.clicked.connect(self.__numberkey_onclick(self.__bt5.text()))
        self.__bt6.clicked.connect(self.__numberkey_onclick(self.__bt6.text()))
        self.__bt1.clicked.connect(self.__numberkey_onclick(self.__bt1.text()))
        self.__bt2.clicked.connect(self.__numberkey_onclick(self.__bt2.text()))
        self.__bt3.clicked.connect(self.__numberkey_onclick(self.__bt3.text()))
        self.__bt0.clicked.connect(self.__numberkey_onclick(self.__bt0.text()))


    def exec(self):
        self.__show_window()
        super().exec()

    # TODO: definir função para limpar o display

    ## SLOTS
    @Slot(str)
    def __numberkey_onclick(self, text):
        def inner(checked):
            self.__display.setText(self.__display.text() + text)
        return inner

    '''
    TODO: Definir slots para o clique dos botões, que permitam executar as operações através
        do uso da da memória, de modo que seja possível executar a operacão matématica e
        obter o resultado só operacionando a pilha de operações e operandos da memória.
    '''

if __name__ == '__main__':
    Calculator().exec()
    


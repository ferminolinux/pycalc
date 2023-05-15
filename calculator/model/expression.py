""" 
Provides classes for calculator logic
"""
from collections.abc import Callable
from inspect import getfullargspec

"""
    In this scope consider:
        _Number: Value can be of type float or int
        _Numbers: Tuple of _Numbers.
        _Operation: A callable that numbers does some work 
                    with them and returns the result.
        _Expression: A tuple containing the args(_Numbers) and function(_Operation)     
"""
_Number = int | float
_Numbers = tuple[_Number]
_Operation = Callable[[_Numbers], _Numbers]
_Expression = tuple[_Numbers, _Operation]

class Memory: 
    """ 
        Stores operations and values ​​on a stack 
    """
    def __init__(self):
        self.__memory = []

    def push(self, value_or_ops: _Numbers | _Operation):
        """ Add value or operation in memory stack """
        self.__memory.append(value_or_ops)

    def pop(self) -> _Numbers | _Operation:
        """ remove value or operation from memory stack """
        return self.__memory.pop()
    
    def size(self) -> int:
        return len(self.__memory)

    def clear(self):
        """ clear memory stack """
        self.__memory = []


class ExpressionParser:
    """ Provides the logic to interpret and execute expressions present in memory """
    def __init__(self, memory: Memory): 
        self.__memory = memory


    def __generate(self) -> _Expression:
        """ Generate a expression """
        expression = []

        while True:
            if self.__memory.size() == 0:
                break
            ## expression: (args_in_reverse_order, function)
            expression.append(self.__memory.pop())
            

        return tuple(expression)
    
    def __parse_function(self, e: _Expression):
        """ Extract function definition of a expression """
        
        ## e: (args_in_reverse_order, function)
        return e[-1]
    
    def __parse_args(self, e: _Expression):
        """ Order and Extract args of a function of a expression"""
        ## e: (args_in_reverse_order, function)
        return tuple(reversed(e[0:-1]))

    def __validate(self, expression: _Expression) -> bool:
        """ 
            Checks if the number of arguments the function needs 
            has been satisfied
        """
        function_ = self.__parse_function(expression)
        args = self.__parse_args(expression)

        if len(args) != len(getfullargspec(function_).args):
            name_def = function_.__name__
            args_def = getfullargspec(function_).args
            message = f'Problem with the arguments for the {name_def} operation.\n'
            message += f'This operation has been defined as '
            message += f'"{name_def}({args_def})", follow it to avoid problems \n'
            raise RuntimeError(message)
        
        return True
    

     
    def execute(self) -> _Numbers:
        """ 
            Executes the expression, that is, calls the function 
            passing the corresponding arguments .
        """
        expression = self.__generate()
        self.__validate(expression)

        function_ = self.__parse_function(expression)
        args = self.__parse_args(expression)

        return function_(*args)




class Operations:
    """ Static functions to perform calculator operations """
    
    @staticmethod
    def plus(x: _Number, y: _Number) -> _Number:
        return x + y
    
    @staticmethod
    def minus(x: _Number, y: _Number) -> _Number:
        return x - y
    
    @staticmethod
    def multiply(x: _Number, y: _Number) -> _Number:
        return x * y
    
    @staticmethod
    def div_int(x: _Number, y: _Number) -> _Number:
        return x // y
    
    @staticmethod
    def div_float(x: _Number, y:_Number) -> _Number:
        return x / y
    
    @staticmethod
    def one_over_x(x: _Number) -> _Number:
        return Operations.div_float(1, x)
    
    @staticmethod
    def square_x(x: _Number) -> _Number:
        return x ** 2
    
    @staticmethod
    def square_root(x: _Number) -> _Number:
        return x ** 0.5
    
    @staticmethod
    def plus_minus(x: _Number) -> _Number:
        return x * (-1)

    


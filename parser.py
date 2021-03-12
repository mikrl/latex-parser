from algorithms import shunting_yard
from lexer import Lexer
from utilities import rpn_to_ast


class LatexParser:

    def __init__(self):
        self._parse_str = ""
        self._rpn_str = ""
        self._ast = None
        self._parse_algorithm = shunting_yard

    @classmethod
    def parse(cls, parse_string: str) -> str:
        if parse_string != cls._parse_str:
            cls._parse_str = parse_string
            cls._rpn_str = cls._parse_algorithm(parse_string)
        return cls._rpn_str

    @classmethod
    def to_ast(cls, parse_string):
        rpn_str = cls.parse(parse_string)
        cls._ast = rpn_to_ast(rpn_str)
        return cls._ast

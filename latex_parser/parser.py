from latex_parser.algorithms import shunting_yard
from latex_parser.lexer import Lexer
from latex_parser.utilities import rpn_to_ast


class LatexParser:
    def __init__(self):
        self._parse_str = ""
        self._rpn_str = ""
        self._ast = None
        self._parse_algorithm = shunting_yard

    def parse(self, parse_string: str) -> str:
        if parse_string != self._parse_str:
            self._parse_str = parse_string
            parser_inp = Lexer.tokenize(self._parse_str)
            parser_out = self._parse_algorithm(parser_inp)
            self._rpn_str = Lexer.untokenize(parse_string)
        return self._rpn_str

    def to_ast(self, parse_string):
        rpn_str = self.parse(parse_string)
        self._ast = rpn_to_ast(rpn_str)
        return self._ast

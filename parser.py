import ast


def shunting_yard(parse_str: str) -> str:
    raise NotImplementedError


class Parser:

    def __init__(self):
        self._parse_str = ""
        self._rpn_str = ""
        self._ast = None
        self._parse_algorithm = shunting_yard

    def parse(self, parse_str: str) -> str:
        if parse_str != self._parse_str:
            self._parse_algorithm(parse_str)
        return self._rpn_str

    def to_ast(self, parse_str):
        rpn_str = self.parse(parse_str)
        # Turn rpn string into ast.
        raise NotImplementedError

""" Lexer tests."""
import random
import re
import unittest
from typing import List, Dict

from latex_parser.lexer import Lexer  # import Lexer


def _insert_spaces(string: str, max_run: int) -> str:
    """
    Randomly inserts runs of up to max_run spaces into a string.
    """

    max_run = max(max_run, 1)
    string = list(string)
    for i in range(len(string) - 1):
        string[i] = string[i] + " " * random.randrange(max_run)

    return "".join(string)


class TestLexer(unittest.TestCase):
    """
    Test that the lexer successfully handles inputs.
    """

    def setUp(self):
        self.lexer = Lexer()

    def test_lexer_functions(self):
        with self.assertRaises(TypeError):
            self.lexer._new_token("UNSUPPORTED")

        for token_type in ["CONS", "VAR", "BINOP_INFIX", "BINOP_PRFIX"]:
            assert re.match(f"{token_type}_[0-9]+", self.lexer._new_token(token_type))

    def test_lexer_edge_cases(self):
        """
        Test null inputs and handling of spaces.
        """
        # Test that lexing nothing leads to an exception
        with self.assertRaises(TypeError):
            self.lexer.lex(None)
            self.lexer.lex()

        # Test that lexing a null string yields a null list
        assert self.lexer.lex("") == []

        # Test that a string of spaces yields a null list
        for i in range(0, 1024):
            spaces = " " * i
            assert self.lexer.lex(spaces) == []

        # Test that adding spaces into an input yields the same output
        in_string = ""
        lexed_string = self.lexer.lex(in_string)
        for i in range(1, 128):
            spaced_string = _insert_spaces(in_string, i)
            assert self.lexer.lex(spaced_string) == lexed_string

    def _test_lexing(self, in_string: str, output: List[str], mapping: Dict[str, str]):
        """
        Utility function to test that the lexer lexes and maps correctly.
        """
        lexer_output = self.lexer.lex(in_string)
        assert lexer_output == output
        for token in lexer_output:
            assert self.lexer.symbol_table[token] == mapping[token]

    def test_lexes_simple_equation(self):
        """
        Tests that when passed simple latex, the lexer lexes correctly.
        """
        # Test simple inputs
        # Simple addition of contants
        in_string = "3+2"
        output = ["CONS_1", "BINOP_INFIX_1", "CONS_2"]
        mapping = {"CONS_1": "3", "BINOP_INFIX_1": "+", "CONS_2": "2"}
        self._test_lexing(in_string, output, mapping)

    def test_lexes_variable_equation(self):
        """
        Test that the lexer can handle an equation with free variables.
        """
        # Equation with free variable
        in_string = "x^{3} + 2x -1"
        output = [
            "VAR_1",
            "BINOP_INFIX_1",
            "LPAREN",
            "CONS_1",
            "RPAREN",
            "BINOP_INFIX_2",
            "CONS_2",
            "VAR_1",
            "BINOP_INFIX_3",
            "CONS_3",
        ]
        mapping = {
            "VAR_1": "x",
            "BINOP_INFIX_1": "pow",
            "LPAREN": "(",
            "CONS_1": "3",
            "RPAREN": ")",
            "BINOP_INFIX_2": "+",
            "CONS_2": "2",
            "BINOP_INFIX_3": "-",
            "CONS_3": "1",
        }
        self._test_lexing(in_string, output, mapping)

    def test_lexes_functions(self):
        """
        Test that the lexer can handle functions.
        """
        in_string = "\sin(x^{2}+1) + \ln(\frac{1}{x})"
        output = [
            "FUNC_1",
            "LPAREN",
            "VAR_1",
            "BINOP_INFIX_1",
            "LPAREN",
            "CONS_1",
            "RPAREN",
            "BINOP_INFIX_2",
            "CONS_2",
            "RPAREN",
            "BINOP_INFIX_3",
            "FUNC_2",
            "BINOP_PRFIX_1",
            "LPAREN",
            "CONS_3",
            "RPAREN",
            "LPAREN",
            "VAR_1",
            "RPAREN",
            "RPAREN",
        ]
        mapping = {
            "FUNC_1": "sin",
            "LPAREN": "(",
            "VAR_1": "x",
            "BINOP_INFIX_1": "pow",
            "CONS_1": "2",
            "RPAREN": ")",
            "BINOP_INFIX_2": "+",
            "CONS_2": "1",
            "BINOP_INFIX_3": "+",
            "FUNC_2": "log",
            "BINOP_PRFIX_1": "\\",
            "CONS_3": "1",
        }

        self._test_lexing(in_string, output, mapping)

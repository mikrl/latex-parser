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


class TestLexerUtilities(unittest.TestCase):
    """
    Test that the lexer utilities work correctly
    """

    def setUp(self):
        self.lexer = Lexer()

    def test_token_creation(self):
        """
        Tests the lexer can create a new token
        and unsupported tokens raise an error.
        """
        with self.assertRaises(TypeError):
            self.lexer._new_token("UNSUPPORTED")

        for token_type in [
            "CONS",
            "VAR",
            "BINOP_INFIX",
            "BINOP_PRFIX",
            "FUNC",
            "LPAREN",
            "RPAREN",
        ]:
            self.assertIsNotNone(
                re.match(f"{token_type}_[0-9]+", self.lexer._new_token(token_type))
            )

    def test_unlexed_indices(self):
        """
        Test that the unlexed indices are correctly computed.
        """
        in_string = r"\sin(x)"
        self.assertEqual(self.lexer.unlexed_indices, [])

        self.lexer.unlexed_indices = list(range(len(in_string)))
        self.lexer._lex_functions(in_string)

        self.assertEqual(self.lexer.unlexed_indices, [4, 5, 6])
        self.assertEqual(len(in_string) - len(self.lexer.unlexed_indices), len("\sin"))

    def test_effective_index(self):
        """
        Test that the effective index function works as intended.
        """
        in_string = r"\sin(x)"
        self.lexer.unlexed_indices = list(range(len(in_string)))
        self.lexer._lex_functions(in_string)
        self.assertEqual(self.lexer._effective_index(0), 4)

    def test_build_token_list(self):
        """
        Test that the token list builder constructs turns the dict into a list properly.
        """
        token_dict = {"CONS_1": 0, "BINOP_INFIX_1": 1, "CONS_2": 2}
        token_list = ["CONS_1", "BINOP_INFIX_1", "CONS_2"]
        self.lexer.token_index = token_dict
        built_list = self.lexer._build_token_list()
        self.assertEqual(built_list, token_list)


class TestLexerPasses(unittest.TestCase):
    """
    Test that the various stages of the lexer work correctly.
    """

    def setUp(self):
        self.lexer = Lexer()

    def _test_lexer_pass(self, lexer_pass, in_string, output, out_dict, symbol_mapping):
        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = lexer_pass(in_string)
        self.assertEqual(lexer_output, output)
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)

    def test_lex_single_variable(self):
        lexer_pass = self.lexer._lex_variables
        in_string = r"x"
        output = ""
        out_dict = {"VAR_1": 0}
        symbol_mapping = {"VAR_1": "x"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_multiple_variables(self):
        lexer_pass = self.lexer._lex_variables
        in_string = r"x+y+z+100"
        output = "+++100"
        out_dict = {"VAR_1": 0, "VAR_2": 2, "VAR_3": 4}
        symbol_mapping = {"VAR_1": "x", "VAR_2": "y", "VAR_3": "z"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_no_variables(self):
        lexer_pass = self.lexer._lex_variables
        in_string = r"{3}"
        output = "{3}"
        out_dict = {}
        symbol_mapping = {}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_single_literal(self):

        lexer_pass = self.lexer._lex_literals

        # Single Literal
        in_string = r"3"
        output = ""
        out_dict = {"CONS_1": 0}
        symbol_mapping = {"CONS_1": "3"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_double_literal(self):
        lexer_pass = self.lexer._lex_literals

        in_string = r"3+2"
        output = "+"
        out_dict = {"CONS_1": 0, "CONS_2": 2}
        symbol_mapping = {"CONS_1": "3", "CONS_2": "2"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_parens(self):

        lexer_pass = self.lexer._lex_parens

        in_string = r"()(){(3)}"
        output = "3"
        out_dict = {
            "LPAREN_1": 0,
            "RPAREN_1": 1,
            "LPAREN_2": 2,
            "RPAREN_2": 3,
            "LPAREN_3": 4,
            "LPAREN_4": 5,
            "RPAREN_3": 7,
            "RPAREN_4": 8,
        }
        symbol_mapping = {
            "LPAREN_1": "(",
            "RPAREN_1": ")",
            "LPAREN_2": "(",
            "RPAREN_2": ")",
            "LPAREN_3": "{",
            "LPAREN_4": "(",
            "RPAREN_3": ")",
            "RPAREN_4": "}",
        }

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_single_func(self):

        lexer_pass = self.lexer._lex_functions

        in_string = r"\sin(x)"
        output = "(x)"
        out_dict = {"FUNC_1": 0}
        symbol_mapping = {"FUNC_1": "sin"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)

    def test_lex_infix_binary_operator(self):

        lexer_pass = self.lexer._lex_infix_binops

        in_string = r"3+2"
        output = "32"
        out_dict = {"BINOP_INFIX_1": 1}
        symbol_mapping = {"BINOP_INFIX_1": "+"}

        self._test_lexer_pass(lexer_pass, in_string, output, out_dict, symbol_mapping)


class TestLexer(unittest.TestCase):
    """
    Test that the lexer successfully lexes things.
    """

    def setUp(self):
        self.lexer = Lexer()

    def _test_token_extraction(
        self, in_string, token_index, symbol_mapping, unlexed_indices
    ):
        """
        Helper test to verify token extraction works.
        """
        self.assertEqual(self.lexer.token_index, {})
        self.lexer._lex_functions(in_string)
        self.assertEqual(self.lexer.token_index, token_index)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)
        self.assertEqual(self.lexer.unlexed_indices, unlexed_indices)

    def test_function_pass1(self):
        in_string = r"\sin(x)"
        self.lexer.unlexed_indices = list(range(len(in_string)))
        token_index = {
            "FUNC_1": 0,
        }
        symbol_mapping = {"FUNC_1": "sin"}
        unlexed_indices = [4, 5, 6]
        self._test_token_extraction(
            in_string, token_index, symbol_mapping, unlexed_indices
        )

    def test_function_pass2(self):
        in_string = r"\sqrt{\sin(x^2)}"
        self.lexer.unlexed_indices = list(range(len(in_string)))
        token_index = {"FUNC_1": 0, "FUNC_2": 6}
        symbol_mapping = {"FUNC_1": "sqrt", "FUNC_2": "sin"}
        unlexed_indices = [5, 10, 11, 12, 13, 14, 15]
        self._test_token_extraction(
            in_string, token_index, symbol_mapping, unlexed_indices
        )

    def test_lexer_edge_cases(self):
        """
        Test null inputs and handling of spaces.
        """
        # Test that lexing nothing leads to an exception
        with self.assertRaises(TypeError):
            self.lexer.lex(None)
            self.lexer.lex()

        # Test that lexing a null string yields a null list
        self.assertEqual(self.lexer.lex(""), [])

        # Test that a string of spaces yields a null list
        for i in range(0, 512):
            spaces = " " * i
            self.assertEqual(self.lexer.lex(spaces), [])

        # Test that adding spaces into an input yields the same output
        in_string = r""
        lexed_string = self.lexer.lex(in_string)
        for i in range(1, 128):
            spaced_string = _insert_spaces(in_string, i)
            self.assertEqual(self.lexer.lex(spaced_string), lexed_string)

    def _test_lexing(self, in_string: str, output: List[str], mapping: Dict[str, str]):
        """
        Utility function to test that the lexer lexes and maps correctly.
        """
        lexer_output = self.lexer.lex(in_string)
        self.assertEqual(lexer_output, output)
        for token in lexer_output:
            if token not in ["LPAREN", "RPAREN"]:
                self.assertEqual(self.lexer.symbol_mapping[token], mapping[token])

    def test_lexes_simple_equation(self):
        """
        Tests that when passed simple latex, the lexer lexes correctly.
        """
        in_string = r"3+2"
        output = ["CONS_1", "BINOP_INFIX_1", "CONS_2"]
        mapping = {"CONS_1": "3", "BINOP_INFIX_1": "+", "CONS_2": "2"}
        self._test_lexing(in_string, output, mapping)

    def test_lexes_variable_equation(self):
        """
        Test that the lexer can handle an equation with free variables.
        """
        in_string = r"x^{3} + 2x -1"
        output = [
            "VAR_1",
            "BINOP_INFIX_1",
            "LPAREN",
            "CONS_1",
            "RPAREN",
            "BINOP_INFIX_2",
            "CONS_2",
            "VAR_2",
            "BINOP_INFIX_3",
            "CONS_3",
        ]
        mapping = {
            "VAR_1": "x",
            "BINOP_INFIX_1": "expt",
            "CONS_1": "3",
            "BINOP_INFIX_2": "+",
            "CONS_2": "2",
            "VAR_2": "x",
            "BINOP_INFIX_3": "-",
            "CONS_3": "1",
        }

        self._test_lexing(in_string, output, mapping)

    def test_lex_easy_function(self):
        """
        Test that the lexer can handle an easy function
        """
        in_string = r"\sqrt{4}"
        output = [
            "FUNC_1",
            "LPAREN",
            "CONS_1",
            "RPAREN",
        ]
        mapping = {
            "FUNC_1": "sqrt",
            "CONS_1": "4",
        }

        self._test_lexing(in_string, output, mapping)

    def test_lex_hard_function(self):
        """
        Test that the lexer can handle a complicated function.
        """
        in_string = r"\sin(x^{2}+1) + \ln(\frac{1}{x})"
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
            "LPAREN",
            "BINOP_PRFIX_1",
            "LPAREN",
            "CONS_3",
            "RPAREN",
            "LPAREN",
            "VAR_2",
            "RPAREN",
            "RPAREN",
        ]
        mapping = {
            "FUNC_1": "sin",
            "LPAREN": "(",
            "VAR_1": "x",
            "BINOP_INFIX_1": "expt",
            "CONS_1": "2",
            "RPAREN": ")",
            "BINOP_INFIX_2": "+",
            "CONS_2": "1",
            "BINOP_INFIX_3": "+",
            "FUNC_2": "nat_log",
            "BINOP_PRFIX_1": "prefix_div",
            "CONS_3": "1",
            "VAR_2": "x",
        }
        self._test_lexing(in_string, output, mapping)

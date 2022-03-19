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

        for token_type in ["CONS", "VAR", "BINOP_INFIX", "BINOP_PRFIX"]:
            self.assertIsNotNone(
                re.match(f"{token_type}_[0-9]+", self.lexer._new_token(token_type))
            )

    def test_unlexed_indices(self):
        """
        Test that the unlexed indices are correctly computed.
        """
        in_string = "\sin(x)"
        self.assertEqual(self.lexer.unlexed_indices, [])

        self.lexer.unlexed_indices = list(range(len(in_string)))
        self.lexer._lex_functions(in_string)

        self.assertEqual(self.lexer.unlexed_indices, [4, 5, 6])
        self.assertEqual(len(in_string) - len(self.lexer.unlexed_indices), len("\sin"))

    def test_effective_index(self):
        """
        Test that the effective index function works as intended.
        """
        in_string = "\sin(x)"
        self.lexer.unlexed_indices = list(range(len(in_string)))
        self.lexer._lex_functions(in_string)
        self.assertEqual(self.lexer._effective_index(0), 4)


class TestLexerPasses(unittest.TestCase):
    """
    Test that the various stages of the lexer work correctly.
    """

    def setUp(self):
        self.lexer = Lexer()

    def test_lex_single_var(self):
        in_string = "x"
        out_dict = {"VAR_1": 0}
        symbol_mapping = {"VAR_1": "x"}

        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = self.lexer._lex_variables(in_string)
        self.assertEqual(lexer_output, "")
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)

    def test_lex_single_lit(self):
        in_string = "3"
        out_dict = {"CONS_1": 0}
        symbol_mapping = {"CONS_1": "3"}

        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = self.lexer._lex_literals(in_string)
        self.assertEqual(lexer_output, "")
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)

    def test_lex_double_lit(self):
        in_string = "3+2"
        out_dict = {"CONS_1": 0, "CONS_2": 2}
        symbol_mapping = {"CONS_1": "3", "CONS_2": "2"}

        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = self.lexer._lex_literals(in_string)
        self.assertEqual(lexer_output, "+")
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)

    def test_lex_single_func(self):
        in_string = "\sin(x)"
        out_dict = {"FUNC_1": 0}
        symbol_mapping = {"FUNC_1": "sin"}

        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = self.lexer._lex_functions(in_string)
        self.assertEqual(lexer_output, "(x)")
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)

    def test_lex_binary_operator(self):
        in_string = "3+2"
        out_dict = {"BINOP_INFIX_1": 1}
        symbol_mapping = {"BINOP_INFIX_1": "+"}

        self.lexer.unlexed_indices = list(range(len(in_string)))
        lexer_output = self.lexer._lex_operators(in_string)
        self.assertEqual(lexer_output, "32")
        self.assertEqual(self.lexer.token_index, out_dict)
        self.assertEqual(self.lexer.symbol_mapping, symbol_mapping)


# @unittest.skip("Need to test lower level stuff first")
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
        in_string = "\sin(x)"
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
        in_string = "\sqrt{\sin(x**2)}"
        self.lexer.unlexed_indices = list(range(len(in_string)))
        token_index = {"FUNC_1": 0, "FUNC_2": 6}
        symbol_mapping = {"FUNC_1": "sqrt", "FUNC_2": "sin"}
        unlexed_indices = [5, 10, 11, 12, 13, 14, 15, 16]
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
        for i in range(0, 1024):
            spaces = " " * i
            self.assertEqual(self.lexer.lex(spaces), [])

        # Test that adding spaces into an input yields the same output
        in_string = ""
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
            self.assertEqual(self.lexer.symbol_table[token], mapping[token])

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

    @unittest.skip("Need to test lower level stuff first")
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

    @unittest.skip("Need to test lower level stuff first")
    def test_lex_easy_function(self):
        """
        Test that the lexer can handle an easy function
        """
        in_string = "\sqrt{4}"
        output = [
            "FUNC_1",
            "LPAREN",
            "CONS_1",
            "RPAREN",
        ]
        mapping = {
            "FUNC_1": "sqrt",
            "LPAREN": "(",
            "CONS_1": "4",
            "RPAREN": ")",
        }
        self._test_lexing(in_string, output, mapping)

    @unittest.skip("Need to test lower level stuff first")
    def test_lex_hard_function(self):
        """
        Test that the lexer can handle a complicated function.
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

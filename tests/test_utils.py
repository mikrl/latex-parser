import unittest

from latex_parser.lexer import Lexer

from latex_parser.utilities import idx_of_first_operator
from latex_parser.utilities import idx_of_second_operator
from latex_parser.utilities import rpn_to_ast


@unittest.skip("Need to rethink these tests")
class TestIndexOfOperators(unittest.TestCase):
    """
    Tests whether the index_of_operator functions return the correct index.
    """

    def test_idx_of_first_operator(self):
        first_inp_1 = r"$(3*sin(\pi^2)+1)/2$"

        # intermediate_1 = r'3 \pi 2 ^ sin *'
        first_out_1 = 3
        self.assertEqual(idx_of_first_operator(first_inp_1), first_out_1)

        first_inp_2 = r"$(1+3) * (2+4)$"
        # intermediate_2 = r'1 3 + 2 4 + *'
        first_out_2 = 2
        self.assertEqual(idx_of_first_operator(first_inp_2), first_out_2)

    def test_idx_of_second_operator(self):
        second_inp_1 = r"$(3*sin(\pi^2)+1)/2$"

        # intermediate_1 = r'3 \pi 2 ^ sin *'
        second_out_1 = 4
        self.assertEqual(idx_of_second_operator(second_inp_1), second_out_1)

        second_inp_2 = r"$(1+3) * (2+4)$"
        # intermediate_2 = r'1 3 + 2 4 + *'
        second_out_2 = 5
        self.assertEqual(idx_of_second_operator(second_inp_2), second_out_2)

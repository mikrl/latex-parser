import unittest

from parser import lexer
from parser import shunting_yard
from parser import idx_of_first_operator
from parser import idx_of_second_operator
from parser import rpn_to_ast


class TestLexer(unittest.TestCase):

    def setUp(self):
        self.lexer = lexer()

    def test_lexes_latex(self):
        inp_1 = None
        out_1 = [None]
        self.assertEqual(self.lexer.lex(inp_1), out_1)

        inp_2 = None
        out_2 = [None]
        self.assertEqual(self.lexer.lex(inp_2), out_2)

    def test_builtin_literals(self):
        literal_table = self.lexer.literal_table
        # Rudimentary list for now!
        scanlist_fns = ['\\arccos',  '\\cos',   '\\csc',  '\\exp', '\\min',
                        '\\sinh', '\\arcsin',  '\\cosh',  '\\deg',  '\\gcd',
                        '\\lg', '\\ln', '\\arctan',  '\\cot', '\\det',
                        '\\log', '\\sec', '\\tan', '\\arg', '\\coth',  '\\dim',
                        '\\inf', '\\max', '\\sin',  '\\tanh', ]
        scanlist_greeks = []


        [self.assertIn(literal, literal_table)
         for literal in scanlist_fns + scanlist_greeks]


class TestShuntingYard(unittest.TestCase):
    """
    Tests the shunting yard algorithm for correctness.
    Should transform a latex equation input into RPN.
    """
    def test_transforms_latex(self):
        inp_1 = r'$(3*sin(\pi^2)+1)/2$'
        out_1 = r'3 \pi 2 ^ sin *'
        self.assertEqual(shunting_yard(inp_1), out_1)

        inp_2 = r'$(1+3) * (2+4)$'
        out_2 = r'1 3 + 2 4 + *'
        self.assertEqual(shunting_yard(inp_2), out_2)


class TestIndexOfOperators(unittest.TestCase):
    """
    Tests whether the index_of_operator functions return the correct index.
    """
    def test_idx_of_first_operator(self):
        first_inp_1 = r'$(3*sin(\pi^2)+1)/2$'
        # intermediate_1 = r'3 \pi 2 ^ sin *'
        first_out_1 = 3
        self.assertEqual(idx_of_first_operator(first_inp_1), first_out_1)

        first_inp_2 = r'$(1+3) * (2+4)$'
        # intermediate_2 = r'1 3 + 2 4 + *'
        first_out_2 = 2
        self.assertEqual(idx_of_first_operator(first_inp_2), first_out_2)

    def test_idx_of_second_operator(self):
        second_inp_1 = r'$(3*sin(\pi^2)+1)/2$'
        # intermediate_1 = r'3 \pi 2 ^ sin *'
        second_out_1 = 4
        self.assertEqual(idx_of_second_operator(second_inp_1), second_out_1)

        second_inp_2 = r'$(1+3) * (2+4)$'
        # intermediate_2 = r'1 3 + 2 4 + *'
        second_out_2 = 5
        self.assertEqual(idx_of_second_operator(second_inp_2), second_out_2)

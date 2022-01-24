import unittest

from latex-parser.lexer import Lexer

from latex-parser.utilities import idx_of_first_operator
from latex-parser.utilities import idx_of_second_operator
from latex-parser.utilities import rpn_to_ast


class TestFunctions(unittest.TestCase):
    def setUp(self):
        
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

class TestParser(unittest.TestCase):

    
    def setUp(self):
        self.parser = LatexParser()

    def test_parser_simple(self):
        inp = r'$(1+3) * (2+4)$'
        out = r'1 3 + 2 4 + *'
        self.assertEqual(self.parser(inp), out)
        
    def test_parser_medium(self):
        inp = r'$(3*sin(\pi^2)+1)/2$'
        out = r'3 \pi 2 ^ sin *'
        self.assertEqual(self.parser(inp), out)
        

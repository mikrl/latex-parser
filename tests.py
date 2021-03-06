
import unittest

from parser import shunting_yard
from parser import idx_of_first_operator
from parser import idx_of_second_operator
from parser import rpn_to_ast

# Shunting yard tests
inp_1 = r'$(3*sin(\pi^2)+1)/2$'
out_1 = r'3 \pi 2 ^ sin *'

inp_2 = r'$(1+3) * (2+4)$'
out_2 = r'1 3 + 2 4 + *'

# idx_of_ tests
first_inp_1 = r'$(3*sin(\pi^2)+1)/2$'
first_int_1 = r'3 \pi 2 ^ sin *'
first_out_1 = 3

first_inp_2 = r'$(1+3) * (2+4)$'
first_int_2 = r'1 3 + 2 4 + *'
first_out_2 = 2

second_inp_1 = r'$(3*sin(\pi^2)+1)/2$'
second_int_1 = r'3 \pi 2 ^ sin *'
second_out_1 = 4

second_inp_2 = r'$(1+3) * (2+4)$'
second_int_2 = r'1 3 + 2 4 + *'
second_out_2 = 5

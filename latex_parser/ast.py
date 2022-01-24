"""
AST factory class to create AST from rpn string
"""

import ast
import math

import numpy

symbol_mapping = {
    # Trig functions
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sec': math.sec,
    'cot': math.cot,
    'cosec': math.cosec,
    # Hyperbolic trig functions
    'sinh': math.sinh,
    'cosh': math.cosh,
    'tanh': math.tanh,
    'sech': math.sech,
    'coth': math.coth,
    #  Functions
    'abs': abs,
    'pow': pow,
    'max': max,
    'min': min,
    
    }

class FunctionTreeFactory:
    def __init__():
        pass


    def create_trig_function(symbol: str):
        if symbol == 'sin':
            function = math.sin
        if symbol == 'cos':
            function = math.cos
        if symbol == 'tan':
            function = math.tan
        ast.Lambda(
        pass

    def create_
        
    
    def create_AST(rpn_string: str)-> ast.AST:
        
        
        pass







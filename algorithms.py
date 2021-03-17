import queue
import re
from typing import List

class ShuntingYardError(Exception):
    """Base class for other shunting yard exceptions"""
    pass

class UnknownTokenError(Exception):
    """Raised when encountering a token that is not a parenthesis, literal, variable, or operator"""
    pass

class NoOuterParentheses(ShuntingYardError):
    """Raised when the input string hasn't been prepared to have outer parens"""
    pass

class MismatchedParenthesesError(ShuntingYardError):
    """Raised when mismatched parentheses lead to an undefined stack operation"""
    pass

def to_token_list(parse_str: str) -> List[str]:
    # valid_token_regex = re.compile(r'^((OPb|OPu|LIT|VAR)[0-9]+|\(|\))')
    valid_token_regex = re.compile(r'^((OP|LIT|VAR)[0-9]+|\(|\))')
    token_list = []
    while len(parse_str)>0:
        if valid_token_regex.match(parse_str):
            token_end_idx = valid_token_regex.match(parse_str).span()[1]
            next_token = parse_str[:token_end_idx]
            parse_str = parse_str[token_end_idx:]
            token_list.append(next_token)
        else:
            raise UnknownTokenError("Encountered an unrecognized token!\
            Lexer didn't catch {0}".format(parse_str))
    return token_list

def shunting_yard(parse_str: str) -> str:
    """
    Implementation of the shunting yard algorithm.
    Assumes that the input is parenthesized to resolve precedence ambiguity.
    Assumes that all literals have been replaced with LITx, where x is a positive integer.
    Assumes that all variables have been replaced with VARx, where x is a positive integer.
    Assumes that all operators have been replaced with OPx, where x is a positive integer. 
    # Assumes that all binary operators have been replaced with OPbx, where x is a positive integer. 
    # Assumes that all unary operators have been replaced with OPux, where x is a positive integer.
    """
    
    in_queue = to_token_list(parse_str)
    out_queue = []
    op_stack = []
    
    for token in in_queue:
        if token[:3] in ['LIT', 'VAR']:
            out_queue.append(token)
        elif token[:2] == 'OP':
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            # Pop operators off the stack until we find the matching parenthesis
            while op_stack[-1] != '(':
                if len(op_stack) == 0:
                    raise MismatchedParenthesesError("Emptied the stack while searching for a L_PAREN!")
                out_queue.append(op_stack.pop())
            op_stack.pop() # Pop off the left parenthesis
    if len(op_stack) > 0:
        raise NoOuterParentheses("Input as prepared did not have outer parentheses!")
    return out_queue














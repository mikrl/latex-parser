
import re
from typing import List
from typing import Tuple


class ShuntingYardError(Exception):
    """Base class for other shunting yard exceptions"""
    pass


class UnknownTokenError(Exception):
    """Raised when encountering a token that is not a parenthesis, literal, variable, or operator"""
    pass


class NoOuterParenthesesError(ShuntingYardError):
    """Raised when the input string hasn't been prepared to have outer parens"""
    pass


class OperatorsOnStackError(ShuntingYardError):
    """Raised when the operator stack still holds operators when the algorithm terminates."""
    pass


class MismatchedParenthesesError(ShuntingYardError):
    """Raised when mismatched parentheses lead to an undefined stack operation"""
    pass


def to_token_list(parse_str: str) -> Tuple[List[str], int]:
    """
    Transforms the preprocessed parse string into a list of tokens.
    Also returns a 0 when tokenizing succeeded, or a 1 if it failed.

    Keyword arguments:
    parse_str -- The preprocessed infix string to be tokenized.
    """
    valid_token_regex = re.compile(r'^((OP|LIT|VAR)[0-9]+|\(|\))')
    token_list = []
    while len(parse_str) > 0:
        if valid_token_regex.match(parse_str):
            token_end_idx = valid_token_regex.match(parse_str).span()[1]
            next_token = parse_str[:token_end_idx]
            parse_str = parse_str[token_end_idx:]
            token_list.append(next_token)
        else:
            return ([parse_str], 1)

    return (token_list, 0)


def shunting_yard(parse_str: str) -> str:
    """
    Implementation of the shunting yard algorithm.

    Assumptions:
    The input is parenthesized to resolve operator precedence ambiguity.
    The first and last characters are L and R parens respectively.
    All literals have been replaced with LITx, where x is a positive integer.
    All variables have been replaced with VARx, where x is a positive integer.
    All operators have been replaced with OPx, where x is a positive integer.

    Keyword arguments:
    parse_str -- The preprocessed infix string to be parsed.
    """

    if parse_str[0] != "(" and parse_str[-1] != ")":
        raise NoOuterParenthesesError(
            "Input as prepared did not have outer parentheses!")

    out_queue = []
    op_stack = []

    in_queue, error = to_token_list(parse_str)
    
    if error:
        raise UnknownTokenError(
            "Encountered an unrecognized token!\
            Lexer didn't catch {0}".format(in_queue[0]))

    for token in in_queue:
        if token[:3] in ['LIT', 'VAR']:
            out_queue.append(token)
        elif token[:2] == 'OP':
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            # Pop operators off the stack
            # until we find the matching parenthesis
            while op_stack[-1] != '(':
                if len(op_stack) == 0:
                    raise MismatchedParenthesesError(
                        "Emptied the stack while searching for a L_PAREN!")
                out_queue.append(op_stack.pop())
            # Pop off the left parenthesis
            op_stack.pop()
    if len(op_stack) > 0:
        raise OperatorsOnStackError(
            "Operators left on stack at algorithm termination!")
    return out_queue














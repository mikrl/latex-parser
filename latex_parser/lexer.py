from typing import Dict, List
import re

# Separate these out so can add Greeks etc
_LETTER = "[a-zA-Z]"
_ALPHANUM = "[a-zA-Z0-9]"
_NUMBER = "[0-9]+"
_IFX_BINARY_OPERATORS = "\+|-|\*|/|\^"

# Only supports single subscript depth. Subscripts must be alphanumeric.
_SUBSCR = f"_{_ALPHANUM}+|_\\{{{_ALPHANUM}+\\}}"
_SUPSCR = f"\^{_ALPHANUM}+|\^\\{{{_ALPHANUM}+\\}}"
_LPAREN = "\(|\[|\{"
_RPAREN = "\)|\]|\}"
_LITERAL = f"{_NUMBER}"
_VARIABLE = f"{_LETTER}+({_SUBSCR})*"
_FUNCTION = f"\\\{_LETTER}+({_SUBSCR})*"


class Lexer:
    """
    A lexer for latex equations into generic tokens with a mapping.
    """

    def __init__(self):
        self.token_index = {}
        self.symbol_mapping = {}
        self.symbol_counters = {}
        self.unlexed_indices = []
        self.token_list = []

    def _new_token(self, token_type: str) -> str:
        """
        Generates a new, numbered token of a certain type

        :param token_type: the object type to which the token will refer
        :return: the token type with an incremented counter suffix
        """
        if token_type not in [
            "CONS",
            "VAR",
            "BINOP_INFIX",
            "BINOP_PRFIX",
            "FUNC",
            "LPAREN",
            "RPAREN",
        ]:
            raise TypeError(f"Unsupported token type: {token_type}")
        symbol_count = self.symbol_counters.get(token_type, 1)
        self.symbol_counters.update({token_type: symbol_count + 1})
        return f"{token_type}_{symbol_count}"

    def _build_token_list(self) -> List[str]:
        """
        Generates the token list from the accumulated token index

        :return: a list of tokens in order according to the lexer
        """
        token_dict = self.token_index
        token_list = sorted(token_dict, key=token_dict.get)
        for idx, token in enumerate(token_list):
            if "PAREN" in token:
                token_list[idx] = token.split("_")[0]
        return token_list

    def _effective_index(self, index: int) -> int:
        """
        Gets the effective index in the original string of an index in the reduced string.

        :param index: an index in the reduced string
        :return: the effective index of the index in the original input string
        """
        return self.unlexed_indices[index]

    def string_mask(self, in_string: str, mask: List[int]):
        return "".join([char for idx, char in enumerate(in_string) if idx in mask])

    def generate_lexer_pass(self, pass_regex: str, token_type: str):
        def _lexer_pass(self, in_string: str) -> str:

            pass_matcher = re.compile(pass_regex)
            match_indices = []
            for match in re.finditer(pass_matcher, in_string):
                token = self._new_token(token_type)
                token_name = match.group()
                self.symbol_mapping.update({token: token_name})

                start_idx = self._effective_index(match.start())
                self.token_index.update({token: start_idx})

                match_indices += list(range(match.start(), match.end()))

            effective_match_indices = [
                self._effective_index(idx) for idx in match_indices
            ]
            self.unlexed_indices = [
                _ for _ in self.unlexed_indices if _ not in effective_match_indices
            ]

            return self.string_mask(
                in_string,
                [idx for idx in range(len(in_string)) if idx not in match_indices],
            )

        return _lexer_pass

    def _lex_functions(self, in_string: str) -> str:
        """
        Tokenizes functions in the input string and adds them to the token index

        :param in_string: the input to be lexed
        :return: the input string with all functions removed
        """

        def _resolve_func_name(func_latex: str) -> str:
            func_mappings = {"\sin": "sin", "\sqrt": "sqrt", "\ln": "nat_log"}
            return func_mappings.get(func_latex, func_latex)

        function_lexer = self.generate_lexer_pass(_FUNCTION, "FUNC")
        tokenize_functions = function_lexer(self, in_string)
        for key, val in self.symbol_mapping.items():
            if "FUNC" in key:
                self.symbol_mapping.update({key: _resolve_func_name(val)})
        return tokenize_functions

    def _lex_lparens(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all lparens removed
        """
        lparen_lexer = self.generate_lexer_pass(_LPAREN, "LPAREN")
        tokenize_lparens = lparen_lexer(self, in_string)

        return tokenize_lparens

    def _lex_rparens(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all rparens removed
        """
        rparen_lexer = self.generate_lexer_pass(_RPAREN, "RPAREN")
        tokenize_rparens = rparen_lexer(self, in_string)

        return tokenize_rparens

    def _lex_parens(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all parens removed
        """
        lparen_lexer = self.generate_lexer_pass(_LPAREN, "LPAREN")
        rparen_lexer = self.generate_lexer_pass(_RPAREN, "RPAREN")

        for paren_pass in [lparen_lexer, rparen_lexer]:
            in_string = paren_pass(self, in_string)

        return in_string

    def _lex_variables(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all variables removed
        """
        variable_lexer = self.generate_lexer_pass(_VARIABLE, "VAR")
        tokenize_variables = variable_lexer(self, in_string)
        return tokenize_variables

    def _lex_literals(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all literals removed
        """
        literal_lexer = self.generate_lexer_pass(_LITERAL, "CONS")
        tokenize_literals = literal_lexer(self, in_string)
        return tokenize_literals

    def _lex_infix_binops(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all operators removed
        """

        def _resolve_binop_name(binop_latex: str) -> str:
            binop_mappings = {"^": "expt"}
            return binop_mappings.get(binop_latex, binop_latex)

        operator_lexer = self.generate_lexer_pass(_IFX_BINARY_OPERATORS, "BINOP_INFIX")
        tokenize_operators = operator_lexer(self, in_string)
        for key, val in self.symbol_mapping.items():
            if "BINOP_INFIX" in key:
                self.symbol_mapping.update({key: _resolve_binop_name(val)})
        return tokenize_operators

    def lex(self, in_string: str):

        self.unlexed_indices = list(range(len(in_string)))
        lexer_passes = [
            self._lex_functions,
            self._lex_variables,
            self._lex_literals,
            self._lex_infix_binops,
            self._lex_parens,
        ]
        for lpass in lexer_passes:
            in_string = lpass(in_string)

        output = self._build_token_list()
        return output

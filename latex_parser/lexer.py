from typing import Dict, List
import re

# Separate these out so can add Greeks etc
_LETTER = "[a-zA-Z]"
_ALPHANUM = "[a-zA-Z0-9]"
_NUMBER = "[0-9]+"
_BINARY_OPERATORS = "\+|-|\*|/"

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

    def _new_token(self, token_type):
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
        token_dict = self.token_index
        token_list = sorted(token_dict, key=token_dict.get)
        for idx, token in enumerate(token_list):
            if "PAREN" in token:
                token_list[idx] = token.split("_")[0]
        return token_list

    def _effective_index(self, index):
        return self.unlexed_indices[index]

    def string_mask(self, in_string: str, mask: List[int]):
        return "".join([char for idx, char in enumerate(in_string) if idx in mask])

    def _lex_functions(self, in_string: str) -> str:
        """
        Tokenizes functions in the input string and adds them to the token index

        :param in_string: the input to be lexed
        :return: the input string with all functions removed
        """
        function_regex = re.compile(_FUNCTION)

        def _resolve_func_name(func_latex: str) -> str:
            func_mappings = {"\sin": "sin", "\sqrt": "sqrt", "\ln": "nat_log"}
            if mapped := func_mappings.get(func_latex):
                return mapped
            raise NotImplementedError(f"{func_latex}")

        match_indices = []
        for function_match in re.finditer(function_regex, in_string):
            func_token = self._new_token("FUNC")
            resolved_func_name = _resolve_func_name(function_match.group())
            self.symbol_mapping.update({func_token: resolved_func_name})

            start_idx = self._effective_index(function_match.start())
            self.token_index.update({func_token: start_idx})

            match_indices += list(range(function_match.start(), function_match.end()))
        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def _lex_lparens(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all parens removed
        """
        match_indices = []

        lparen_regex = re.compile(_LPAREN)
        for lparen_match in re.finditer(lparen_regex, in_string):
            lparen_token = self._new_token("LPAREN")
            start_idx = self._effective_index(lparen_match.start())
            self.token_index.update({lparen_token: start_idx})

            match_indices += list(range(lparen_match.start(), lparen_match.end()))

        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def _lex_parens(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all parens removed
        """
        match_indices = []

        lparen_regex = re.compile(_LPAREN)
        for lparen_match in re.finditer(lparen_regex, in_string):
            lparen_token = self._new_token("LPAREN")
            start_idx = self._effective_index(lparen_match.start())
            self.token_index.update({lparen_token: start_idx})

            match_indices += list(range(lparen_match.start(), lparen_match.end()))

        rparen_regex = re.compile(_RPAREN)
        for rparen_match in re.finditer(rparen_regex, in_string):
            rparen_token = self._new_token("RPAREN")
            start_idx = self._effective_index(rparen_match.start())
            self.token_index.update({rparen_token: start_idx})

            match_indices += list(range(rparen_match.start(), rparen_match.end()))

        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def _lex_variables(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all variables removed
        """
        variable_regex = re.compile(_VARIABLE)

        match_indices = []
        for variable_match in re.finditer(variable_regex, in_string):
            var_token = self._new_token("VAR")
            var_name = variable_match.group()
            self.symbol_mapping.update({var_token: var_name})

            start_idx = self._effective_index(variable_match.start())
            self.token_index.update({var_token: start_idx})

            match_indices += list(range(variable_match.start(), variable_match.end()))
        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        # breakpoint()
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def _lex_literals(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all literals replaced with CONS tokens
        """
        literal_regex = re.compile(_LITERAL)

        match_indices = []
        for literal_match in re.finditer(literal_regex, in_string):
            lit_token = self._new_token("CONS")
            lit_name = literal_match.group()
            self.symbol_mapping.update({lit_token: lit_name})

            start_idx = self._effective_index(literal_match.start())
            self.token_index.update({lit_token: start_idx})

            match_indices += list(range(literal_match.start(), literal_match.end()))
        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def _lex_operators(self, in_string: str) -> str:
        """
        :param in_string: the input to be lexed
        :return: the input with all operators replaced with BINOP_x tokens
        """
        binop_regex = re.compile(_BINARY_OPERATORS)

        match_indices = []
        for operator_match in re.finditer(binop_regex, in_string):
            binop_token = self._new_token("BINOP_INFIX")
            binop_name = operator_match.group()
            self.symbol_mapping.update({binop_token: binop_name})

            start_idx = self._effective_index(operator_match.start())
            self.token_index.update({binop_token: start_idx})

            match_indices += list(range(operator_match.start(), operator_match.end()))
        self.unlexed_indices = [
            _ for _ in self.unlexed_indices if _ not in match_indices
        ]
        return self.string_mask(
            in_string,
            [idx for idx in range(len(in_string)) if idx not in match_indices],
        )

    def lex(self, in_string: str):
        output = []
        token_list = []
        self.unlexed_indices = list(range(len(in_string)))
        tokenize_functions = self._lex_functions(in_string)
        tokenize_variables = self._lex_variables(tokenize_functions)
        tokenize_literals = self._lex_literals(tokenize_variables)
        tokenize_operators = self._lex_operators(tokenize_literals)
        tokenize_parens = self._lex_parens(tokenize_operators)
        output = self._build_token_list()
        return output

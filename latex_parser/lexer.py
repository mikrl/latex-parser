import re

# Separate these out so can add Greeks etc
_LETTER = "[a-zA-Z]"
_ALPHANUM = "[a-zA-Z0-9]"
_NUMBER = "[0-9]+"

# Only supports single subscript depth. Subscripts must be alphanumeric.
_SUBSCR = f"_{_ALPHANUM}+|_\\{{{_ALPHANUM}+\\}}"
_SUPSCR = f"\^{_ALPHANUM}+|\^\\{{{_ALPHANUM}+\\}}"
_LPAREN = "\(|\[|\{"
_RPAREN = "\)|\]|\}"
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

    def _new_token(self, token_type):
        if token_type not in ["CONS", "VAR", "BINOP_INFIX", "BINOP_PRFIX", "FUNC"]:
            raise TypeError("Unsupported token type")
        symbol_count = self.symbol_counters.get(token_type, 1)
        self.symbol_counters.update({token_type: symbol_count + 1})
        return f"{token_type}_{symbol_count}"

    def _effective_index(self, index):
        return self.unlexed_indices[index]

    def _reduced_in_string(self, in_string):
        return "".join(
            [char for idx, char in enumerate(in_string) if char in self.unlexed_indices]
        )

    def _lex_functions(self, in_string: str):

        function_regex = re.compile(_FUNCTION)

        def _resolve_func_name(func_latex: str):
            func_mappings = {"\sin": "sin", "\sqrt": "sqrt"}
            if mapped := func_mappings.get(func_latex):
                return mapped
            raise NotImplementedError

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
        return self._reduced_in_string(in_string)

    def lex(self, in_string: str):
        output = []
        token_list = []
        self.unlexed_indices = list(range(len(in_string)))
        self._lex_functions(in_string)

        raise NotImplementedError
        return output

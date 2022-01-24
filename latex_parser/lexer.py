import re


FUNCTION = re.compile(r"(\\)([a-zA-Z]+)(\(.*\))")
NUMBER = re.compile("[0-9]+")
ARITHMETIC = re.compile(r"\+|\*|\/|-")
LPARENS = re.compile(r"")
RPARENS = re.compile(r"")


class Lexer:
    """
    A lexer for latex equations into generic tokens with a mapping.
    """

    def __init__(self):
        self.symbol_table = {}
        self.symbol_counters = {}
        self.cons_count = 0

    def _new_token(self, token_type):
        if token_type not in ["CONS", "VAR", "BINOP_INFIX", "BINOP_PRFIX"]:
            raise TypeError("Unsupported token type")
        symbol_count = self.symbol_counters.get(token_type, 1)
        self.symbol_counters.update({token_type: symbol_count + 1})
        return f"{token_type}_{symbol_count}"

    def lex(self, in_string: str):
        output = []
        tok_string = ""
        token_list = []
        while match := NUMBER.search(in_string):
            constant_token = self._new_token("CONS")
            match_content = match.group()
            self.symbol_table.update({constant_token: match_content})

            match_end = match.span()[1]
            match_string = in_string[:match_end]
            match_string = match_string.replace(match_content, constant_token)
            token_list.append(match_string)
            in_string = in_string[match_end:]

        in_string = "".join(token_list)

        tok_string = re.sub(r"[ ]+", " ", tok_string)
        output = [token for token in tok_string.split(" ") if token]

        return output

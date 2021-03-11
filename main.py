
import sys

from parser import LatexParser


def main(parse_str: str):
    latex_parser = LatexParser()
    parsed_str = latex_parser.parse(parse_string=parse_str)
    ast = latex_parser.to_ast(parse_string=parse_str)
    print("RPN: {}", parsed_str)
    print("AST: {}", ast)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        main(arg)

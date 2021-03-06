
from parser import Parser


def main(parse_str: str):
    parsed_str = Parser.parse(parse_str)
    ast = Parser.to_ast(parse_str)
    print("RPN: {}", parsed_str)
    print("AST: {}", ast)


if __name__() == '__main__':
    parse_str = r'$(3*sin(\pi^2)+1)/2$'
    main(parse_str)


from parser import Parser


def main(parse_str: str):
    parsed_str = Parser.parse(parse_str)
    ast = Parser.to_ast(parse_str)
    print("RPN: {}", parsed_str)
    print("AST: {}", ast)


if __name__() == '__main__':
    parse_str_1 = r'$(3*sin(\pi^2)+1)/2$'  # input str
    paren_rpn_str_1 = r'( 3 ( ( \pi 2 ^) sin) *)'  # output in RPN with parens
    noparen_rpn_str_1 = r'3 \pi 2 ^ sin *'  # output ion RPN with no parens

    parse_str_2 = r'$(1+3) * (2+4)$'
    paren_rpn_str_2 = r'( ( 1 3 +) ( 2 4 +) *)'
    noparen_rpn_str_2 = r'1 3 + 2 4 + *'
    
    main(parse_str)

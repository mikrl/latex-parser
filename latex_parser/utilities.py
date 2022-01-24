import ast

def isUnary(operator: str) -> bool:
    raise NotImplementedError("isUnary not implemented!")


def isBinary(operator: str) -> bool:
    raise NotImplementedError("isBinary not implemented!")


def isOperator(operator: str) -> bool:
    raise NotImplementedError("isOperator not implemented!")


def idx_of_first_operator(rpn_str: str) -> int:
    next(token for token in rpn_str.split(" ") if isOperator(token))


def idx_of_second_operator(rpn_str: str) -> int:
    rpn_substr = rpn_str[idx_of_first_operator(rpn_str)]
    return idx_of_first_operator(rpn_substr)


def rpn_to_ast(rpn_str: str) -> ast.AST:
    rpn_list = rpn_str.split(" ")
    idx_operator = len(rpn_list)-1
    operator = rpn_list[idx_operator]

    if isUnary(operator):
        idx_op_1 = idx_of_first_operator(rpn_str)

        if idx_op_1 == len(rpn_str) - 1:
            # construct the unary sub-AST directly here and return
            raise NotImplementedError("[!] Construct unary AST not implemented!")

        rpn_substr_unary = " ".join()
        # construt the unary AST from its sub ASTs
        raise NotImplementedError("[!] Construct inner unary AST not implemented!")

    elif isBinary(operator):
        idx_op_1 = idx_of_first_operator(rpn_str)

        if idx_op_1 == len(rpn_str) - 1:
            # construct the binary sub-AST directly here and return
            raise NotImplementedError("[!] Construct binary AST not implemented!")
        idx_op_2 = idx_of_second_operator(rpn_str)

        rpn_substr_l = " ".join(rpn_list[:idx_op_1])
        rpn_substr_r = " ".join(rpn_list[idx_op_1:idx_op_2])

        l_ast = rpn_to_ast(rpn_substr_l)
        r_ast = rpn_to_ast(rpn_substr_r)

        # construct the binary AST from its sub ASTs
        raise NotImplementedError("[!] Construct inner binary AST not implemented!")

    else:
        raise NotImplementedError("[!] Operator {} not recognised!", operator)

from src.calculate import calc
from src.tokenizer import is_num, is_operator


def calculate_rpn(rpn_exp: list) -> float:
    """вычисляет выражение, введенное в обратной польской нотации"""
    stack = []
    for tk in rpn_exp:
        if is_operator(tk):
            if tk in ["~", "$"]:
                if len(stack) == 0:
                    raise SyntaxError("Не хватает чисел на операцию")
                operand1 = stack.pop()
                res = calc(operand1, None, tk)
                stack.append(res)
            else:
                if len(stack) <= 1:
                    raise SyntaxError("Не хватает чисел на операцию")
                operand1 = stack.pop()
                operand2 = stack.pop()
                res = calc(operand1, operand2, tk)
                stack.append(res)
        else:
            stack.append(tk)
    return stack[0]

from src.calculate import calc
from src.tokenizer import isNum, isOperator


def calculate_rpn(rpn_exp: list()) -> float:
    stack = []
    for tk in rpn_exp:
        if isOperator(tk):
            if len(stack) <= 1:
                raise SyntaxError("Не хватает чисел на операцию")
            operand1 = stack.pop()
            operand2 = stack.pop()
            res = calc(operand1, operand2, tk)
            stack.append(res)
        else:
            stack.append(tk)
    return stack[0]

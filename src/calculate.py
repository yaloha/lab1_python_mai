from src.tokenizer import is_operator


def calc(op1: int|float, op2: int|float|None, oper: str) -> int|float:
    """выполняет введенную операцию над операндами (или одним операндом)"""
    match oper:
        case "+":
            return op1 + op2
        case "-":
            return op2 - op1
        case "*":
            return op1 * op2
        case "/":
            if op2 == 0:
                raise ZeroDivisionError("Нельзя делить на ноль")
            return op2 / op1
        case "//":
            if op2 == 0:
                raise ZeroDivisionError("Нельзя делить на ноль")
            elif type(op1) == float or type(op2) == float:
                raise TypeError("Операцию нельзя производить над вещественными числами")
            return op2 // op1
        case "%":
            if op2 == 0:
                raise ZeroDivisionError("Нельзя делить на ноль")
            elif type(op1) == float or type(op2) == float:
                raise TypeError("Операцию нельзя производить над вещественными числами")
            return op2 % op1
        case "**":
            if op2 < 0 and type(op1) == float:
                raise TypeError("Операцию нельзя проводить над отрицательными числами")
            return op2 ** op1
        case "~":
            return -op1
        case "$":
            return op1


def calculate_rpn(rpn_exp: list) -> int|float:
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
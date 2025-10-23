def calc(op1: int|float, op2: int|float, oper: str) -> int|float:
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
            return op2 ** op1
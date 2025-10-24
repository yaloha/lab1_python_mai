import re

from src.priority import op_priority


def isNum(t: str) -> bool:
    nums = [str(i) for i in range(10)]
    t = t.replace('.', '', 1)
    t = t.replace('-', '', 1)

    for symb in t:
        if symb not in nums:
            return False
    if len(t) == 0:
        return False
    return True

def isOperator(t: str) -> bool:
    return t in ["**", "*", "/", "//", "%", "+", "-", "~", "$"]

def tokenize(exp:str) -> list():
    exp = exp.replace(' ', '')
    reg_str = r"\d+\.?\d*|//|\*\*|[()\*\+-/%]"
    output = re.findall(reg_str, exp)
    return replace_un(output)

def replace_un(tokens: list()) -> list():
    if isOperator(tokens[0]):
        if tokens[0] == "-":
            tokens[0] = "~"
        elif tokens[0] == "+":
            tokens[0] = "$"
    for k in range(1, len(tokens) - 1):
        if isOperator(tokens[k]) and not(isNum(tokens[k - 1])):
            if tokens[k] == "-":
                tokens[k] = "~"
            elif tokens[k] == "+":
                tokens[k] = "$"
    return tokens

def to_rpn(expression: list()) -> list():
    output = []
    stack = []
    prev_priority = 0
    for tk in expression:
        print(output, stack)
        if isNum(tk):
            if '.' in tk:
                output.append(float(tk))
            else:
                output.append(int(tk))
        elif isOperator(tk):
            current_priority = op_priority(tk)
            if prev_priority != 0:
                if prev_priority <= current_priority and current_priority != 1:
                    output.append(stack.pop())
            prev_priority = current_priority
            stack.append(tk)
        else:
            if tk == "(":
                stack.append(tk)
                prev_priority = 0
            elif tk == ")":
                prev_priority = 0
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                else:
                    if len(stack) == 0:
                        raise ValueError("Лишние скобки")
                    else:
                        stack.pop()
            else:
                raise ValueError("Неверный формат ввода")
            print(output, stack)
    while stack:
        operator = stack.pop()
        if operator == "(":
            raise ValueError("Лишние скобки")
        output.append(operator)
    print(output)
    return output



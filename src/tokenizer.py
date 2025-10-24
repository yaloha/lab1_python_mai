import re

from src.priority import op_priority


def is_num(t: str) -> bool:
    """проверка на то, является ли полученная строка числом"""
    nums = [str(i) for i in range(10)]
    t = t.replace('.', '', 1)
    t = t.replace('-', '', 1)
    for symb in t:
        if symb not in nums:
            return False
    if len(t) == 0:
        return False
    return True


def is_operator(t: str) -> bool:
    """проверка на то, является ли полученная строка оператором из заданного списка операторов"""
    return t in ["**", "*", "/", "//", "%", "+", "-", "~", "$"]


def tokenize(exp: str) -> list:
    """разбиение полученного выражения на токены с помощью regex"""
    exp = exp.replace(' ', '')
    reg_str = r"\d+\.?\d*|//|\*\*|[()\*\+-/%]"
    output = re.findall(reg_str, exp)
    return replace_un(output)


def replace_un(tokens: list) -> list:
    """выявление унарных + и - в токенизированном выражении и замена их на $ и ~ соответственно"""
    if is_operator(tokens[0]):
        if tokens[0] == "-":
            tokens[0] = "~"
        elif tokens[0] == "+":
            tokens[0] = "$"
    for k in range(1, len(tokens) - 1):
        if is_operator(tokens[k]) and not (is_num(tokens[k - 1])):
            if tokens[k] == "-":
                tokens[k] = "~"
            elif tokens[k] == "+":
                tokens[k] = "$"
    return tokens


def to_rpn(expression: list) -> list:
    "преобразование токенизированного выражения в обратную польскую нотацию"
    output = []
    stack = []
    prev_priority = 0
    for tk in expression:
        if is_num(tk):
            if '.' in tk:
                output.append(float(tk))
            else:
                output.append(int(tk))
        elif is_operator(tk):
            current_priority = op_priority(tk)
            if prev_priority != 0:
                if prev_priority <= current_priority and current_priority != 1:
                    if not(stack[-1] == tk == "**"):
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
    while stack:
        operator = stack.pop()
        if operator == "(":
            raise ValueError("Лишние скобки")
        output.append(operator)
    return output

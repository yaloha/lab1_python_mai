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
    valid_symbs = set('0123456789.()*+-/% ')
    for char in exp:
        if char not in valid_symbs:
            raise SyntaxError(f"Недопустимый символ")
    exp = exp.replace(' ', '')
    reg_str = r"\d+\.?\d*|//|\*\*|[()\*\+-/%]"
    output = re.findall(reg_str, exp)
    if len(output) == 0:
        raise SyntaxError("Ввод неверного формата")
    return replace_un(output)


def replace_un(tokens: list) -> list:
    """выявление унарных + и - в токенизированном выражении и замена их на $ и ~ соответственно"""
    result = []
    for i in range(len(tokens)):
        current = tokens[i]
        if current in ["+", "-"] and is_operator(current):
            if i == 0:
                if current == "+":
                    result.append("$")
                else:
                    result.append("~")
            else:
                prev_tk = tokens[i - 1]
                if is_operator(prev_tk) or prev_tk == "(":
                    if current == "+":
                        result.append("$")
                    else:
                        result.append("~")
                else:
                    result.append(current)
        else:
            result.append(current)
    return result


def to_rpn(expression: list) -> list:
    "преобразование токенизированного выражения в обратную польскую нотацию"
    output = []
    stack = []
    prev_tk = ""
    for tk in expression:
        if is_num(tk):
            if '.' in tk:
                output.append(float(tk))
            else:
                output.append(int(tk))
        elif is_operator(tk):
            current_priority = op_priority(tk)
            while (stack and stack[-1] != "("
                   and op_priority(stack[-1]) <= current_priority):
                if (tk == "**" and stack[-1] == "**") or (tk in ["~", "$"] and stack[-1] in ["~", "$"]):
                    break
                output.append(stack.pop())
            stack.append(tk)
        elif tk == "(":
            if is_num(prev_tk) or prev_tk == ")":
                stack.append("*")
            stack.append(tk)
        elif tk == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Лишние скобки")
            stack.pop()
        else:
            raise ValueError("Неверный формат ввода")
        prev_tk = tk
    while stack:
        operator = stack.pop()
        if operator == "(":
            raise ValueError("Лишние скобки")
        output.append(operator)
    return output

from src.priority import op_priority


def isNum(t: str) -> bool:
    nums = [str(i) for i in range(10)]
    t = t.replace('.', '', 1)
    t = t.replace('-', '', 1)
    for symb in t:
        if symb not in nums:
            return False
    return True

def isOperator(t: str) -> bool:
    return t in ["**", "*", "/", "//", "%", "+", "-"]

def tokenize(exp:str) -> list():
    output = []
    splitted_exp = exp.split()
    for tk in splitted_exp:
        if len(tk) == 1:
            output.append(tk)
        else:
            if tk[0] == "(":
                output.append(tk[0])
                tk = tk[1:]
            if tk[0] == "+":
                tk = tk[1:]
            if tk[-1] == ")":
                output.append(tk[:-1])
                tk = tk[-1]
            output.append(tk)
    return output

def to_rpn(expression: str) -> list():
    output = []
    stack = []
    prev_priority = 0
    tokenized_exp = tokenize(expression)
    print(tokenized_exp)
    for tk in tokenized_exp:
        print(output, stack)
        if isNum(tk):
            if '.' in tk:
                output.append(float(tk))
            else:
                output.append(int(tk))
        elif isOperator(tk):
            current_priority = op_priority(tk)
            if prev_priority != 0:
                if prev_priority <= current_priority:
                    output.append(stack.pop())
            prev_priority = current_priority
            stack.append(tk)
        else:
            if tk == "(":
                stack.append(tk)
                prev_priority = 0
            elif tk == ")":
                while stack[-1] != "(" and stack:
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



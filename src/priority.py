priority_table = {"~": 1, "$": 1, "**": 2, "*": 3, "/": 3, "//": 3, "%": 3, "+": 4, "-": 4}


def op_priority(t: str) -> int:
    """возвращает приоритет введенного оператора"""
    return priority_table[t]

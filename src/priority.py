priority_table = {"**": 1, "*": 2, "/": 2, "//": 2, "%": 2, "+": 3, "-": 3}

def op_priority(t: str) -> int:
    return priority_table[t]

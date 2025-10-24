from src.calculate_rpn import calculate_rpn
from src.tokenizer import tokenize, to_rpn

def final_calc(expresssion: str) -> int|float:
    """функция, объединяющая остальные фукции и выдающая результат вычислений"""
    tokens = tokenize(expresssion)
    rpn = to_rpn(tokens)
    result = calculate_rpn(rpn)
    return result

def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    print("Для выхода введите stop вместо выражения")
    while True:
        try:
            expression = input("Введите выражение: ").strip()
            if expression == "stop":
                break
            if not expression:
                continue
            result = final_calc(expression)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

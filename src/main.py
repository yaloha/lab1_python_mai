from src.calculate_rpn import calculate_rpn
from src.constants import SAMPLE_CONSTANT
from src.tokenizer import tokenize, to_rpn, replace_un


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """
    try:
        print(calculate_rpn(to_rpn(replace_un(tokenize("-4 * (5 / -2)")))))
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

import unittest

from src.main import final_calc
from src.tokenizer import is_num, is_operator, tokenize, to_rpn, replace_un
from src.calculate import calculate_rpn


class NumberValTest(unittest.TestCase):
    """тесты для функции is_num"""

    def test_numbers(self):
        """проверка чисел"""
        self.assertTrue(is_num("123"))
        self.assertTrue(is_num("0"))
        self.assertTrue(is_num("1.23"))
        self.assertTrue(is_num("-7"))
        self.assertTrue(is_num("-2.55"))
        self.assertTrue(is_num("0.01"))

    def test_invalid_numbers(self):
        """проверка невалидных чисел"""
        self.assertFalse(is_num("abc"))
        self.assertFalse(is_num("12.3.45"))
        self.assertFalse(is_num("--5"))
        self.assertFalse(is_num(""))
        self.assertFalse(is_num("1a2"))
        self.assertFalse(is_num("."))
        self.assertFalse(is_num("-"))


class OperatorValTest(unittest.TestCase):
    """тесты для фунции is_operator"""

    def test_operators(self):
        """проверка операторов"""
        operators = ["~", "$", "**", "*", "/", "//", "%", "+", "-"]
        for op in operators:
            with self.subTest(op):
                self.assertTrue(is_operator(op))

    def test_invalid_operators(self):
        """проверка неподходящих операторов"""
        invalid_ops = ["&", "|", "=", ">>", "<<"]
        for op in invalid_ops:
            with self.subTest(op):
                self.assertFalse(is_operator(op))


class TokenizerTest(unittest.TestCase):
    """тесты для функции tokenize"""

    def test_basic(self):
        """базовая токенизация с пробелами"""
        self.assertEqual(tokenize("3 + 4"), ["3", "+", "4"])
        self.assertEqual(tokenize("8 / 2"), ["8", "/", "2"])
        self.assertEqual(tokenize("1 + 2 * 3 - 4 / 2"), ["1", "+", "2", "*", "3", "-", "4", "/", "2"])

    def test_basic_wo_spaces(self):
        """без пробелов"""
        self.assertEqual(tokenize("(1+2)*3"), ["(", "1", "+", "2", ")", "*", "3"])
        self.assertEqual(tokenize("(-1-2)*3"), ["(", "~", "1", "-", "2", ")", "*", "3"])
        self.assertEqual(tokenize("(1+2)*(3-4)"), ["(", "1", "+", "2", ")", "*", "(", "3", "-", "4", ")"])

    def test_floats(self):
        """токенизация float-ов"""
        self.assertEqual(tokenize("3.7 + 2.5"), ["3.7", "+", "2.5"])
        self.assertEqual(tokenize("0.9 * 0.4"), ["0.9", "*", "0.4"])


class UnaryRepTest(unittest.TestCase):
    """тесты для функции replace_un"""

    def test_unary_minus(self):
        self.assertEqual(replace_un(["-", "5"]), ["~", "5"]) #унарный минус в начале выражения
        self.assertEqual(replace_un(["3", "*", "-", "2"]), ["3", "*", "~", "2"]) #унарный минус после оператора
        self.assertEqual(replace_un(["3", "+", "(", "-", "2", ")"]), ["3", "+", "(", "~", "2", ")"]) #унарный минус после скобки

    def test_unary_plus(self):
        self.assertEqual(replace_un(["+", "5"]), ["$", "5"]) #унарный плюс в начале выражения
        self.assertEqual(replace_un(["3", "*", "+", "2"]), ["3", "*", "$", "2"]) #унарный плюс после оператора
        self.assertEqual(replace_un(["3", "+", "(", "+", "2", ")"]), ["3", "+", "(", "$", "2", ")"]) #унарный плюс после скобки


class ToRPNTest(unittest.TestCase):
    """тесты для функции to_rpn"""

    def test_operators_priority(self):
        """приоритет операторов"""
        self.assertEqual(to_rpn(["3", "+", "4", "*", "2"]), [3, 4, 2, "*", "+"])
        self.assertEqual(to_rpn(["3", "*", "4", "+", "2"]), [3, 4, "*", 2, "+"])

    def test_parentheses(self):
        """скобки"""
        self.assertEqual(to_rpn(["(", "3", "+", "4", ")", "*", "2"]), [3, 4, "+", 2, "*"])
        self.assertEqual(to_rpn(["3", "+", "(", "4", "*", "2", ")"]), [3, 4, 2, "*", "+"])

    def test_unary_operators(self):
        """унарные операторы"""
        self.assertEqual(to_rpn(["~", "5"]), [5, "~"])
        self.assertEqual(to_rpn(["3", "*", "~", "4"]), [3, 4, "~", "*"])

    def test_errors(self):
        """ошибки"""
        with self.assertRaises(ValueError): #незакрытая правая скобка
            to_rpn(["3", "+", ")"])

        with self.assertRaises(ValueError): #незакрытая левая скобка
            to_rpn(["(", "3", "+", "4"])

        with self.assertRaises(ValueError): #невалидный токен
            to_rpn(["3", "abc", "4"])


class RPNCalculationTest(unittest.TestCase):
    """тесты для функции calculate_rpn"""

    def test_basic_operations(self):
        """базовые операции"""
        self.assertEqual(calculate_rpn([3, 4, "+"]), 7)
        self.assertEqual(calculate_rpn([5, 2, "-"]), 3)
        self.assertEqual(calculate_rpn([6, 3, "*"]), 18)
        self.assertEqual(calculate_rpn([8, 2, "/"]), 4)
        self.assertEqual(calculate_rpn([10, 3, "//"]), 3)

    def test_unary_operations(self):
        """унарные операции"""
        self.assertEqual(calculate_rpn([5, "~"]), -5)
        self.assertEqual(calculate_rpn([-3, "~"]), 3)
        self.assertEqual(calculate_rpn([5, "$"]), 5)

    def test_longer_expressions(self):
        """выражения длиннее"""
        self.assertEqual(calculate_rpn([3, 4, 2, "*", "+"]), 11)
        self.assertEqual(calculate_rpn([3, 4, "*", 2, "+"]), 14)

    def test_decimal_numbers(self):
        """float-ы"""
        self.assertEqual(calculate_rpn([3.5, 2.5, "+"]), 6.0)
        self.assertEqual(calculate_rpn([5.0, 2.0, "/"]), 2.5)

    def test_error_cases(self):
        """ошибочные случаи"""
        with self.assertRaises(SyntaxError):
            calculate_rpn([3, "+"])  # не хватает чисел для унарной операции

        with self.assertRaises(SyntaxError):
            calculate_rpn(["+"])  # только оператор

        with self.assertRaises(SyntaxError):
            calculate_rpn([5, "~", "+"])  # не хватает чисел для бинарной операции

        with self.assertRaises(ZeroDivisionError):
            calculate_rpn([5, 0, "/"])  # деление на ноль


class FinalCalcTest(unittest.TestCase):
    """тест финальной функции"""

    def test_full_calculation_cycle(self):
        self.assertEqual(final_calc("-3 + 4"), 1)
        self.assertEqual(final_calc("3 + 4 * 2"), 11)
        self.assertEqual(final_calc("(3 + 4) * 2"), 14)

    def test_single_number(self):
        """одно число"""
        self.assertEqual(final_calc("42"), 42)

    def test_single_neg_number(self):
        """одно отрицательное число"""
        self.assertEqual(final_calc("-5"), -5)

    def test_pow_expressions(self):
        """приоритет степеней"""
        self.assertEqual(final_calc("2 ** 4 ** 2"), 65536)
        self.assertEqual(final_calc("(2 ** 4) ** 2"), 256)

    def test_decimal_numbers(self):
        """float-ы"""
        self.assertEqual(final_calc("2.5 + 3.5"), 6.0)
        self.assertEqual(final_calc("10.0 / 4"), 2.5)
        self.assertEqual(final_calc("5.34 * 2"), 10.68)

    def test_nested_parentheses(self):
        """вложенные скобки"""
        self.assertEqual(final_calc("-((2 + 3) * 4)"), -20)
        self.assertEqual(final_calc("5 - (2 * (3 + 4))"), -9)
        self.assertEqual(final_calc("((5 - 1) * (3 + 2))"), 20)

    def test_space_handling(self):
        "пробелы"
        self.assertEqual(final_calc("  3 + 4  "), 7)
        self.assertEqual(final_calc("3+4"), 7)
        self.assertEqual(final_calc("3 +    4"), 7)
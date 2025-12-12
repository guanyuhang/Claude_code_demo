"""
計算機單元測試
"""

import unittest
from calculator import Calculator, evaluate_expression


class TestCalculator(unittest.TestCase):
    """測試 Calculator 類別"""

    def setUp(self):
        """每個測試前建立新的計算機實例"""
        self.calc = Calculator()

    # 測試基本算術運算
    def test_add(self):
        """測試加法"""
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0.5, 0.5), 1.0)

    def test_subtract(self):
        """測試減法"""
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)
        self.assertEqual(self.calc.subtract(0, 0), 0)

    def test_multiply(self):
        """測試乘法"""
        self.assertEqual(self.calc.multiply(4, 5), 20)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)

    def test_divide(self):
        """測試除法"""
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertEqual(self.calc.divide(-6, 3), -2)

    def test_divide_by_zero(self):
        """測試除以零的錯誤處理"""
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)
        self.assertIn("除數不能為零", str(context.exception))

    # 測試進階運算
    def test_power(self):
        """測試乘方"""
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(2, -1), 0.5)

    def test_sqrt(self):
        """測試平方根"""
        self.assertEqual(self.calc.sqrt(16), 4)
        self.assertEqual(self.calc.sqrt(0), 0)
        self.assertAlmostEqual(self.calc.sqrt(2), 1.4142135623730951)

    def test_sqrt_negative(self):
        """測試負數平方根的錯誤處理"""
        with self.assertRaises(ValueError) as context:
            self.calc.sqrt(-1)
        self.assertIn("負數無法計算平方根", str(context.exception))

    def test_percentage(self):
        """測試百分比"""
        self.assertEqual(self.calc.percentage(50), 0.5)
        self.assertEqual(self.calc.percentage(100), 1)
        self.assertEqual(self.calc.percentage(0), 0)

    def test_modulo(self):
        """測試取餘數"""
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(15, 5), 0)
        self.assertEqual(self.calc.modulo(7, 2), 1)

    def test_modulo_by_zero(self):
        """測試取餘數除以零的錯誤處理"""
        with self.assertRaises(ValueError):
            self.calc.modulo(10, 0)

    def test_absolute(self):
        """測試絕對值"""
        self.assertEqual(self.calc.absolute(-5), 5)
        self.assertEqual(self.calc.absolute(5), 5)
        self.assertEqual(self.calc.absolute(0), 0)

    def test_negate(self):
        """測試取負數"""
        self.assertEqual(self.calc.negate(5), -5)
        self.assertEqual(self.calc.negate(-5), 5)
        self.assertEqual(self.calc.negate(0), 0)

    # 測試歷史記錄功能
    def test_history(self):
        """測試運算歷史記錄"""
        self.calc.add(1, 2)
        self.calc.multiply(3, 4)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertIn("1 + 2 = 3", history[0])
        self.assertIn("3 × 4 = 12", history[1])

    def test_clear_history(self):
        """測試清除歷史記錄"""
        self.calc.add(1, 2)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)
        self.assertEqual(self.calc.get_last_result(), 0)

    def test_last_result(self):
        """測試取得上次結果"""
        self.calc.add(5, 5)
        self.assertEqual(self.calc.get_last_result(), 10)
        self.calc.multiply(2, 3)
        self.assertEqual(self.calc.get_last_result(), 6)


class TestEvaluateExpression(unittest.TestCase):
    """測試 evaluate_expression 函數"""

    def test_simple_expression(self):
        """測試簡單表達式"""
        self.assertEqual(evaluate_expression("2 + 3"), 5)
        self.assertEqual(evaluate_expression("10 - 4"), 6)
        self.assertEqual(evaluate_expression("3 * 4"), 12)
        self.assertEqual(evaluate_expression("8 / 2"), 4)

    def test_complex_expression(self):
        """測試複雜表達式"""
        self.assertEqual(evaluate_expression("2 + 3 * 4"), 14)
        self.assertEqual(evaluate_expression("(2 + 3) * 4"), 20)
        self.assertEqual(evaluate_expression("10 / 2 + 3"), 8)

    def test_invalid_characters(self):
        """測試非法字元"""
        with self.assertRaises(ValueError):
            evaluate_expression("2 + a")

    def test_invalid_syntax(self):
        """測試無效語法"""
        with self.assertRaises(ValueError):
            evaluate_expression("2 + * 3")


if __name__ == "__main__":
    unittest.main()

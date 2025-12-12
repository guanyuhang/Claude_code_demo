"""
簡易計算機模組
支援基本算術運算和進階數學功能
"""

import math
from typing import Union

Number = Union[int, float]


class Calculator:
    """計算機類別，提供各種數學運算功能"""

    def __init__(self):
        self.history: list[str] = []
        self.last_result: Number = 0

    def _record(self, expression: str, result: Number) -> Number:
        """記錄運算歷史"""
        self.history.append(f"{expression} = {result}")
        self.last_result = result
        return result

    # 基本算術運算
    def add(self, a: Number, b: Number) -> Number:
        """加法"""
        result = a + b
        return self._record(f"{a} + {b}", result)

    def subtract(self, a: Number, b: Number) -> Number:
        """減法"""
        result = a - b
        return self._record(f"{a} - {b}", result)

    def multiply(self, a: Number, b: Number) -> Number:
        """乘法"""
        result = a * b
        return self._record(f"{a} × {b}", result)

    def divide(self, a: Number, b: Number) -> Number:
        """除法"""
        if b == 0:
            raise ValueError("除數不能為零")
        result = a / b
        return self._record(f"{a} ÷ {b}", result)

    # 進階運算
    def power(self, base: Number, exponent: Number) -> Number:
        """乘方"""
        result = base ** exponent
        return self._record(f"{base} ^ {exponent}", result)

    def sqrt(self, a: Number) -> Number:
        """平方根"""
        if a < 0:
            raise ValueError("負數無法計算平方根")
        result = math.sqrt(a)
        return self._record(f"√{a}", result)

    def percentage(self, a: Number) -> Number:
        """百分比（轉換為小數）"""
        result = a / 100
        return self._record(f"{a}%", result)

    def modulo(self, a: Number, b: Number) -> Number:
        """取餘數"""
        if b == 0:
            raise ValueError("除數不能為零")
        result = a % b
        return self._record(f"{a} mod {b}", result)

    def absolute(self, a: Number) -> Number:
        """絕對值"""
        result = abs(a)
        return self._record(f"|{a}|", result)

    def negate(self, a: Number) -> Number:
        """取負數"""
        result = -a
        return self._record(f"-({a})", result)

    # 歷史記錄功能
    def get_history(self) -> list[str]:
        """取得運算歷史"""
        return self.history.copy()

    def clear_history(self) -> None:
        """清除運算歷史"""
        self.history.clear()
        self.last_result = 0

    def get_last_result(self) -> Number:
        """取得上次運算結果"""
        return self.last_result


def evaluate_expression(expression: str) -> Number:
    """
    安全地計算數學表達式
    僅允許基本數學運算
    """
    # 只允許數字、運算符和空格
    allowed_chars = set('0123456789+-*/().% ')
    if not all(c in allowed_chars for c in expression):
        raise ValueError("表達式包含不允許的字元")

    try:
        # 使用 eval 但限制在安全的範圍內
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except (SyntaxError, NameError, TypeError) as e:
        raise ValueError(f"無效的表達式: {e}")


if __name__ == "__main__":
    # 簡單測試
    calc = Calculator()
    print("計算機測試:")
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"6 × 7 = {calc.multiply(6, 7)}")
    print(f"15 ÷ 3 = {calc.divide(15, 3)}")
    print(f"2 ^ 8 = {calc.power(2, 8)}")
    print(f"√16 = {calc.sqrt(16)}")
    print(f"\n運算歷史: {calc.get_history()}")

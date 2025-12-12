#!/usr/bin/env python3
"""
計算機命令行介面
提供互動式計算機功能
"""

from calculator import Calculator, evaluate_expression


def print_help():
    """顯示說明"""
    print("""
╔══════════════════════════════════════════════════╗
║              簡易計算機 - 使用說明               ║
╠══════════════════════════════════════════════════╣
║  基本運算:                                       ║
║    add <a> <b>      - 加法 (a + b)              ║
║    sub <a> <b>      - 減法 (a - b)              ║
║    mul <a> <b>      - 乘法 (a × b)              ║
║    div <a> <b>      - 除法 (a ÷ b)              ║
║                                                  ║
║  進階運算:                                       ║
║    pow <a> <b>      - 乘方 (a ^ b)              ║
║    sqrt <a>         - 平方根 (√a)               ║
║    mod <a> <b>      - 取餘數 (a mod b)          ║
║    abs <a>          - 絕對值 (|a|)              ║
║    pct <a>          - 百分比 (a%)               ║
║                                                  ║
║  直接輸入表達式:                                 ║
║    例: 2 + 3 * 4    - 直接計算數學表達式        ║
║                                                  ║
║  其他命令:                                       ║
║    history          - 顯示運算歷史              ║
║    clear            - 清除歷史記錄              ║
║    last             - 顯示上次結果              ║
║    help             - 顯示此說明                ║
║    quit / exit      - 離開程式                  ║
╚══════════════════════════════════════════════════╝
""")


def print_banner():
    """顯示程式標題"""
    print("""
    ╔═══════════════════════════════════╗
    ║       🧮 簡易計算機 v1.0 🧮       ║
    ║   輸入 'help' 查看使用說明        ║
    ╚═══════════════════════════════════╝
    """)


def parse_number(s: str) -> float:
    """解析數字字串"""
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except ValueError:
        raise ValueError(f"'{s}' 不是有效的數字")


def main():
    """主程式"""
    calc = Calculator()
    print_banner()

    while True:
        try:
            user_input = input("\n計算機 > ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0].lower()

            # 離開程式
            if command in ('quit', 'exit', 'q'):
                print("感謝使用，再見！👋")
                break

            # 顯示說明
            elif command == 'help':
                print_help()

            # 顯示歷史
            elif command == 'history':
                history = calc.get_history()
                if history:
                    print("\n📜 運算歷史:")
                    for i, record in enumerate(history, 1):
                        print(f"  {i}. {record}")
                else:
                    print("尚無運算記錄")

            # 清除歷史
            elif command == 'clear':
                calc.clear_history()
                print("✅ 歷史記錄已清除")

            # 顯示上次結果
            elif command == 'last':
                print(f"上次結果: {calc.get_last_result()}")

            # 加法
            elif command == 'add':
                if len(parts) != 3:
                    print("用法: add <數字1> <數字2>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.add(a, b)
                    print(f"結果: {result}")

            # 減法
            elif command == 'sub':
                if len(parts) != 3:
                    print("用法: sub <數字1> <數字2>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.subtract(a, b)
                    print(f"結果: {result}")

            # 乘法
            elif command == 'mul':
                if len(parts) != 3:
                    print("用法: mul <數字1> <數字2>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.multiply(a, b)
                    print(f"結果: {result}")

            # 除法
            elif command == 'div':
                if len(parts) != 3:
                    print("用法: div <數字1> <數字2>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.divide(a, b)
                    print(f"結果: {result}")

            # 乘方
            elif command == 'pow':
                if len(parts) != 3:
                    print("用法: pow <底數> <指數>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.power(a, b)
                    print(f"結果: {result}")

            # 平方根
            elif command == 'sqrt':
                if len(parts) != 2:
                    print("用法: sqrt <數字>")
                else:
                    a = parse_number(parts[1])
                    result = calc.sqrt(a)
                    print(f"結果: {result}")

            # 取餘數
            elif command == 'mod':
                if len(parts) != 3:
                    print("用法: mod <數字1> <數字2>")
                else:
                    a, b = parse_number(parts[1]), parse_number(parts[2])
                    result = calc.modulo(a, b)
                    print(f"結果: {result}")

            # 絕對值
            elif command == 'abs':
                if len(parts) != 2:
                    print("用法: abs <數字>")
                else:
                    a = parse_number(parts[1])
                    result = calc.absolute(a)
                    print(f"結果: {result}")

            # 百分比
            elif command == 'pct':
                if len(parts) != 2:
                    print("用法: pct <數字>")
                else:
                    a = parse_number(parts[1])
                    result = calc.percentage(a)
                    print(f"結果: {result}")

            # 嘗試直接計算表達式
            else:
                try:
                    result = evaluate_expression(user_input)
                    print(f"結果: {result}")
                except ValueError as e:
                    print(f"❌ 錯誤: {e}")
                    print("輸入 'help' 查看可用命令")

        except ValueError as e:
            print(f"❌ 錯誤: {e}")
        except KeyboardInterrupt:
            print("\n\n感謝使用，再見！👋")
            break
        except EOFError:
            print("\n感謝使用，再見！👋")
            break


if __name__ == "__main__":
    main()

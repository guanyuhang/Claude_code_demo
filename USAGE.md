# 簡易計算機 使用文件

## 目錄
- [簡介](#簡介)
- [系統需求](#系統需求)
- [安裝方式](#安裝方式)
- [使用方法](#使用方法)
  - [互動模式](#互動模式)
  - [模組匯入](#模組匯入)
- [功能說明](#功能說明)
  - [基本運算](#基本運算)
  - [進階運算](#進階運算)
  - [其他功能](#其他功能)
- [使用範例](#使用範例)
- [執行測試](#執行測試)

---

## 簡介

這是一個使用 Python 開發的簡易計算機程式，提供基本算術運算和進階數學功能。支援互動式命令行介面，也可以作為模組匯入到其他 Python 專案中使用。

---

## 系統需求

- Python 3.8 或以上版本
- 無需額外安裝第三方套件

---

## 安裝方式

1. 複製專案到本地端：
   ```bash
   git clone <repository-url>
   cd Claude_code_demo
   ```

2. 確認 Python 版本：
   ```bash
   python3 --version
   ```

---

## 使用方法

### 互動模式

啟動互動式計算機介面：

```bash
python3 main.py
```

啟動後會顯示歡迎畫面，輸入 `help` 可以查看完整的使用說明。

### 模組匯入

在 Python 程式中匯入計算機模組：

```python
from calculator import Calculator

calc = Calculator()

# 執行計算
result = calc.add(3, 5)
print(result)  # 輸出: 8
```

---

## 功能說明

### 基本運算

| 命令 | 說明 | 範例 |
|------|------|------|
| `add <a> <b>` | 加法 (a + b) | `add 3 5` → 8 |
| `sub <a> <b>` | 減法 (a - b) | `sub 10 4` → 6 |
| `mul <a> <b>` | 乘法 (a × b) | `mul 6 7` → 42 |
| `div <a> <b>` | 除法 (a ÷ b) | `div 15 3` → 5 |

### 進階運算

| 命令 | 說明 | 範例 |
|------|------|------|
| `pow <a> <b>` | 乘方 (a^b) | `pow 2 8` → 256 |
| `sqrt <a>` | 平方根 | `sqrt 16` → 4 |
| `mod <a> <b>` | 取餘數 | `mod 10 3` → 1 |
| `abs <a>` | 絕對值 | `abs -5` → 5 |
| `pct <a>` | 百分比轉小數 | `pct 50` → 0.5 |

### 其他功能

| 命令 | 說明 |
|------|------|
| `history` | 顯示運算歷史記錄 |
| `clear` | 清除歷史記錄 |
| `last` | 顯示上次運算結果 |
| `help` | 顯示使用說明 |
| `quit` / `exit` / `q` | 離開程式 |

### 直接輸入表達式

除了使用命令，您也可以直接輸入數學表達式：

```
計算機 > 2 + 3 * 4
結果: 14

計算機 > (2 + 3) * 4
結果: 20
```

---

## 使用範例

### 範例 1: 基本計算

```bash
$ python3 main.py

計算機 > add 3 5
結果: 8

計算機 > mul 6 7
結果: 42

計算機 > div 100 4
結果: 25.0
```

### 範例 2: 進階計算

```bash
計算機 > pow 2 10
結果: 1024

計算機 > sqrt 144
結果: 12.0

計算機 > mod 17 5
結果: 2
```

### 範例 3: 查看歷史記錄

```bash
計算機 > history

運算歷史:
  1. 3 + 5 = 8
  2. 6 × 7 = 42
  3. 100 ÷ 4 = 25.0
```

### 範例 4: 作為模組使用

```python
from calculator import Calculator, evaluate_expression

# 使用 Calculator 類別
calc = Calculator()

# 基本運算
print(calc.add(10, 5))       # 15
print(calc.subtract(10, 5))  # 5
print(calc.multiply(10, 5))  # 50
print(calc.divide(10, 5))    # 2.0

# 進階運算
print(calc.power(2, 8))      # 256
print(calc.sqrt(64))         # 8.0

# 查看歷史
print(calc.get_history())

# 直接計算表達式
result = evaluate_expression("(10 + 5) * 2")
print(result)  # 30
```

---

## 執行測試

執行單元測試以驗證程式功能：

```bash
python3 -m unittest test_calculator.py -v
```

預期輸出將顯示所有測試通過。

---

## 檔案結構

```
Claude_code_demo/
├── calculator.py       # 計算機核心模組
├── main.py            # 命令行介面程式
├── test_calculator.py # 單元測試
├── USAGE.md           # 本使用文件
└── .gitignore         # Git 忽略檔案設定
```

---

## 注意事項

1. **除法運算**：除數不能為零，否則會顯示錯誤訊息
2. **平方根運算**：不支援負數，否則會顯示錯誤訊息
3. **表達式計算**：僅支援基本數學符號 (`+`, `-`, `*`, `/`, `(`, `)`, `%`)

---

## 聯絡方式

如有任何問題或建議，歡迎提出 Issue 或 Pull Request。

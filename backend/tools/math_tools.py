def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Modulo by zero")
    return a % b

def power(base: float, exp: float) -> float:
    return base ** exp

def clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, value))

def calculate_percentage_of_value(percent: float, total: float) -> float:
    return total * (percent / 100.0)

def subtract_percentage(value: float, percent: float) -> float:
    return value * (1 - (percent / 100.0))

def percent_to_decimal(percent: float) -> float:
    return percent / 100.0

def decimal_to_percent(decimal: float) -> float:
    return decimal * 100.0

def usd_to_brl(value_usd: float, rate: float) -> float:
    return value_usd * rate

def calculate_volatility(returns_list: list) -> float:
    if len(returns_list) < 2:
        return 0.0
    n = len(returns_list)
    mean = sum(returns_list) / n
    variance = sum((x - mean) ** 2 for x in returns_list) / (n - 1)
    return variance ** 0.5

def calculate_sharpe_ratio(return_pct: float, risk_free_rate: float, std_dev: float) -> float:
    if std_dev == 0:
        return 0.0
    return (return_pct - risk_free_rate) / std_dev

def calculate_ir_on_rf(gain: float, months: int) -> float:
    if months <= 6:
        rate = 0.225
    elif months <= 12:
        rate = 0.20
    elif months <= 24:
        rate = 0.175
    else:
        rate = 0.15
    return gain * rate

def calculate_ir_on_equity(gain: float) -> float:
    return gain * 0.15

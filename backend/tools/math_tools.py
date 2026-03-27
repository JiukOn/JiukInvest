import datetime
import math
from typing import List, Dict, Optional

# Constants for Brazil (Reference 2024-2025)
CDI_ANNUAL = 10.75
SELIC_ANNUAL = 10.75
IPCA_ANNUAL = 4.50
POUPANCA_MONTHLY_RATE = 0.005
IBOV_MONTHLY_RATE = 0.01

def _monthly_rate_from_annual(annual_rate_pct: float) -> float:
    if annual_rate_pct <= 0:
        return 0.0
    return (1 + annual_rate_pct / 100.0) ** (1 / 12.0) - 1

# --- Basic Math Tools ---

def math_add(a: float, b: float) -> float:
    """Retorna a soma de a e b."""
    return a + b

def math_subtract(a: float, b: float) -> float:
    """Retorna a subtração de b de a."""
    return a - b

def math_multiply(a: float, b: float) -> float:
    """Retorna o produto de a e b."""
    return a * b

def math_divide(a: float, b: float) -> float:
    """Retorna a divisão de a por b. Levanta erro se b for zero."""
    if b == 0: raise ValueError("Divisão por zero.")
    return a / b

def math_remainder(a: float, b: float) -> float:
    """Retorna o resto da divisão de a por b."""
    return a % b

def math_percentage(part: float, total: float) -> float:
    """Calcula qual a porcentagem de 'part' em relação ao 'total'."""
    if total == 0: return 0.0
    return (part / total) * 100.0

def math_factorial(n: int) -> int:
    """Calcula o fatorial de n."""
    return math.factorial(n)

# --- Sequences and Series ---

def math_arithmetic_progression(a1: float, n: int, d: float) -> Dict[str, float]:
    """Calcula o n-ésimo termo (an) e a soma (Sn) de uma Progressão Aritmética."""
    an = a1 + (n - 1) * d
    sn = (n * (a1 + an)) / 2
    return {"n_term": an, "sum": sn}

def math_geometric_progression(a1: float, n: int, r: float) -> Dict[str, float]:
    """Calcula o n-ésimo termo (an) e a soma (Sn) de uma Progressão Geométrica."""
    an = a1 * (r ** (n - 1))
    if r == 1:
        sn = n * a1
    else:
        sn = (a1 * (r**n - 1)) / (r - 1)
    return {"n_term": an, "sum": sn}

def math_summation(values: List[float]) -> float:
    """Retorna a somatória de uma lista de valores."""
    return sum(values)

# --- Financial Tools ---

def calculate_compound_interest(principal: float, monthly_contribution: float, annual_rate_pct: float, months: int) -> float:
    """Calcula o montante final de um investimento com juros compostos e aportes mensais."""
    current_amount = float(principal)
    monthly_rate = _monthly_rate_from_annual(annual_rate_pct)
    
    for _ in range(months):
        current_amount += monthly_contribution
        current_amount *= (1 + monthly_rate)
        
    return round(current_amount, 2)

def math_roi(initial_value: float, final_value: float) -> float:
    """Calcula o Retorno sobre Investimento (ROI) em porcentagem."""
    if initial_value == 0: return 0.0
    return ((final_value - initial_value) / initial_value) * 100.0

def math_pmt(rate_annual_pct: float, nper_months: int, pv: float) -> float:
    """Calcula o valor da prestação mensal (PMT) pelo Sistema Price (Francês)."""
    r = _monthly_rate_from_annual(rate_annual_pct)
    if r == 0: return pv / nper_months
    pmt = (pv * r * (1 + r)**nper_months) / ((1 + r)**nper_months - 1)
    return round(pmt, 2)

def get_market_benchmarks() -> Dict[str, float]:
    """Retorna as taxas de mercado atuais (SELIC, CDI, IPCA) para uso em cálculos."""
    return {
        "SELIC_ANNUAL": SELIC_ANNUAL,
        "CDI_ANNUAL": CDI_ANNUAL,
        "IPCA_ANNUAL": IPCA_ANNUAL,
        "POUPANCA_MONTHLY": POUPANCA_MONTHLY_RATE * 100,
        "IBOVESPA_MONTHLY": IBOV_MONTHLY_RATE * 100
    }

def calculate_tax_impact(profit: float, asset_type: str, period_months: int) -> float:
    """Estima o Imposto de Renda (IR) para ativos brasileiros baseado no tempo e tipo."""
    if profit <= 0: return 0.0
    a_type = asset_type.upper()
    if a_type == "FII": return 0.0
    if a_type in ["ACOES", "AÇÕES"]: return profit * 0.15
    if period_months <= 6: rate = 0.225
    elif period_months <= 12: rate = 0.20
    elif period_months <= 24: rate = 0.175
    else: rate = 0.15
    return round(profit * rate, 2)

def calculate_inflation_adjustment(value: float, annual_inflation_pct: float, months: int) -> float:
    """Ajusta um valor futuro pela inflação (IPCA) para encontrar o poder de compra real."""
    monthly_inflation = (1 + annual_inflation_pct / 100.0) ** (1/12.0) - 1
    real_value = value / ((1 + monthly_inflation) ** months)
    return round(real_value, 2)

def get_compound_interest_projection(principal: float, monthly_contribution: float, annual_rate_pct: float, months: int) -> List[Dict]:
    """Calcula a evolução do investimento comparando com Poupança e Benchmark."""
    start_year = datetime.datetime.now().year
    start_month = datetime.datetime.now().month
    month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    evolution_data = []
    current_value = float(principal)
    current_poupanca = float(principal)
    current_ibov = float(principal)

    if months <= 36:
        for i in range(months + 1):
            month_offset = (start_month - 1 + i) % 12
            year_offset = start_year + (start_month - 1 + i) // 12
            curr_str = f"{month_names[month_offset]}/{year_offset}"
            if i > 0:
                current_value = calculate_compound_interest(current_value, monthly_contribution, annual_rate_pct, 1)
                current_poupanca = calculate_compound_interest(current_poupanca, monthly_contribution, POUPANCA_MONTHLY_RATE * 12 * 100, 1)
                current_ibov = calculate_compound_interest(current_ibov, monthly_contribution, IBOV_MONTHLY_RATE * 12 * 100, 1)
            evolution_data.append({
                "year": curr_str, "value": round(current_value, 2),
                "value_poupanca": round(current_poupanca, 2), "value_ibov": round(current_ibov, 2)
            })
    else:
        years_horizon = max(1, months // 12)
        target_dates = [0] + [i * 12 for i in range(1, years_horizon + 1)]
        if target_dates[-1] != months: target_dates.append(months)
        current_time = 0
        for m_tick in target_dates:
            diff = m_tick - current_time
            if diff > 0:
                current_value = calculate_compound_interest(current_value, monthly_contribution, annual_rate_pct, diff)
                current_poupanca = calculate_compound_interest(current_poupanca, monthly_contribution, POUPANCA_MONTHLY_RATE * 12 * 100, diff)
                current_ibov = calculate_compound_interest(current_ibov, monthly_contribution, IBOV_MONTHLY_RATE * 12 * 100, diff)
            curr_y = start_year + (m_tick // 12)
            evolution_data.append({
                "year": str(curr_y), "value": round(current_value, 2),
                "value_poupanca": round(current_poupanca, 2), "value_ibov": round(current_ibov, 2)
            })
            current_time = m_tick
    return evolution_data

def get_portfolio_allocation(principal: float, client_risk_score: float, matched_products: List[Dict]) -> List[Dict]:
    """Calcula a alocação de ativos baseada no risco e limites de concentração."""
    MAX_SINGLE_ASSET_PCT = 31.0
    raw_weights = []
    for p in matched_products:
        p_risk = p.get("risk_score", 0.5)
        w = pow(max(1.0 - abs(p_risk - client_risk_score), 0.01), 4.0)
        raw_weights.append(w)
    total_w = sum(raw_weights) if raw_weights else 1.0
    allocation_data = []
    accum_pct = 0.0
    for i, p in enumerate(matched_products):
        pct = round(100.0 - accum_pct, 2) if i == len(matched_products) - 1 else round((raw_weights[i] / total_w) * 100.0, 2)
        accum_pct += pct
        allocation_data.append({"name": p.get("name", "Ativo"), "value": pct, "value_brl": round((pct / 100.0) * principal, 2)})
    for item in allocation_data:
        if item["value"] > MAX_SINGLE_ASSET_PCT:
            excess = item["value"] - MAX_SINGLE_ASSET_PCT
            item["value"] = MAX_SINGLE_ASSET_PCT
            item["value_brl"] = round((MAX_SINGLE_ASSET_PCT / 100.0) * principal, 2)
            others = [x for x in allocation_data if x["name"] != item["name"]]
            if others:
                r_per = round(excess / len(others), 4)
                for o in others:
                    o["value"] = round(o["value"] + r_per, 2)
                    o["value_brl"] = round((o["value"] / 100.0) * principal, 2)
    return allocation_data

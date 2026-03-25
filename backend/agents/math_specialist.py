from data.schemas.state_models import AgentState
from backend.tools.financial_calculator import calculate_compound_interest

MAX_SINGLE_ASSET_PCT = 31.0
POUPANCA_MONTHLY_RATE = 0.005
IBOV_MONTHLY_RATE = 0.01

def _monthly_rate_from_annual(annual_rate_pct: float) -> float:
    if annual_rate_pct <= 0:
        return 0.0
    return (1 + annual_rate_pct / 100.0) ** (1 / 12.0) - 1

def run_math_specialist(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["MathSpecialist: Skipped. Missing ClientData."]}

    principal = float(client_data.initial_investment)
    contribution = float(client_data.monthly_contribution)
    months = int(client_data.investment_horizon_months)
    client_score = state.get("risk_score", 0.5)
    matched_products = state.get("matched_products", [])

    if not matched_products:
        return {"audit_logs": ["MathSpecialist: Aborted. No matched_products from ProfileAnalyzer."]}

    math_logs = []
    math_logs.append(f"calculate_initial_capital(value={principal})")

    total_ret = sum(p.get("expected_annual_return", 0.0) for p in matched_products)
    avg_ret = total_ret / len(matched_products) if matched_products else 0.0
    monthly_rate = _monthly_rate_from_annual(avg_ret)
    math_logs.append(f"calculate_weighted_avg_return(products={len(matched_products)}) -> annual={round(avg_ret,2)}% -> monthly_rate={round(monthly_rate*100,4)}%")

    import datetime
    start_year = datetime.datetime.now().year
    start_month = datetime.datetime.now().month
    month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

    evolution_data = []
    current_value = principal
    current_poupanca = principal
    current_ibov = principal

    if months <= 36:
        for i in range(months + 1):
            month_offset = (start_month - 1 + i) % 12
            year_offset = start_year + (start_month - 1 + i) // 12
            curr_str = f"{month_names[month_offset]}/{year_offset}"
            if i > 0:
                current_value = calculate_compound_interest(current_value, contribution, monthly_rate, 1)
                current_poupanca = calculate_compound_interest(current_poupanca, contribution, POUPANCA_MONTHLY_RATE, 1)
                current_ibov = calculate_compound_interest(current_ibov, contribution, IBOV_MONTHLY_RATE, 1)
            evolution_data.append({
                "year": curr_str,
                "value": round(current_value, 2),
                "value_poupanca": round(current_poupanca, 2),
                "value_ibov": round(current_ibov, 2)
            })
    else:
        years_horizon = max(1, months // 12)
        target_dates = [0] + [i * 12 for i in range(1, years_horizon + 1)]
        if target_dates[-1] != months:
            target_dates.append(months)

        current_time = 0
        for m_tick in target_dates:
            diff = m_tick - current_time
            if diff > 0:
                current_value = calculate_compound_interest(current_value, contribution, monthly_rate, diff)
                current_poupanca = calculate_compound_interest(current_poupanca, contribution, POUPANCA_MONTHLY_RATE, diff)
                current_ibov = calculate_compound_interest(current_ibov, contribution, IBOV_MONTHLY_RATE, diff)
            curr_y = start_year + (m_tick // 12)
            evolution_data.append({
                "year": str(curr_y),
                "value": round(current_value, 2),
                "value_poupanca": round(current_poupanca, 2),
                "value_ibov": round(current_ibov, 2)
            })
            current_time = m_tick

    final_amount = calculate_compound_interest(principal, contribution, monthly_rate, months)
    math_logs.append(f"calculate_compound_interest(principal={principal}, contribution={contribution}, rate={round(monthly_rate*100,4)}%/mo, months={months}) -> {round(final_amount, 2)}")

    raw_weights = []
    for p in matched_products:
        p_risk = p.get("risk_score", 0.5)
        affinity = 1.0 - abs(p_risk - client_score)
        w = pow(max(affinity, 0.01), 4.0)
        raw_weights.append(w)

    total_w = sum(raw_weights) if raw_weights else 1.0
    allocation_data = []
    accum_pct = 0.0

    for i, p in enumerate(matched_products):
        if i == len(matched_products) - 1:
            pct = round(100.0 - accum_pct, 2)
        else:
            pct = round((raw_weights[i] / total_w) * 100.0, 2)
        accum_pct += pct
        allocation_data.append({
            "name": p.get("name", "Ativo"),
            "value": pct,
            "value_brl": round((pct / 100.0) * principal, 2)
        })
        math_logs.append(f"calculate_weighted_allocation({p.get('name','?')}) -> affinity={round(1-abs(p.get('risk_score',0.5)-client_score),3)}, weight={round(raw_weights[i],4)} -> {pct}% = R$ {round((pct/100.0)*principal,2)}")

    capped_items = []
    for item in allocation_data:
        if item["value"] > MAX_SINGLE_ASSET_PCT:
            excess = item["value"] - MAX_SINGLE_ASSET_PCT
            item["value"] = MAX_SINGLE_ASSET_PCT
            item["value_brl"] = round((MAX_SINGLE_ASSET_PCT / 100.0) * principal, 2)
            others = [x for x in allocation_data if x["name"] != item["name"]]
            if others:
                redistrib_per = round(excess / len(others), 4)
                for o in others:
                    o["value"] = round(o["value"] + redistrib_per, 2)
                    o["value_brl"] = round((o["value"] / 100.0) * principal, 2)
            capped_items.append(item["name"])
            math_logs.append(f"apply_anti_concentration_cap(asset='{item['name']}', cap={MAX_SINGLE_ASSET_PCT}%, excess={round(excess,2)}% redistributed among {len(others)} assets)")

    cap_log = f"Anti-concentration cap applied to: {capped_items}. " if capped_items else "No concentration cap triggered. "

    return {
        "math_operations_log": math_logs,
        "audit_logs": [
            f"MathSpecialist: Portfolio calculated. {cap_log}Final projected value: R$ {round(final_amount, 2)} over {months} months at {round(avg_ret, 2)}% p.a."
        ],
        "calculated_charts": {
            "evolution_bar": evolution_data,
            "allocation_pie": allocation_data
        }
    }

def calculate_risk_bounds(age: int, knowledge: str, horizon_months: int, income: float, contribution: float,
                          accepted_assets: list, past_investments: str, personal_stability: str) -> tuple[float, float]:
    
    high_risk_keys = ["acao", "ações", "acoes", "internaciona", "cripto", "bdr", "derivativo"]
    med_risk_keys = ["fii", "debenture", "debênture", "fundo multimercado", "fundo de investimento"]
    low_risk_keys = ["tesouro", "cdb", "lci", "lca", "poupanca", "poupança", "renda fixa"]
    
    def evaluate_text_risk(text: str, default_val: float) -> float:
        if not text:
            return default_val
        t = text.lower()
        if any(k in t for k in high_risk_keys):
            return 0.90
        if any(k in t for k in med_risk_keys):
            return 0.50
        if any(k in t for k in low_risk_keys):
            return 0.15
        return default_val

    asset_str = " ".join(accepted_assets).lower() if accepted_assets else ""
    w1_val = evaluate_text_risk(asset_str, 0.40)
    
    k_map = {"Iniciante": 0.10, "Intermediário": 0.50, "Avançado": 0.90}
    w2_val = k_map.get(knowledge, 0.10)
    
    w3_val = evaluate_text_risk(past_investments, 0.10)
    
    if horizon_months < 12: w4_val = 0.10
    elif horizon_months < 60: w4_val = 0.30
    elif horizon_months < 120: w4_val = 0.60
    else: w4_val = 0.90
    
    ratio = contribution / income if income > 0 else 1.0
    w5_val = ratio * 0.70  
    
    if age < 20: w6_val = 0.05
    elif age < 40: w6_val = 0.85
    elif age < 50: w6_val = 0.50
    else: w6_val = 0.30
    
    stab = personal_stability.lower()
    w7_weight = 1
    if "estavel" in stab or "estável" in stab:
        w7_val = 0.03
    elif "instavel" in stab or "instável" in stab:
        w7_val = 0.30
    elif "medio" in stab or "médio" in stab:
        w7_val = 0.13
    else:
        w7_val = 0.00
        w7_weight = 0
        
    total_weight = 6 + 5 + 4 + 3 + 2 + 1 + w7_weight
    weighted_sum = (w1_val*6) + (w2_val*5) + (w3_val*4) + (w4_val*3) + (w5_val*2) + (w6_val*1) + (w7_val*w7_weight)
    
    base_score = weighted_sum / total_weight
    
    high_score = base_score
    low_score = base_score * 0.85 
    
    high_score = max(0.0, min(1.0, high_score))
    low_score = max(0.0, min(1.0, low_score))
    
    return float(f"{low_score:.3f}"), float(f"{high_score:.3f}")

from data.schemas.state_models import AgentState

def run_financial_health_agent(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})
    income = float(raw_input.get("monthly_income", 0.0))
    contribution = float(raw_input.get("monthly_contribution", 0.0))
    
    warning = False
    logs = []
    
    if income == 0 and contribution > 0:
        warning = True
        logs.append("FinancialHealthAgent: WARNING - No income reported but contribution planned.")
    elif contribution > income:
        warning = True
        logs.append("FinancialHealthAgent: CRITICAL - Monthly contribution exceeds monthly income.")
    elif contribution > (0.7 * income):
        warning = True
        logs.append("FinancialHealthAgent: WARNING - Monthly contribution > 70% of income. Recommend emergency fund.")
    else:
        logs.append("FinancialHealthAgent: Health check passed.")
        
    return {
        "financial_health_warning": warning,
        "audit_logs": logs
    }

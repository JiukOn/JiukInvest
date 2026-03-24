from data.schemas.state_models import AgentState
from backend.tools.financial_calculator import calculate_compound_interest

def run_math_specialist(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["MathSpecialist: Skipped due to missing ClientData."]}
        
    principal = float(client_data.initial_investment)
    contribution = float(client_data.monthly_contribution)
    months = int(client_data.investment_horizon_months)
    
    rate = 0.10
    final_amount = calculate_compound_interest(principal, contribution, rate, months)
    
    log = f"MathSpecialist: calculate_compound_interest({principal}, {contribution}, {rate}, {months}) = {final_amount}"
    
    return {
        "math_operations_log": [log],
        "audit_logs": [log]
    }

def calculate_compound_interest(principal: float, monthly_contribution: float, annual_rate: float, months: int) -> float:
    current_amount = float(principal)
    monthly_rate = annual_rate / 12.0
    
    for _ in range(months):
        current_amount += monthly_contribution
        current_amount *= (1 + monthly_rate)
        
    return round(current_amount, 2)

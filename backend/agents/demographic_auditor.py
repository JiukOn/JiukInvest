from data.schemas.state_models import AgentState

def run_demographic_auditor(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})
    age = raw_input.get("age", 18)
    
    if age < 13:
        category = "CHILD"
        log = "DemographicAuditor: User is < 13. Restricted to family/school focus."
    elif age < 16:
        category = "TEEN"
        log = "DemographicAuditor: User is 13-15. Restricted to financial education focus."
    else:
        category = "ADULT"
        log = "DemographicAuditor: User is >= 16. Standard investment track."
        
    return {
        "demographic_category": category,
        "audit_logs": [log]
    }

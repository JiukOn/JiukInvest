from data.schemas.state_models import AgentState

def run_compliance_checker(state: AgentState) -> dict:
    draft = state.get("draft_report")
    if not draft:
        return {"status_code": 400, "audit_logs": ["ComplianceChecker: No draft to check."]}
        
    text = draft.markdown_text.lower()
    forbidden_terms = ["lucro garantido", "risco zero", "absoluta certeza"]
    
    for term in forbidden_terms:
        if term in text:
            return {
                "status_code": 406,
                "audit_logs": [f"ComplianceChecker: REJECTED. Hallucination identified: '{term}'."]
            }
            
    return {
        "final_report": draft,
        "status_code": 200,
        "audit_logs": ["ComplianceChecker: APPROVED. Safe generation verified."]
    }

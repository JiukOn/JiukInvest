from data.schemas.state_models import AgentState
from backend.tools.blacklist_manager import add_to_blacklist, is_blacklisted

def run_context_analyzer(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})
    name = raw_input.get("name", "Unknown")
    
    if is_blacklisted(name):
        return {
            "is_blacklisted": True,
            "blacklist_reason": "Pre-existing blacklist entry",
            "audit_logs": ["ContextAnalyzer: User blocked due to existing blacklist entry."]
        }
        
    comments = str(raw_input.get("additional_comments", "")).lower()
    suspicious_keywords = ["roubei", "roubo", "lavagem", "ilegal", "crime", "fraude", "golpe", "ilícito", "tráfico"]
    
    for kw in suspicious_keywords:
        if kw in comments:
            age = raw_input.get("age", 0)
            reason = f"Suspicious keyword detected: {kw}"
            add_to_blacklist(name, age, comments, reason)
            return {
                "is_blacklisted": True,
                "blacklist_reason": reason,
                "audit_logs": [f"ContextAnalyzer: User blacklisted. {reason}"]
            }
            
    return {
        "is_blacklisted": False, 
        "blacklist_reason": None, 
        "audit_logs": ["ContextAnalyzer: AML check passed."]
    }

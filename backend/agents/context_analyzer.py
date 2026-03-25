from data.schemas.state_models import AgentState
from backend.tools.blacklist_manager import add_to_blacklist, is_blacklisted
import re

INJECTION_PATTERNS = [
    r"ignore\s+(previous|prior|all)\s+instructions?",
    r"jailbreak",
    r"act\s+as\s+(if\s+you\s+are|an?\s+)",
    r"forget\s+(your|all)\s+(rules?|instructions?)",
    r"you\s+are\s+now\s+in\s+",
    r"roleplay\s+as",
    r"pretend\s+you\s+(are|have\s+no)",
    r"bypass\s+(the\s+)?(filter|guardrail|rules?)",
    r"do\s+anything\s+now",
    r"developer\s+mode",
    r"override\s+(all\s+)?(rules?|safety)",
    r"disregard\s+(all\s+)?(previous|prior|your)",
]

AML_KEYWORDS = [
    "roubei", "roubo", "roubando", "rouba",
    "lavagem", "lavar dinheiro", "branquear", "limpar dinheiro",
    "ilegal", "crime", "criminoso", "atividade ilícita",
    "fraude", "fraudar", "golpe", "golpista",
    "ilícito", "ilícita",
    "tráfico", "trafico", "droga", "drogas", "cocaína", "cocaina",
    "maconha", "heroína", "heroina", "crack", "entorpecente",
    "vendo droga", "vendia droga", "venda de droga",
    "vendo substância", "traficante",
    "suborno", "propina", "corrupção", "desvio", "esquema",
    "caixa dois", "caixa 2", "esconder dinheiro",
    "evasão fiscal", "sonegação", "sonegar",
    "paraíso fiscal", "off-shore ilegal",
    "laundering", "bribery", "fake account", "money mule",
    "tax evasion", "shell company", "fictício", "laranja", "fantasma",
    "pistola", "arma ilegal", "contrabando", "sequestro", "extorsão",
    "pirâmide financeira", "pirâmide",
]

def run_context_analyzer(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})
    name = raw_input.get("name")
    
    if not name:
        return {
            "is_blacklisted": False,
            "blacklist_reason": None,
            "status_code": 400,
            "audit_logs": ["ContextAnalyzer: CRITICAL - Missing 'name' parameter. Halting."]
        }
    
    if is_blacklisted(name):
        return {
            "is_blacklisted": True,
            "blacklist_reason": "Pre-existing blacklist entry — this client is permanently banned.",
            "audit_logs": [f"ContextAnalyzer: BLOCKED. Client '{name}' is in the permanent blacklist. Access denied."]
        }

    all_text = " ".join([
        str(raw_input.get("additional_comments", "")),
        str(raw_input.get("past_investments", "")),
        str(raw_input.get("name", "")),
    ]).lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, all_text, re.IGNORECASE):
            return {
                "is_blacklisted": True,
                "blacklist_reason": "Prompt injection attempt detected.",
                "audit_logs": [f"ContextAnalyzer: BLOCKED. Prompt injection attempt detected."]
            }

    for kw in AML_KEYWORDS:
        if kw in all_text:
            age = raw_input.get("age", 0)
            reason = f"AML keyword detected in input: '{kw}'"
            add_to_blacklist(name, age, all_text[:300], reason)
            return {
                "is_blacklisted": True,
                "blacklist_reason": reason,
                "audit_logs": [f"ContextAnalyzer: BLOCKED & BLACKLISTED. {reason}. Client '{name}' permanently recorded."]
            }
            
    return {
        "is_blacklisted": False, 
        "blacklist_reason": None, 
        "audit_logs": ["ContextAnalyzer: AML check passed."]
    }

import sys
import os
import json
import logging
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.graph_orchestrator import build_graph

def run():
    print("Testing langgraph orchestration...")
    import backend.utils.env_loader  # forces override
    graph = build_graph()
    initial_state = {
        "raw_input": {
            "name": "Maria Silva Santos",
            "age": 34,
            "knowledge_level": "Intermediário",
            "has_invested_before": True,
            "past_investments": "CDB, Fundos DI, Previdência Privada",
            "investment_horizon_months": 24,
            "monthly_income": 5000,
            "monthly_contribution": 1000,
            "initial_investment": 10000,
            "accepts_public_titles": True,
            "accepts_private_titles": True,
            "accepts_national": True,
            "accepts_international": False,
            "accepted_asset_types": ["CDB", "LCI", "LCA", "Tesouro Direto", "Ações"]
        },
        "standardized_client_data": None,
        "matched_products": [],
        "draft_report": None,
        "final_report": None,
        "status_code": 0,
        "retry_count": 0,
        "is_blacklisted": False,
        "blacklist_reason": None,
        "demographic_category": "",
        "financial_health_warning": False,
        "math_operations_log": [],
        "audit_logs": ["System: Received payload via FastAPI."]
    }
    
    try:
        final_state = graph.invoke(initial_state)
        print("Success!")
        print(f"Final State dict keys: {list(final_state.keys()) if isinstance(final_state, dict) else type(final_state)}")
    except Exception as e:
        print(f"CRASH OCCURRED:\n{traceback.format_exc()}")

if __name__ == "__main__":
    run()

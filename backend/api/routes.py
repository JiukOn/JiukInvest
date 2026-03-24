from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from backend.graph_orchestrator import build_graph

router = APIRouter()
graph = build_graph()

class CopilotRequest(BaseModel):
    payload: Dict[str, Any]

@router.post("/copilot/generate")
async def generate_report(request: CopilotRequest):
    try:
        initial_state = {
            "raw_input": request.payload,
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
        
        final_state = graph.invoke(initial_state)
        
        if final_state.get("is_blacklisted"):
            return {
                "status": "error",
                "message": "Operação recusada por políticas de compliance (AML/Blacklist).",
                "reason": final_state.get("blacklist_reason"),
                "logs": final_state.get("audit_logs")
            }
            
        if final_state.get("demographic_category") in ["CHILD", "TEEN"]:
             return {
                "status": "restricted",
                "message": "Idade restrita. Foco redirecionado para família/educação.",
                "logs": final_state.get("audit_logs")
            }
            
        report = final_state.get("final_report")
        if not report:
            report = final_state.get("draft_report")
            
        if not report:
            raise HTTPException(status_code=500, detail="Failed to generate report.")
            
        return {
            "status": "success",
            "report": report.model_dump(),
            "logs": final_state.get("audit_logs")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from backend.graph_orchestrator import build_graph
from fastapi.responses import StreamingResponse
import json

router = APIRouter()
graph = build_graph()

class CopilotRequest(BaseModel):
    payload: Dict[str, Any]

@router.post("/copilot/generate")
async def generate_report(request: CopilotRequest):
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
        "demographic_lifecycle_note": None,
        "personal_stability": "",
        "financial_health_warning": False,
        "financial_health_score": None,
        "financial_health_summary": None,
        "financial_health_recommendation": None,
        "risk_score": 0.0,
        "math_operations_log": [],
        "calculated_charts": {},
        "audit_logs": ["System: Received payload via FastAPI."]
    }

    async def event_generator():
        yield f"data: {json.dumps({'type': 'log', 'agent': 'System', 'content': 'Received payload via FastAPI.'})}\n\n"

        final_state = {**initial_state}
        try:
            for step in graph.stream(initial_state):
                for node_name, node_state in step.items():
                    if node_state is None:
                        # Log para debug em caso de falha silenciosa
                        print(f"DEBUG: Node '{node_name}' returned None in parallel flow.")
                        continue
                    
                    if not isinstance(node_state, dict):
                        print(f"DEBUG: Node '{node_name}' returned non-mapping type: {type(node_state)}")
                        continue

                    final_state = {**final_state, **node_state}

                    if "audit_logs" in node_state and node_state["audit_logs"]:
                        for log_line in node_state["audit_logs"]:
                            yield f"data: {json.dumps({'type': 'log', 'agent': node_name, 'content': log_line})}\n\n"

                    if "math_operations_log" in node_state and node_state["math_operations_log"]:
                        for math_line in node_state["math_operations_log"]:
                            yield f"data: {json.dumps({'type': 'math_log', 'agent': node_name, 'content': math_line})}\n\n"

            if final_state.get("is_blacklisted"):
                yield f"data: {json.dumps({'type': 'result', 'status': 'blocked', 'message': 'Operação recusada por políticas de compliance (AML/Blacklist).', 'reason': final_state.get('blacklist_reason'), 'logs': final_state.get('audit_logs')})}\n\n"
                return

            if final_state.get("demographic_category") in ["CHILD", "TEEN"]:
                yield f"data: {json.dumps({'type': 'result', 'status': 'restricted', 'message': 'Acesso restrito. Cliente não elegível para a trilha de investimentos.', 'lifecycle_note': final_state.get('demographic_lifecycle_note', ''), 'logs': final_state.get('audit_logs')})}\n\n"
                return

            if final_state.get("status_code") == 400:
                yield f"data: {json.dumps({'type': 'result', 'status': 'validation_error', 'message': 'Dados inválidos. Verifique os campos do formulário.', 'logs': final_state.get('audit_logs')})}\n\n"
                return

            if final_state.get("financial_health_score") == "CRITICO":
                yield f"data: {json.dumps({'type': 'result', 'status': 'health_critical', 'message': 'Saúde financeira crítica. O aporte mensal não é compatível com a renda declarada.', 'recommendation': final_state.get('financial_health_recommendation', ''), 'logs': final_state.get('audit_logs')})}\n\n"
                return

            report = final_state.get("final_report") or final_state.get("draft_report")

            if not report:
                yield f"data: {json.dumps({'type': 'error', 'detail': 'Falha ao gerar o relatório. Nenhum conteúdo foi produzido pelo pipeline.'})}\n\n"
                return

            report_data = report.model_dump() if hasattr(report, "model_dump") else report

            result_payload = {
                "type": "result",
                "status": "success",
                "report": report_data,
                "charts": final_state.get("calculated_charts", {}),
                "health_score": final_state.get("financial_health_score"),
                "health_summary": final_state.get("financial_health_summary"),
                "health_recommendation": final_state.get("financial_health_recommendation"),
                "demographic_lifecycle_note": final_state.get("demographic_lifecycle_note"),
                "risk_score": final_state.get("risk_score", 0.0),
                "logs": final_state.get("audit_logs", []),
            }
            yield f"data: {json.dumps(result_payload)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'detail': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

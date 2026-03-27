import json
from langchain_core.prompts import ChatPromptTemplate
from data.schemas.state_models import AgentState
from backend.prompts.system_prompts import COMPLIANCE_PROMPT
from backend.utils.llm_factory import get_llm
from backend.utils.env_loader import AZURE_OPENAI_KEY
import re

FORBIDDEN_INTERNAL_LEAKS = [
    r"PROD\d{3}",
    r"calculate_",
    r"backend/",
    r"AgentState",
    r"math_specialist",
    r"report_writer",
    r"run_",
    r"\.py\b",
]

def run_compliance_checker(state: AgentState) -> dict:
    draft = state.get("draft_report")
    if not draft:
        return {"status_code": 400, "audit_logs": ["ComplianceChecker: No draft to check."]}

    text = draft.markdown_text

    for pattern in FORBIDDEN_INTERNAL_LEAKS:
        if re.search(pattern, text):
            return {
                "status_code": 406,
                "audit_logs": [f"ComplianceChecker (guard): REJECTED. Internal data leak detected: pattern '{pattern}'."]
            }

    if AZURE_OPENAI_KEY:
        try:
            llm = get_llm(temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", COMPLIANCE_PROMPT),
                ("user", "Revise o seguinte relatório:\n\n{report}")
            ])
            result = (prompt | llm).invoke({"report": text[:6000]})
            parsed = json.loads(result.content.strip())
            approved = parsed.get("approved", True)
            reason = parsed.get("reason", "")
            violations = parsed.get("violations", [])

            if not approved:
                return {
                    "status_code": 406,
                    "retry_count": state.get("retry_count", 0) + 1,
                    "audit_logs": [f"ComplianceChecker (LLM): REJECTED. {reason}. Violations: {violations}"]
                }

            return {
                "final_report": draft,
                "status_code": 200,
                "audit_logs": [f"ComplianceChecker (LLM): APPROVED. {reason}"]
            }
        except Exception as e:
            fallback_log = f"ComplianceChecker (fallback): APPROVED [⚠️ IA Error: {str(e)}]. Standard regex checks passed."

    return {
        "final_report": draft,
        "status_code": 200,
        "audit_logs": [fallback_log if 'fallback_log' in locals() else "ComplianceChecker (fallback): APPROVED. Standard regex checks passed."]
    }

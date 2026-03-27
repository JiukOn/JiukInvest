from langgraph.graph import StateGraph, END
from data.schemas.state_models import AgentState

from backend.agents.data_organizer import run_data_organizer
from backend.agents.context_analyzer import run_context_analyzer
from backend.agents.demographic_auditor import run_demographic_auditor
from backend.agents.financial_health_agent import run_financial_health_agent
from backend.agents.emotional_analyzer import run_emotional_analyzer
from backend.agents.profile_analyzer import run_profile_analyzer
from backend.agents.math_specialist import run_math_specialist
from backend.agents.report_writer import run_report_writer
from backend.agents.compliance_checker import run_compliance_checker


def should_continue_after_data(state: AgentState):
    if not state.get("standardized_client_data") or state.get("status_code") == 400:
        return END
    # Dispara os 4 agentes em paralelo
    return ["ContextAnalyzer", "Demographics", "HealthCheck", "EmotionalAnalyzer"]


def should_proceed_to_profile(state: AgentState):
    """Verifica se algum guardrail barrou a execução antes de prosseguir."""
    # AML Block
    if state.get("is_blacklisted"):
        return END
    # Demographics Block
    if state.get("demographic_category") in ["CHILD", "TEEN"]:
        return END
    # Health Block
    if state.get("financial_health_score") == "CRITICO":
        return END
    
    return "ProfileAnalyzer"


def should_retry_compliance(state: AgentState):
    """Decide se tenta corrigir o relatório ou encerra."""
    status = state.get("status_code")
    retries = state.get("retry_count", 0)
    
    if status == 406 and retries < 2:
        return "ReportWriter"
    return END


def should_emit_final(state: AgentState):
    return END


def run_guardrail_gate(state: AgentState) -> dict:
    """Nó de sincronização que verifica se podemos prosseguir após o paralelo."""
    return {}


def should_proceed_after_gate(state: AgentState):
    """Decisão final após o fan-in paralelo."""
    if state.get("is_blacklisted"):
        return END
    if state.get("demographic_category") in ["CHILD", "TEEN"]:
        return END
    if state.get("financial_health_score") == "CRITICO":
        return END
    return "ProfileAnalyzer"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("DataOrganizer", run_data_organizer)
    graph.add_node("ContextAnalyzer", run_context_analyzer)
    graph.add_node("Demographics", run_demographic_auditor)
    graph.add_node("HealthCheck", run_financial_health_agent)
    graph.add_node("EmotionalAnalyzer", run_emotional_analyzer)
    graph.add_node("GuardrailGate", run_guardrail_gate)
    graph.add_node("ProfileAnalyzer", run_profile_analyzer)
    graph.add_node("MathSpecialist", run_math_specialist)
    graph.add_node("ReportWriter", run_report_writer)
    graph.add_node("Compliance", run_compliance_checker)

    graph.set_entry_point("DataOrganizer")

    # Fan-out paralelo
    graph.add_conditional_edges("DataOrganizer", should_continue_after_data)

    # Fan-in para o GuardrailGate
    graph.add_edge("ContextAnalyzer", "GuardrailGate")
    graph.add_edge("Demographics", "GuardrailGate")
    graph.add_edge("HealthCheck", "GuardrailGate")
    graph.add_edge("EmotionalAnalyzer", "GuardrailGate")

    # Decisão de prosseguir ou barrar
    graph.add_conditional_edges("GuardrailGate", should_proceed_after_gate)
    
    graph.add_edge("ProfileAnalyzer", "MathSpecialist")
    graph.add_edge("MathSpecialist", "ReportWriter")
    graph.add_edge("ReportWriter", "Compliance")
    graph.add_conditional_edges("Compliance", should_retry_compliance)

    return graph.compile()

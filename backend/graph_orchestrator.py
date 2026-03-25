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
    return "ContextAnalyzer"


def should_block_aml(state: AgentState):
    if state.get("is_blacklisted"):
        return END
    return "Demographics"


def should_block_demographics(state: AgentState):
    if state.get("demographic_category") in ["CHILD", "TEEN"]:
        return END
    return "HealthCheck"


def should_block_health(state: AgentState):
    if state.get("financial_health_score") == "CRITICO":
        return END
    return "EmotionalAnalyzer"


def should_emit_final(state: AgentState):
    if state.get("status_code") == 406:
        return END
    if not state.get("final_report") and not state.get("draft_report"):
        return END
    return END


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("DataOrganizer", run_data_organizer)
    graph.add_node("ContextAnalyzer", run_context_analyzer)
    graph.add_node("Demographics", run_demographic_auditor)
    graph.add_node("HealthCheck", run_financial_health_agent)
    graph.add_node("EmotionalAnalyzer", run_emotional_analyzer)
    graph.add_node("ProfileAnalyzer", run_profile_analyzer)
    graph.add_node("MathSpecialist", run_math_specialist)
    graph.add_node("ReportWriter", run_report_writer)
    graph.add_node("Compliance", run_compliance_checker)

    graph.set_entry_point("DataOrganizer")

    graph.add_conditional_edges("DataOrganizer", should_continue_after_data)
    graph.add_conditional_edges("ContextAnalyzer", should_block_aml)
    graph.add_conditional_edges("Demographics", should_block_demographics)
    graph.add_conditional_edges("HealthCheck", should_block_health)

    graph.add_edge("EmotionalAnalyzer", "ProfileAnalyzer")
    graph.add_edge("ProfileAnalyzer", "MathSpecialist")
    graph.add_edge("MathSpecialist", "ReportWriter")
    graph.add_edge("ReportWriter", "Compliance")
    graph.add_edge("Compliance", END)

    return graph.compile()

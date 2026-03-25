import json
from langchain_core.prompts import ChatPromptTemplate
from data.schemas.state_models import AgentState
from backend.prompts.system_prompts import FINANCIAL_HEALTH_PROMPT
from backend.utils.llm_factory import get_llm
from backend.utils.env_loader import AZURE_OPENAI_KEY

def run_financial_health_agent(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["FinancialHealthAgent: Missing standardized_client_data. Halting."]}

    income = float(client_data.monthly_income)
    contribution = float(client_data.monthly_contribution)
    wealth = float(client_data.initial_investment)

    if income > 0 and contribution > income:
        return {
            "financial_health_warning": True,
            "financial_health_score": "CRITICO",
            "financial_health_summary": "Aporte mensal excede a renda mensal declarada. Situação financeira inviável para investimento.",
            "audit_logs": ["FinancialHealthAgent: CRITICAL BLOCK - Contribution exceeds income. Graph halted."]
        }

    if AZURE_OPENAI_KEY:
        try:
            llm = get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_messages([
                ("system", FINANCIAL_HEALTH_PROMPT),
                ("user", (
                    "Renda Mensal: R$ {income}\n"
                    "Aporte Mensal: R$ {contribution}\n"
                    "Patrimônio Inicial: R$ {wealth}\n"
                    "Horizonte de Investimento: {horizon} meses\n"
                    "Histórico de Investimentos: {history}\n"
                    "Comentários do Cliente: {comments}"
                ))
            ])
            result = (prompt | llm).invoke({
                "income": income,
                "contribution": contribution,
                "wealth": wealth,
                "horizon": client_data.investment_horizon_months,
                "history": client_data.past_investments or "Não informado",
                "comments": client_data.additional_comments or "Nenhum",
            })
            parsed = json.loads(result.content.strip())
            warning = parsed.get("warning", False)
            score = parsed.get("health_score", "SAUDAVEL")
            summary = parsed.get("summary", "Análise financeira concluída.")
            recommendation = parsed.get("recommendation", "")
            return {
                "financial_health_warning": warning,
                "financial_health_score": score,
                "financial_health_summary": summary,
                "financial_health_recommendation": recommendation,
                "audit_logs": [f"FinancialHealthAgent (LLM): Score={score}. Warning={warning}. {summary}"]
            }
        except Exception as e:
            pass

    warning = income == 0 and contribution > 0
    return {
        "financial_health_warning": warning,
        "financial_health_score": "ATENCAO" if warning else "SAUDAVEL",
        "financial_health_summary": "Análise de saúde financeira (modo fallback).",
        "audit_logs": [f"FinancialHealthAgent (fallback): Warning={warning}."]
    }

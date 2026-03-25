import json
from langchain_core.prompts import ChatPromptTemplate
from data.schemas.state_models import AgentState
from backend.prompts.system_prompts import DEMOGRAPHIC_AUDITOR_PROMPT
from backend.utils.llm_factory import get_llm
from backend.utils.env_loader import AZURE_OPENAI_KEY

def run_demographic_auditor(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["DemographicAuditor: Missing standardized_client_data. Halting."]}

    age = client_data.age

    if age < 13:
        fallback_category = "CHILD"
        fallback_note = "Menor de 13 anos. Elegibilidade de investimento restrita."
    elif age < 16:
        fallback_category = "TEEN"
        fallback_note = "Entre 13 e 15 anos. Elegibilidade de investimento restrita."
    elif age >= 65:
        fallback_category = "SENIOR"
        fallback_note = "Cliente sênior. Atenção especial à liquidez e preservação patrimonial."
    else:
        fallback_category = "ADULT"
        fallback_note = "Cliente adulto em trilha padrão de investimentos."

    if AZURE_OPENAI_KEY:
        try:
            llm = get_llm(temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", DEMOGRAPHIC_AUDITOR_PROMPT),
                ("user", "Nome: {name} | Idade: {age} | Renda Mensal: R$ {income} | Patrimônio Inicial: R$ {wealth}")
            ])
            result = (prompt | llm).invoke({
                "name": client_data.name,
                "age": age,
                "income": client_data.monthly_income,
                "wealth": client_data.initial_investment,
            })
            parsed = json.loads(result.content.strip())
            category = parsed.get("category", fallback_category)
            lifecycle_note = parsed.get("lifecycle_note", fallback_note)
            return {
                "demographic_category": category,
                "demographic_lifecycle_note": lifecycle_note,
                "audit_logs": [f"DemographicAuditor (LLM): Category={category}. {lifecycle_note}"]
            }
        except Exception as e:
            pass

    return {
        "demographic_category": fallback_category,
        "demographic_lifecycle_note": fallback_note,
        "audit_logs": [f"DemographicAuditor (fallback): Category={fallback_category}. {fallback_note}"]
    }

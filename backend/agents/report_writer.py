import os
import json
from data.schemas.state_models import AgentState, FinalReport, ReportCharts, AllocationData, EvolutionData
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.prompts.system_prompts import WRITER_SYSTEM_PROMPT
from backend.utils.env_loader import (
    AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_MODEL, 
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_VERSION
)

def run_report_writer(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    matched_products = state.get("matched_products", [])
    math_logs = state.get("math_operations_log", [])
    
    markdown_output = "## Erro Crítico do Sistema\n\nNão foi possível gerar a estratégia hiper-personalizada."
    charts = ReportCharts(allocation_pie=[], evolution_bar=[])
    
    if AZURE_OPENAI_KEY:
        try:
            llm = AzureChatOpenAI(
                azure_deployment=AZURE_OPENAI_DEPLOYMENT,
                model_name=AZURE_OPENAI_MODEL,
                api_key=AZURE_OPENAI_KEY,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_version=AZURE_OPENAI_VERSION
            )
            context = f"Cliente: {client_data.name}, {client_data.age} anos. Produtos: {json.dumps(matched_products)}. Calculos: {math_logs}. Distribuição Exigida (%): {json.dumps(state.get('calculated_charts', {}).get('allocation_pie', []))}."
            prompt = ChatPromptTemplate.from_messages([
                ("system", WRITER_SYSTEM_PROMPT),
                ("user", "{context}")
            ])
            response = (prompt | llm).invoke({"context": context})
            markdown_output = response.content
            
            calculated_charts = state.get("calculated_charts", {})
            if "allocation_pie" in calculated_charts:
                charts.allocation_pie = [AllocationData(**p) for p in calculated_charts["allocation_pie"]]
            if "evolution_bar" in calculated_charts:
                charts.evolution_bar = [EvolutionData(**b) for b in calculated_charts["evolution_bar"]]
        except Exception as e:
            markdown_output += f"\n\n**Motivo:** Falha de comunicação com o serviço cognitivo Azure OpenAI.\n\nDetalhes Técnicos: `{str(e)}`"
    else:
        markdown_output += "\n\n**Motivo:** A variável `AZURE_OPENAI_KEY` não está configurada."

    draft = FinalReport(
        markdown_text=markdown_output, 
        charts=charts
    )
    return {
        "draft_report": draft,
        "audit_logs": ["ReportWriter: Drafted report (LLM Integration Executed)."]
    }

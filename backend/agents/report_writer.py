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
            personal_goals = client_data.additional_comments or "Nenhum objetivo específico mencionado."
            health_summary = state.get("financial_health_summary", "Não disponível")
            health_rec = state.get("financial_health_recommendation", "Não disponível")
            compliance_feedback = [log for log in state.get("audit_logs", []) if "REJECTED" in log]
            
            context = (
                f"CLIENTE: {client_data.name}, {client_data.age} anos.\n"
                f"OBJETIVOS PESSOAIS: {personal_goals}\n"
                f"SAÚDE FINANCEIRA: {health_summary}\n"
                f"RECOMENDAÇÃO DE SAÚDE: {health_rec}\n"
                f"PRODUTOS SELECIONADOS: {json.dumps(matched_products)}\n"
                f"LOGS DE CÁLCULO: {math_logs}\n"
                f"DISTRIBUIÇÃO EXIGIDA (%): {json.dumps(state.get('calculated_charts', {}).get('allocation_pie', []))}\n"
            )
            
            if compliance_feedback:
                context += f"\nAVISO DE REVISÃO (O RELATÓRIO ANTERIOR FOI REJEITADO): {compliance_feedback[-1]}\n"
                context += "POR FAVOR, CORRIJA OS PONTOS ACIMA E GERE UMA NOVA VERSÃO RESPEITANDO TODAS AS REGRAS."

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

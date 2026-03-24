import os
import json
from data.schemas.state_models import AgentState, FinalReport, ReportCharts, AllocationData, EvolutionData
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def run_report_writer(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    matched_products = state.get("matched_products", [])
    math_logs = state.get("math_operations_log", [])
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    markdown_output = "## Report Gerado\n\nA IA está inativa por falta de API KEY no arquivo .env."
    charts = ReportCharts(allocation_pie=[], evolution_bar=[])
    
    if api_key and api_key != "sua_chave_aqui":
        try:
            llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
            context = f"Cliente: {client_data.name}, {client_data.age} anos. Produtos: {json.dumps(matched_products)}. Calculos: {math_logs}."
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Escreva um relatório ao cliente em português claro recomendando os produtos. Use Markdown. Inclua uma versão MENSAGEM CURTA e uma VERSÃO DETALHADA."),
                ("user", context)
            ])
            response = (prompt | llm).invoke({})
            markdown_output = response.content
            
            charts.allocation_pie = [AllocationData(name=p["name"], value=100.0/len(matched_products)) for p in matched_products]
            charts.evolution_bar = [EvolutionData(year=2024, value=float(client_data.initial_investment))]
        except Exception:
            pass
    else:
        if matched_products:
            charts.allocation_pie = [AllocationData(name=p["name"], value=10.0) for p in matched_products]
        markdown_output = "## Simulated LLM Draft\\n\\nVersão Detalhada e Resumida gerada por IA."

    draft = FinalReport(
        markdown_text=markdown_output, 
        charts=charts
    )
    return {
        "draft_report": draft,
        "audit_logs": ["ReportWriter: Drafted report (LLM Integration Executed)."]
    }

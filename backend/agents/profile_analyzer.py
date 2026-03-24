import os
from data.schemas.state_models import AgentState
from backend.tools.investment_api_mock import get_products_by_risk
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def run_profile_analyzer(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["ProfileAnalyzer: Skipped due to missing ClientData."]}
        
    knowledge = client_data.knowledge_level.value
    horizon = client_data.investment_horizon_months
    
    api_key = os.getenv("OPENAI_API_KEY")
    risk_score = 0.3 
    
    if api_key and api_key != "sua_chave_aqui":
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Você é um especialista em risco. Responda apenas com um número float entre 0.0 e 1.0 representando o apetite de risco deste cliente."),
                ("user", f"Conhecimento: {knowledge}. Horizonte: {horizon} meses. Comentários adicionais: {client_data.additional_comments}")
            ])
            chain = prompt | llm
            response = chain.invoke({})
            try:
                risk_score = float(response.content.strip())
            except ValueError:
                risk_score = 0.5
        except Exception as e:
            pass 
    else:
        if knowledge == "Intermediário":
            risk_score = 0.6
        elif knowledge == "Avançado":
            risk_score = 1.0
            
        if horizon < 12:
            risk_score = min(risk_score, 0.4)
            
    products = get_products_by_risk(risk_score)
    
    return {
        "matched_products": products,
        "audit_logs": [f"ProfileAnalyzer: Assigned risk score {risk_score}. Retrieved {len(products)} products."]
    }

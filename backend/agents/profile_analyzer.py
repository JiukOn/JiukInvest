import os
from data.schemas.state_models import AgentState
from backend.tools.investment_api_mock import get_products_by_risk
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from backend.prompts.system_prompts import STRATEGIST_SYSTEM_PROMPT
from backend.tools.risk_calculator import calculate_risk_bounds
from backend.utils.env_loader import (
    AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_MODEL, 
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_VERSION
)

def run_profile_analyzer(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["ProfileAnalyzer: Skipped due to missing ClientData."]}
        
    knowledge = client_data.knowledge_level.value
    horizon = client_data.investment_horizon_months
    age = client_data.age
    income = float(client_data.monthly_income)
    contribution = float(client_data.monthly_contribution)
    
    past_investments = client_data.past_investments or ""
    accepted_assets = []
    if hasattr(client_data, "asset_preferences") and client_data.asset_preferences and hasattr(client_data.asset_preferences, "accepted_asset_types"):
        accepted_assets = client_data.asset_preferences.accepted_asset_types
        
    comments = client_data.additional_comments or "Sem comentários adicionais."
    
    risk_score = 0.29
    personal_stability = state.get("personal_stability", "SEM INFORMACAO")
    
    if AZURE_OPENAI_KEY:
        try:
            llm = AzureChatOpenAI(
                azure_deployment=AZURE_OPENAI_DEPLOYMENT,
                model_name=AZURE_OPENAI_MODEL,
                api_key=AZURE_OPENAI_KEY,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                api_version=AZURE_OPENAI_VERSION,
                temperature=0
            )
            
            low_score, high_score = calculate_risk_bounds(
                age, knowledge, horizon, income, contribution, accepted_assets, past_investments, personal_stability
            )
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", STRATEGIST_SYSTEM_PROMPT),
                ("user", "Conhecimento: {knowledge}. Horizonte: {horizon} meses. Estabilidade Oculta: {personal_stability}. Low Score Matemático: {low_score}. High Score Matemático: {high_score}. Comentários adicionais: {comments}. Escolha entre o Low ou High score.")
            ])
            chain = prompt | llm
            try:
                response = chain.invoke({
                    "knowledge": knowledge,
                    "horizon": horizon,
                    "personal_stability": personal_stability,
                    "low_score": low_score,
                    "high_score": high_score,
                    "comments": comments
                })
                risk_score = float(response.content.strip())
            except ValueError as ve:
                return {"audit_logs": [f"ProfileAnalyzer: LLM returned non-float response for Risk Score. Error: {str(ve)}"]}
        except Exception as e:
            return {"audit_logs": [f"ProfileAnalyzer: CRITICAL - Failed to call LLM: {str(e)}"]}
    else:
        return {
            "audit_logs": ["ProfileAnalyzer: Aborted. Missing AZURE_OPENAI_KEY in .env."]
        }
            
    all_products = get_products_by_risk(risk_score)
    seen_names = set()
    unique_products = []
    for p in all_products:
        pname = p.get("name", "")
        if pname not in seen_names:
            seen_names.add(pname)
            unique_products.append(p)
    products = sorted(unique_products, key=lambda x: x.get("expected_annual_return", 0), reverse=True)[:5]
    
    return {
        "matched_products": products,
        "risk_score": risk_score,
        "audit_logs": [f"ProfileAnalyzer: Assigned risk score {risk_score}. Retrieved {len(products)} products (Top 5 selected). Thresholds: Conservador (<=0.05), Moderado (0.06-0.29), Arrojado (>=0.30)."]
    }

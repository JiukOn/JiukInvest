import os
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from backend.prompts.system_prompts import EMOTIONAL_ANALYZER_PROMPT
from data.schemas.state_models import AgentState
from backend.utils.env_loader import (
    AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_MODEL, 
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_VERSION
)

def run_emotional_analyzer(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["EmotionalAnalyzer: Aborted. Missing standardized_client_data."]}
        
    comments = client_data.additional_comments or "Sem comentários adicionais."
    
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
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", EMOTIONAL_ANALYZER_PROMPT),
                ("user", "Comentário: {comments}")
            ])
            
            try:
                stability_res = (prompt | llm).invoke({"comments": comments})
                personal_stability = stability_res.content.strip().upper()
                
                return {
                    "personal_stability": personal_stability,
                    "audit_logs": [f"EmotionalAnalyzer: Stability classified as '{personal_stability}'"]
                }
            except Exception as e:
                return {
                    "personal_stability": "ESTAVEL", # Default fallback
                    "audit_logs": [f"EmotionalAnalyzer: Failed to extract emotional stability via LLM. ⚠️ Error: {str(e)}"]
                }
        except Exception as e:
            return {"audit_logs": [f"EmotionalAnalyzer: CRITICAL - Failed to initialize LLM: {str(e)}"]}
    else:
        return {
            "audit_logs": ["EmotionalAnalyzer: Aborted. Missing AZURE_OPENAI_KEY in .env."]
        }

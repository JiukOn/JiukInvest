from langchain_openai import AzureChatOpenAI
from backend.utils.env_loader import (
    AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_MODEL,
    AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_VERSION
)

def get_llm(temperature: float = 0) -> AzureChatOpenAI:
    if not AZURE_OPENAI_KEY:
        raise ValueError("AZURE_OPENAI_KEY is not set in the environment.")
    return AzureChatOpenAI(
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        model_name=AZURE_OPENAI_MODEL,
        api_key=AZURE_OPENAI_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_VERSION,
        temperature=temperature,
    )

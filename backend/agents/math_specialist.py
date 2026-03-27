import json
import logging
import inspect
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import StructuredTool
from data.schemas.state_models import AgentState
from backend.utils.llm_factory import get_llm
from backend.utils.env_loader import AZURE_OPENAI_KEY
from backend.prompts.system_prompts import MATH_SPECIALIST_PROMPT

# Import tool modules
import backend.tools.math_tools as math_tools
import backend.tools.risk_calculator as risk_calc

logger = logging.getLogger(__name__)

def _get_all_tools() -> List[StructuredTool]:
    """Dynamically creates LangChain tools from the specified modules."""
    tools = []
    modules = [math_tools, risk_calc]
    
    for module in modules:
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith("_"):
                # Use docstring as description
                desc = obj.__doc__ or f"Executa a função {name}"
                tools.append(StructuredTool.from_function(
                    func=obj,
                    name=name,
                    description=desc
                ))
    return tools

def run_math_specialist(state: AgentState) -> dict:
    client_data = state.get("standardized_client_data")
    if not client_data:
        return {"audit_logs": ["MathSpecialist: Skipped. Missing ClientData."]}

    principal = float(client_data.initial_investment)
    contribution = float(client_data.monthly_contribution)
    months = int(client_data.investment_horizon_months)
    client_score = state.get("risk_score", 0.5)
    matched_products = state.get("matched_products", [])

    if not matched_products:
        return {"audit_logs": ["MathSpecialist: Aborted. No matched_products from ProfileAnalyzer."]}

    if not AZURE_OPENAI_KEY:
        return _fallback_math_logic(principal, contribution, months, client_score, matched_products, "No API Key")

    try:
        llm = get_llm(temperature=0)
        available_tools = _get_all_tools()
        llm_with_tools = llm.bind_tools(available_tools)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", MATH_SPECIALIST_PROMPT),
            ("user", (
                "Cliente: {name}\n"
                "Capital Inicial: R$ {principal}\n"
                "Aporte Mensal: R$ {contribution}\n"
                "Prazo: {months} meses\n"
                "Score de Risco do Cliente: {score}\n"
                "Produtos Disponíveis: {products}"
            ))
        ])
        
        math_logs = []
        results = {}
        
        # Tool Map for easy access
        tool_map = {t.name: t.func for t in available_tools}
        
        # Invoke with variables
        ai_msg = (prompt | llm_with_tools).invoke({
            "name": client_data.name,
            "principal": principal,
            "contribution": contribution,
            "months": months,
            "score": client_score,
            "products": json.dumps(matched_products, ensure_ascii=False)
        })
        
        if ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                t_name = tool_call["name"]
                t_args = tool_call["args"]
                
                if t_name in tool_map:
                    try:
                        res = tool_map[t_name](**t_args)
                        # Log to frontend in real-time
                        log_msg = f"Tool Execution: {t_name}({t_args}) -> Result captured."
                        math_logs.append(log_msg)
                        logger.info(log_msg)
                        
                        # Store specific results for the final payload
                        if t_name == "get_compound_interest_projection":
                            results["evolution_bar"] = res
                        elif t_name == "get_portfolio_allocation":
                            results["allocation_pie"] = res
                        else:
                            # Generic log for other tools (Tax, Inflation, etc.)
                            math_logs.append(f"DEBUG [{t_name}]: {json.dumps(res, ensure_ascii=False)}")
                    except Exception as te:
                        math_logs.append(f"Error calling {t_name}: {str(te)}")

        # Mandatory fallbacks if LLM forgot crucial tools
        if "evolution_bar" not in results:
            total_ret = sum(p.get("expected_annual_return", 0.0) for p in matched_products)
            avg_ret = total_ret / len(matched_products) if matched_products else 0.0
            results["evolution_bar"] = math_tools.get_compound_interest_projection(principal, contribution, avg_ret, months)
            math_logs.append("Auto-Fallback: get_compound_interest_projection executed.")
            
        if "allocation_pie" not in results:
            results["allocation_pie"] = math_tools.get_portfolio_allocation(principal, client_score, matched_products)
            math_logs.append("Auto-Fallback: get_portfolio_allocation executed.")

        final_val = results["evolution_bar"][-1]["value"] if results["evolution_bar"] else 0.0
        
        return {
            "math_operations_log": math_logs,
            "audit_logs": [
                f"MathSpecialist (LLM): {len(math_logs)} operações matemáticas registradas. Valor final: R$ {round(final_val, 2)}."
            ],
            "calculated_charts": {
                "evolution_bar": results["evolution_bar"],
                "allocation_pie": results["allocation_pie"]
            },
            "risk_score": client_score # Ensure it persists
        }

    except Exception as e:
        logger.error(f"Error in MathSpecialist: {e}")
        return _fallback_math_logic(principal, contribution, months, client_score, matched_products, str(e))

def _fallback_math_logic(principal, contribution, months, client_score, matched_products, error_msg) -> dict:
    evolution = math_tools.get_compound_interest_projection(principal, contribution, 0.0, months)
    allocation = math_tools.get_portfolio_allocation(principal, client_score, matched_products)
    return {
        "math_operations_log": [f"Fallback: {error_msg}"],
        "audit_logs": [f"MathSpecialist (Error Fallback): {error_msg}"],
        "calculated_charts": {"evolution_bar": evolution, "allocation_pie": allocation}
    }

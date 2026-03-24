from data.schemas.state_models import AgentState, ClientData

def run_data_organizer(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})
    
    try:
        if isinstance(raw_input, ClientData):
            client_data = raw_input
        else:
            client_data = ClientData(**raw_input)
            
        return {
            "standardized_client_data": client_data,
            "status_code": 200,
            "audit_logs": ["DataOrganizer: JSON Payload successfully validated and parsed using Pydantic."]
        }
    except Exception as e:
        return {
            "standardized_client_data": None,
            "status_code": 400,
            "audit_logs": [f"DataOrganizer: Validation Failed. Pydantic Error: {str(e)}"]
        }

from data.schemas.state_models import AgentState, ClientData, AssetPreferences, KnowledgeLevel

def _sanitize_str(value, default=None):
    if value is None or str(value).strip() in ("", "null", "undefined", "None"):
        return default
    return str(value).strip()

def _sanitize_float(value, default=0.0):
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return default

def _sanitize_int(value, default=0):
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default

def _sanitize_bool(value, default=True):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() not in ("false", "0", "no", "nao", "nao")
    return default

def run_data_organizer(state: AgentState) -> dict:
    raw_input = state.get("raw_input", {})

    try:
        if isinstance(raw_input, ClientData):
            return {
                "standardized_client_data": raw_input,
                "status_code": 200,
                "audit_logs": ["DataOrganizer: ClientData object received directly. Validation skipped."]
            }

        name = _sanitize_str(raw_input.get("name"))
        if not name:
            return {
                "standardized_client_data": None,
                "status_code": 400,
                "audit_logs": ["DataOrganizer: CRITICAL - 'name' field is missing or empty. Cannot proceed."]
            }

        age = _sanitize_int(raw_input.get("age"), default=0)
        monthly_income = _sanitize_float(raw_input.get("monthly_income"))
        monthly_contribution = _sanitize_float(raw_input.get("monthly_contribution"))
        initial_investment = _sanitize_float(raw_input.get("initial_investment"))
        investment_horizon_months = _sanitize_int(raw_input.get("investment_horizon_months"), default=12)
        investment_horizon_months = max(6, min(420, investment_horizon_months))

        raw_knowledge = _sanitize_str(raw_input.get("knowledge_level"), default="Iniciante")
        knowledge_map = {
            "iniciante": KnowledgeLevel.BEGINNER,
            "intermediário": KnowledgeLevel.INTERMEDIATE,
            "intermediario": KnowledgeLevel.INTERMEDIATE,
            "avançado": KnowledgeLevel.ADVANCED,
            "avancado": KnowledgeLevel.ADVANCED,
        }
        knowledge_level = knowledge_map.get(raw_knowledge.lower(), KnowledgeLevel.BEGINNER)

        has_invested_before = _sanitize_bool(raw_input.get("has_invested_before"), default=False)
        past_investments = _sanitize_str(raw_input.get("past_investments"))
        additional_comments = _sanitize_str(raw_input.get("additional_comments"))

        asset_prefs = None
        if any(k in raw_input for k in ["accepts_public_titles", "accepts_private_titles", "accepts_national", "accepts_international", "accepted_asset_types"]):
            asset_prefs = AssetPreferences(
                accepts_public_titles=_sanitize_bool(raw_input.get("accepts_public_titles"), True),
                accepts_private_titles=_sanitize_bool(raw_input.get("accepts_private_titles"), True),
                accepts_national=_sanitize_bool(raw_input.get("accepts_national"), True),
                accepts_international=_sanitize_bool(raw_input.get("accepts_international"), False),
                accepted_asset_types=raw_input.get("accepted_asset_types", []),
            )

        client_data = ClientData(
            name=name,
            age=age,
            knowledge_level=knowledge_level,
            has_invested_before=has_invested_before,
            past_investments=past_investments,
            investment_horizon_months=investment_horizon_months,
            monthly_income=monthly_income,
            monthly_contribution=monthly_contribution,
            initial_investment=initial_investment,
            asset_preferences=asset_prefs,
            additional_comments=additional_comments,
        )

        logs = [
            f"DataOrganizer: Client '{name}' validated. Age={age}, Income=R${monthly_income}, Contribution=R${monthly_contribution}, Investment=R${initial_investment}, Horizon={investment_horizon_months}mo, Knowledge='{knowledge_level.value}', HasInvested={has_invested_before}."
        ]
        return {
            "standardized_client_data": client_data,
            "status_code": 200,
            "audit_logs": logs,
        }

    except Exception as e:
        return {
            "standardized_client_data": None,
            "status_code": 400,
            "audit_logs": [f"DataOrganizer: Validation Failed. Error: {str(e)}"]
        }

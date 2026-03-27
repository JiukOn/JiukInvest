# JiukInvest Data Layer — Contratos, Mocks e Schemas

> Módulo central de padronização de dados do JiukInvest. Define os contratos de tipagem que transitam pelo pipeline multi-agente e fornece os artefatos estáticos que simulam a infraestrutura de produtos e clientes do banco.

---

## 📂 Estrutura do Diretório

```
data/
├── schemas/
│   └── state_models.py       # Contratos Pydantic: AgentState, ClientData, FinalReport
├── mocks/
│   ├── product_catalog.json  # Catálogo de produtos financeiros (18 ativos)
│   └── mock_clients.json     # Perfis de clientes pré-cadastrados para demonstração
├── blacklist.txt             # Log legível de clientes bloqueados (gerado em runtime)
└── blacklist_log.json        # Blacklist estruturada em JSON (gerado em runtime)
```

> **Nota:** `blacklist.txt` e `blacklist_log.json` são gerados automaticamente em runtime pelo `ContextAnalyzer` ao detectar uma violação AML. Não são versionados.

---

## 📋 `/schemas/state_models.py` — Contratos de Tipagem

Este arquivo define a **espinha dorsal do sistema**. Qualquer dado que trafega entre os 9 agentes do pipeline LangGraph está tipado aqui.

### `ClientData` — Input Validado do Cliente

| Campo | Tipo | Descrição |
|---|---|---|
| `name` | `str` | Nome completo do cliente |
| `age` | `int` (≥ 0) | Idade — determina elegibilidade demográfica |
| `knowledge_level` | `KnowledgeLevel` | `Iniciante` / `Intermediário` / `Avançado` |
| `has_invested_before` | `bool` | Experiência prévia com investimentos |
| `past_investments` | `str?` | Descreve ativos ou histórico anterior |
| `investment_horizon_months` | `int` [6–420] | Horizonte de investimento em meses |
| `monthly_income` | `float` (≥ 0) | Renda mensal bruta |
| `monthly_contribution` | `float` (≥ 0) | Aporte mensal planejado |
| `initial_investment` | `float` (≥ 0) | Patrimônio disponível para investir |
| `asset_preferences` | `AssetPreferences?` | Preferências de classes de ativos |
| `additional_comments` | `str?` | Contexto qualitativo do cliente |

### `AgentState` — Memória Transitória do Pipeline (19 campos)

| Campo | Produtor | Consumidor |
|---|---|---|
| `raw_input` | FastAPI Routes | DataOrganizer |
| `standardized_client_data` | DataOrganizer | Todos os agentes |
| `is_blacklisted` | ContextAnalyzer | Orchestrator (guarda AML) |
| `blacklist_reason` | ContextAnalyzer | Routes SSE |
| `demographic_category` | DemographicAuditor | Orchestrator (guarda demog.) |
| `demographic_lifecycle_note` | DemographicAuditor | ReportWriter |
| `financial_health_warning` | FinancialHealthAgent | ReportWriter |
| `financial_health_score` | FinancialHealthAgent | Orchestrator (guarda health) |
| `financial_health_summary` | FinancialHealthAgent | ReportWriter |
| `financial_health_recommendation` | FinancialHealthAgent | Routes SSE |
| `personal_stability` | EmotionalAnalyzer | ProfileAnalyzer |
| `risk_score` | ProfileAnalyzer | MathSpecialist, Routes SSE |
| `matched_products` | ProfileAnalyzer | MathSpecialist |
| `calculated_charts` | MathSpecialist | Routes SSE → Frontend |
| `math_operations_log` | MathSpecialist | Routes SSE (`math_log`) |
| `draft_report` | ReportWriter | ComplianceChecker |
| `final_report` | ComplianceChecker | Routes SSE → Frontend |
| `status_code` | Routes + Agents | Routes |
| `audit_logs` | **Todos** (append) | Routes SSE (`log` events) |

### `FinalReport` — Estrutura de Saída

```python
class FinalReport(BaseModel):
    markdown_text: str          # Relatório completo em Markdown
    charts: ReportCharts        # Dados dos gráficos

class ReportCharts(BaseModel):
    allocation_pie: List[AllocationData]   # Distribuição de ativos
    evolution_bar: List[EvolutionData]     # Série temporal de evolução

class EvolutionData(BaseModel):
    year: str            # "Mar/2026" (mensal) ou "2031" (anual)
    value: float         # Projeção JiukInvest (R$)
    value_poupanca: float  # Benchmark poupança (R$)
    value_ibov: float      # Benchmark Ibovespa (R$)
```

---

## 🗂️ `/mocks/product_catalog.json` — Catálogo de Produtos

Arquivo JSON com **38+ produtos financeiros** estruturados (expandido para cobrir todas as variantes de risco). Consumido pelo `investment_api_mock.py` para seleção baseada no `risk_score`.

### Estrutura de cada produto

```json
{
  "id": "PROD001",
  "name": "Tesouro IPCA+ 2035",
  "type": "Renda Fixa",
  "risk_score": 0.10,
  "expected_annual_return": 7.5,
  "liquidity": "D+1",
  "min_investment": 50.0,
  "description": "Título público federal indexado à inflação (IPCA)."
}
```

### Regras de Filtragem e Segurança
- **Paralelismo AML**: O `ContextAnalyzer` opera em paralelo com outros auditores. Ao detectar uma violação, ele encerra o fluxo global e grava instantaneamente na blacklist.
- **Persistent Hardening**: Uma vez na blacklist, o cliente (por nome normalizado) é bloqueado em todas as submissões futuras, mesmo após reinicialização do servidor, graças à persistência dual (JSON/TXT).
- **Limite de Concentração**: O sistema impõe um teto de 31% por ativo, forçando a diversificação real.
- **Catalog Grounding**: A IA está restrita aos 38 ativos do catálogo; qualquer tentativa de sugerir ativos externos é interceptada no `ComplianceChecker`.

### Distribuição de Risco no Catálogo

| Faixa | Tipo | Exemplos |
|---|---|---|
| 0.05 – 0.15 | Conservador | Tesouro Selic, CDB DI, Poupança Premium |
| 0.20 – 0.40 | Moderado | Tesouro IPCA+, CDB Pré, LCI, LCA |
| 0.45 – 0.65 | Moderado-Arrojado | FIIs, Debêntures, Fundo Multimercado |
| 0.70 – 0.85 | Arrojado | Ações Nacionais, ETF, Fundo ESG |
| > 0.90 | Excluído | Alta especulação — bloqueado pelo sistema |

---

## 👥 `/mocks/mock_clients.json` — Perfis de Demonstração

Base de clientes pré-cadastrados usada pelo `ClientSelector` no frontend para preencher o formulário rapidamente. Cada cliente possui:

| Campo | Descrição |
|---|---|
| `client_id` | Identificador único |
| `name` | Nome completo |
| `age` | Idade |
| `suitability_profile` | `Conservador` / `Moderado` / `Arrojado` |
| `monthly_income` | Renda mensal (R$) |
| `total_assets` | Patrimônio total (R$) |
| `average_ticket` | Aporte médio mensal (R$) |
| `investment_knowledge` | Nível de conhecimento |
| `time_horizon` | `Curto Prazo` / `Longo Prazo` |
| `active_products` | Lista de ativos que o cliente possui |
| `investment_objective` | Objetivo declarado |

O `api.js` no frontend converte este formato para `ClientData` via `mapMockToFormData()`.

---

## 🔒 Blacklist Persistente (gerada em runtime)

O `ContextAnalyzer` grava automaticamente clientes bloqueados por violações AML em dois formatos:

### `blacklist.txt` — Log Humano Legível

```
[2026-03-25T18:03:00] Name: João Exemplo | Age: 40 | Reason: AML keyword detected: 'droga' | Background: ...
```

### `blacklist_log.json` — Estrutura para Lookups

```json
[
  {
    "timestamp": "2026-03-25T18:03:00",
    "name": "João Exemplo",
    "age": 40,
    "reason": "AML keyword detected: 'droga'",
    "background_excerpt": "..."
  }
]
```

A busca de blacklist é feita com **normalização case-insensitive** — "João Exemplo" e "joão exemplo" são tratados como o mesmo cliente.

---

## 🛡️ Princípios de Engenharia

| Princípio | Como é aplicado |
|---|---|
| **Single Source of Truth** | Qualquer mudança nos dados transita por `state_models.py` |
| **Validação Estrita** | Pydantic rejeita payloads malformados antes de chegar ao LLM |
| **Grounding Anti-Alucinação** | Produtos vêm do catálogo JSON — o LLM não pode inventar ativos |
| **Desacoplamento de Produção** | Substituir os mocks JSON por conexão a banco de dados real exige zero refatoração dos agentes |
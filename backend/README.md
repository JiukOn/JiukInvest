# JiukInvest Backend — Motor de Orquestração GenAI

> **Wealth Management assistido por Inteligência Artificial** — Pipeline multi-agente, stateful, orientado a compliance e segurança financeira.

Este módulo é o núcleo de inteligência do **JiukInvest**. Implementado em **Python + FastAPI + LangGraph**, não se trata de uma API que chama um LLM diretamente, mas de um **Stateful Agentic Workflow** com 9 agentes autônomos especializados, 4 guardrails de bloqueio, 5 ferramentas determinísticas e um sistema de logs em tempo real (SSE).

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| API Framework | FastAPI + Uvicorn (ASGI assíncrono) |
| Orquestração | LangGraph (`StateGraph` com `Conditional Edges`) |
| LLM Interface | LangChain + Azure OpenAI (GPT-4o) |
| Validação | Pydantic v2 (`AgentState`, `ClientData`, `FinalReport`) |
| Schema de Estado | `TypedDict` tipado (19 campos) |
| Streaming | Server-Sent Events (SSE) — `text/event-stream` |
| Segurança | AML Keyword Detection + Regex Injection Guard |
| Persistência | Blacklist dual-storage: `.txt` + `.json` |

---

## 📂 Estrutura do Projeto

```
backend/
├── main.py                     # Entrypoint ASGI — FastAPI + CORS
├── graph_orchestrator.py       # Máquina de estados LangGraph
├── agents/
│   ├── data_organizer.py       # Agente 1 — Sanitização e validação do payload
│   ├── context_analyzer.py     # Agente 2 — AML + Detecção de injeção de prompt
│   ├── demographic_auditor.py  # Agente 3 — LLM — Perfil demográfico e ciclo de vida
│   ├── financial_health_agent.py  # Agente 4 — LLM — Saúde financeira (CFP analysis)
│   ├── emotional_analyzer.py   # Agente 5 — LLM — Estabilidade emocional/comportamental
│   ├── profile_analyzer.py     # Agente 6 — LLM — Score de risco + seleção de produtos
│   ├── math_specialist.py      # Agente 7 — Projeções, alocação com cap 31% e benchmarks
│   ├── report_writer.py        # Agente 8 — LLM — Redação personalizada do relatório
│   └── compliance_checker.py   # Agente 9 — LLM — Revisão ética e legal do relatório
├── api/
│   └── routes.py               # POST /api/copilot/generate — SSE streaming
├── prompts/
│   └── system_prompts.py       # Repositório central de system prompts
├── tools/
│   ├── risk_calculator.py      # Cálculo determinístico de score (Low/High bounds)
│   ├── financial_calculator.py # Juros compostos e projeção matemática
│   ├── math_tools.py           # Toolkit: Sharpe, volatilidade, IR, clamp, power, %
│   ├── investment_api_mock.py  # Leitor do catálogo de produtos filtrado por risk_score
│   └── blacklist_manager.py    # Persistência da blacklist em TXT + JSON
└── utils/
    ├── env_loader.py            # Carregamento e export de variáveis de ambiente
    └── llm_factory.py          # Fábrica centralizada de instâncias AzureChatOpenAI
```

---

## 🔄 Máquina de Estados — Pipeline de 9 Agentes

O estado global tipado (`AgentState`, 19 campos) trafega pelo grafo. Cada nó pode **mutá-lo ou encerrar o fluxo**:

```
START
  │
  ▼
[DataOrganizer]  ──[INVALID]──► END (400)
  │
  ▼
[ContextAnalyzer]  ──[AML/INJECTION]──► END (blacklisted)
  │
  ▼
[Demographics]  ──[CHILD/TEEN]──► END (restricted)
  │
  ▼
[HealthCheck]  ──[CRITICO]──► END (health_critical)
  │
  ▼
[EmotionalAnalyzer]
  │
  ▼
[ProfileAnalyzer]  (LLM — Risk Score + Product Selection)
  │
  ▼
[MathSpecialist]  (Juros compostos + Alocação com cap 31% + Benchmarks)
  │
  ▼
[ReportWriter]  (LLM — Markdown personalizado por perfil)
  │
  ▼
[Compliance]  ──[REJECTED]──► END (406)
  │
  ▼
END  → SSE result:success → Frontend
```

### Guardas de Bloqueio (Conditional Edges)

| Guarda | Condição de Bloqueio |
|---|---|
| `should_continue_after_data` | `standardized_client_data` ausente ou `status_code=400` |
| `should_block_aml` | `is_blacklisted=True` (AML keyword ou injeção detectada) |
| `should_block_demographics` | `demographic_category` in `["CHILD", "TEEN"]` |
| `should_block_health` | `financial_health_score == "CRITICO"` |

---

## 🤖 Agentes — Responsabilidades Detalhadas

### 1. `DataOrganizer` — Sanitização e Validação
- Sanitiza todos os campos do payload com funções `_sanitize_str/float/int/bool`
- Normaliza `KnowledgeLevel` (e.g., "avancado" → `ADVANCED`)
- Restringe `investment_horizon_months` ao intervalo `[6, 420]`
- Emite log detalhado com todos os campos do cliente validados
- **Tipo:** Determinístico

### 2. `ContextAnalyzer` — Segurança AML & Guardrail de Prompt
- **45+ palavras-chave AML** cobrindo: drogas, lavagem de dinheiro, extorsão, fraude, pirâmides, contrabando
- **12 padrões regex** para detecção de prompt injection ("ignore previous instructions", "jailbreak", etc.)
- Ao detectar violação: chama `blacklist_manager.add_to_blacklist()` → persiste em `.txt` + `.json`
- Verifica `is_blacklisted()` no início — clientes banidos são bloqueados imediatamente
- **Tipo:** Determinístico (AML não pode depender de LLM)

### 3. `DemographicAuditor` — Perfil Demográfico (LLM)
- Classifica: `CHILD` (<13) / `TEEN` (13-15) / `ADULT` (16-64) / `SENIOR` (65+)
- Gera nota de **ciclo de vida** (ex: "fase de acumulação patrimonial ativa")
- Fallback determinístico por faixa etária se LLM indisponível
- **Tipo:** LLM com fallback

### 4. `FinancialHealthAgent` — Saúde Financeira CFP (LLM)
- Analisa: renda, aporte, patrimônio, horizonte, histórico, comentários
- Classifica em: `SAUDAVEL` / `ATENCAO` / `CRITICO`
- Retorna `summary` narrativo + `recommendation` curta
- Hard block determinístico antes do LLM: `contribution > income` → `CRITICO` instantâneo
- **Tipo:** LLM com hard guard determinístico

### 5. `EmotionalAnalyzer` — Análise Comportamental (LLM)
- Analisa os comentários do cliente e classifica: `ESTAVEL` / `INSTAVEL` / `MEDIO` / `SEM INFORMACAO`
- Output alimenta o `ProfileAnalyzer` para ajuste de score
- **Tipo:** LLM

### 6. `ProfileAnalyzer` — Risk Score + Seleção de Produtos (LLM + Tool)
- Chama `risk_calculator.calculate_risk_bounds()` → gera `(low_score, high_score)` determinístico
- O LLM Estrategista analisa comentários e decide qual score usar, com ajustes emocionais:
  - `INSTAVEL` → penalidade de `-0.05`
  - `ESTAVEL` + experiente → bônus de `+0.03`
- Busca produtos via `investment_api_mock.get_products_by_risk()` → filtra por `risk_score ≤ max(score, 0.90)`
- Deduplica por nome antes do Top 5
- **Tipo:** LLM + Tools

### 7. `MathSpecialist` — Projeções e Alocação
- Converte retorno anual → taxa mensal via fórmula composta correta: `(1+r)^(1/12) - 1`
- Gera série temporal de evolução patrimonial vs. **Poupança** e **Ibovespa** (benchmarks)
- Calcula alocação por **afinidade de score** (`1 - |p_risk - client_score|^4`)
- Aplica **cap de 31%** por ativo com redistribuição proporcional do excedente
- Emite `math_operations_log` como trace de chamadas de ferramenta
- **Tipo:** Determinístico (matemática não pode ser alucinada)

### 8. `ReportWriter` — Redação do Relatório (LLM)
- Tom personalizado por perfil: conservador → enfatiza segurança; jovem → menciona poder do tempo; instável → tranquilizador
- Estrutura obrigatória: Saudação, Perfil de Risco, Resumo Executivo, Tabela de Portfólio, Análise de Ativos, Projeção de Crescimento
- Nunca cita códigos internos, funções ou ferramentas
- **Tipo:** LLM

### 9. `ComplianceChecker` — Revisão Ética e Legal (LLM + Regex Guard)
- Regex guard roda primeiro: bloqueia vazamento de identificadores internos (`PROD001`, `backend/`, `.py`)
- LLM Compliance Officer verifica: garantias proibidas, afirmações falsas, linguagem inadequada
- Retorna `approved: true/false` + `violations` lista
- **Tipo:** LLM com regex hard guard

---

## 🔧 Ferramentas (Tools)

| Tool | Tipo | Função |
|---|---|---|
| `risk_calculator.py` | Determinístico | Score ponderado por 7 variáveis (age, knowledge, horizon, income ratio, stability, assets, history) |
| `financial_calculator.py` | Determinístico | Juros compostos com aporte mensal recorrente |
| `math_tools.py` | Determinístico | `sharpe_ratio`, `volatility`, `ir_on_rf`, `ir_on_equity`, `clamp`, `power`, `usd_to_brl`, operações % |
| `investment_api_mock.py` | I/O | Leitor do `product_catalog.json` — filtra por `risk_score` com cap de 0.90 |
| `blacklist_manager.py` | I/O Persistente | Grava e consulta clientes bloqueados em `data/blacklist.txt` + `data/blacklist_log.json` |

---

## 📡 API Endpoint

### `POST /api/copilot/generate`

**Content-Type:** `application/json`  
**Response:** `text/event-stream` (SSE)

**Payload de entrada:**
```json
{
  "payload": {
    "name": "João Carlos Oliveira",
    "age": 35,
    "knowledge_level": "Intermediário",
    "has_invested_before": true,
    "past_investments": "CDB, Tesouro Direto",
    "investment_horizon_months": 60,
    "monthly_income": 8000.0,
    "monthly_contribution": 2000.0,
    "initial_investment": 50000.0,
    "additional_comments": "Busco crescimento mas com segurança.",
    "accepts_national": true,
    "accepts_international": false,
    "accepted_asset_types": ["ações", "fundo multimercado"]
  }
}
```

**Eventos SSE emitidos:**

| Tipo | Descrição |
|---|---|
| `log` | Log de auditoria por agente, em tempo real |
| `math_log` | Trace de cálculos matemáticos do MathSpecialist |
| `result` (status: `success`) | Relatório final com `report`, `charts`, `health_score`, `risk_score` |
| `result` (status: `blocked`) | Cliente bloqueado por AML/blacklist |
| `result` (status: `restricted`) | Menor de idade — não elegível |
| `result` (status: `health_critical`) | Saúde financeira crítica — aporte > renda |
| `result` (status: `validation_error`) | Payload inválido — erro de campo |
| `error` | Exceção não tratada |

---

## 🔒 Segurança e Compliance

### Guardrail em Camadas

```
Camada 1 — Sanitização (DataOrganizer): campos normalizados antes de qualquer processamento
Camada 2 — AML/Injection (ContextAnalyzer): 45 keywords + 12 regex patterns (determinístico)
Camada 3 — Blacklist Permanente (blacklist_manager): TXT + JSON, busca normalizada case-insensitive
Camada 4 — Elegibilidade (DemographicAuditor): menores não acessam trilha de investimentos
Camada 5 — Saúde Financeira (FinancialHealthAgent): aporte > renda bloqueia o pipeline
Camada 6 — Compliance de Conteúdo (ComplianceChecker): LLM revisa o relatório antes da entrega
```

### Escala de Risco (Régua Corporativa)

| Range | Perfil |
|---|---|
| 0.000 – 0.050 | **Conservador** — preservação e liquidez |
| 0.051 – 0.290 | **Moderado** — equilíbrio crescimento/proteção |
| 0.300 – 1.000 | **Arrojado** — foco em multiplicação de capital |

> Produtos com `risk_score > 0.90` são automaticamente excluídos do catálogo — classificados como excessivamente especulativos.

---

## 🚀 Deployment Local

### Pré-requisitos

Configure o arquivo `.env` na raiz do projeto:

```env
AZURE_OPENAI_KEY=sua-chave-aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_VERSION=2024-02-15-preview
```

### Inicialização

```bash
# Na raiz do projeto
export PYTHONPATH=$(pwd)

# Ativação do ambiente virtual
.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# Execução
python backend/main.py
# Servidor disponível em: http://localhost:8000
```

> O frontend deve ser iniciado separadamente em `frontend/` com `npm run dev`.

---

## 📊 AgentState — Esquema de Estado (19 campos)

| Campo | Tipo | Produtor |
|---|---|---|
| `raw_input` | `Dict` | FastAPI routes.py |
| `standardized_client_data` | `ClientData` | DataOrganizer |
| `is_blacklisted` | `bool` | ContextAnalyzer |
| `blacklist_reason` | `str?` | ContextAnalyzer |
| `demographic_category` | `str` | DemographicAuditor |
| `demographic_lifecycle_note` | `str?` | DemographicAuditor |
| `financial_health_warning` | `bool` | FinancialHealthAgent |
| `financial_health_score` | `str?` | FinancialHealthAgent |
| `financial_health_summary` | `str?` | FinancialHealthAgent |
| `financial_health_recommendation` | `str?` | FinancialHealthAgent |
| `personal_stability` | `str` | EmotionalAnalyzer |
| `risk_score` | `float` | ProfileAnalyzer |
| `matched_products` | `List[Dict]` | ProfileAnalyzer |
| `calculated_charts` | `Dict` | MathSpecialist |
| `math_operations_log` | `List[str]` | MathSpecialist |
| `draft_report` | `FinalReport?` | ReportWriter |
| `final_report` | `FinalReport?` | ComplianceChecker |
| `status_code` | `int` | Routes + Agents |
| `audit_logs` | `List[str]` (append) | Todos os agentes |
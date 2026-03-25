# JiukInvest — Plataforma de Wealth Management com IA Generativa

> **Pipeline multi-agente, stateful e orientado a compliance** para geração de estratégias de investimento hiperpersonalizadas, com rastreabilidade em tempo real via SSE.

---

## 🎯 Visão do Produto

O **JiukInvest** é um copiloto de wealth management para gerentes bancários. Dado um perfil financeiro e comportamental de um cliente, o sistema orquestra **9 agentes de IA autônomos** que analisam, calculam, redigem e revisam automaticamente um relatório estratégico completo — com gráficos de evolução patrimonial e comparação com benchmarks de mercado.

### Diferenciais Técnicos

| Pilar | Implementação |
|---|---|
| **Workflow Agêntico** | LangGraph `StateGraph` com 4 guardas de bloqueio condicional |
| **Determinismo Matemático** | LLM nunca calcula — aciona ferramentas Python determinísticas |
| **Guardrail AML em Camadas** | 45 keywords + 12 regex de injeção + blacklist persistente |
| **Compliance LLM-as-a-Judge** | 9º agente revisa o relatório antes de entregá-lo |
| **Concentração Máxima 31%** | Cap automático por ativo com redistribuição proporcional |
| **Benchmarks Integrados** | Evolução projetada vs. Poupança e Ibovespa |
| **SSE em Tempo Real** | Cada agente emite log ao frontend durante execução |

---

## 🏗️ Arquitetura do Sistema

```
┌────────────────────┐     SSE Stream      ┌──────────────────────────────────────┐
│   Frontend (React) │ ◄─────────────────── │         Backend (FastAPI)            │
│   Vite + Recharts  │                      │                                      │
│   Glassmorphism UI │ ─── POST /api/ ────► │  LangGraph StateGraph (9 agentes)    │
└────────────────────┘                      │                                      │
                                            │  [DataOrganizer] → [ContextAnalyzer] │
┌────────────────────┐                      │  → [Demographics] → [HealthCheck]    │
│   Data Layer       │ ◄── leitura ──────── │  → [EmotionalAnalyzer]               │
│   Pydantic Schemas │                      │  → [ProfileAnalyzer] → [Math]        │
│   Product Catalog  │                      │  → [ReportWriter] → [Compliance]     │
│   Mock Clients     │                      └──────────────────────────────────────┘
│   Blacklist TXT/JSON│
└────────────────────┘
```

---

## 📂 Estrutura do Repositório

```
projetos-beca-2026/
├── backend/                    # Motor de orquestração — FastAPI + LangGraph
│   ├── main.py                 # Entrypoint ASGI
│   ├── graph_orchestrator.py   # Máquina de estados com 4 guardas condicionais
│   ├── agents/                 # 9 agentes autônomos especializados
│   │   ├── data_organizer.py   # Sanitização e validação de payload
│   │   ├── context_analyzer.py # AML + detecção de injeção de prompt
│   │   ├── demographic_auditor.py  # LLM — ciclo de vida e elegibilidade
│   │   ├── financial_health_agent.py  # LLM CFP — saúde financeira
│   │   ├── emotional_analyzer.py   # LLM — análise comportamental
│   │   ├── profile_analyzer.py     # LLM — risk score + seleção de produtos
│   │   ├── math_specialist.py      # Projeções + alocação + benchmarks
│   │   ├── report_writer.py        # LLM — redação personalizada
│   │   └── compliance_checker.py   # LLM — revisão ética e legal
│   ├── api/routes.py           # POST /api/copilot/generate (SSE)
│   ├── prompts/system_prompts.py  # Repositório de 6 system prompts
│   ├── tools/                  # Ferramentas determinísticas
│   │   ├── risk_calculator.py     # Score ponderado por 7 variáveis
│   │   ├── financial_calculator.py  # Juros compostos com aportes
│   │   ├── math_tools.py          # Sharpe, volatilidade, IR, clamp, %
│   │   ├── investment_api_mock.py  # Leitor do catálogo de produtos
│   │   └── blacklist_manager.py   # Persistência dual TXT + JSON
│   └── utils/
│       ├── env_loader.py          # Variáveis de ambiente Azure
│       └── llm_factory.py         # Fábrica centralizada AzureChatOpenAI
│
├── frontend/                   # Interface React — Glassmorphism 2.0
│   └── src/
│       ├── components/         # Header, Form, ReportDisplay, StatusTimeline, Charts
│       ├── hooks/useLangGraph.js  # SSE consumer com SSE_STEP_MAP real
│       ├── services/api.js     # fetch nativo — generateReport + fetchMockProfiles
│       └── utils/exportPdf.js  # Print CSS → PDF
│
├── data/                       # Contratos, mocks e blacklist
│   ├── schemas/state_models.py # AgentState (19 campos), ClientData, FinalReport
│   ├── mocks/product_catalog.json  # 18 produtos financeiros categorizados
│   └── mocks/mock_clients.json    # Perfis de demonstração para o ClientSelector
│
├── .env                        # Credenciais Azure OpenAI (NÃO versionado)
└── requirements.txt            # Dependências Python
```

---

## ⚙️ Pipeline de Execução (9 Agentes)

```
Payload  ──►  DataOrganizer  ──►  ContextAnalyzer
                   │ [400?]→END       │ [AML?]→END+Blacklist
                   ▼                  ▼
              Demographics ────────► HealthCheck
                   │ [menor?]→END          │ [CRITICO?]→END
                   ▼                       ▼
              EmotionalAnalyzer ─────── ProfileAnalyzer
                                              │ risk_score + Top 5 produtos
                                              ▼
                                        MathSpecialist
                                              │ projeção + alocação 31% cap
                                              ▼
                                        ReportWriter
                                              │ Markdown personalizado
                                              ▼
                                        ComplianceChecker ──► SSE result:success
```

### Escala de Risco

| Range | Perfil | Estratégia |
|---|---|---|
| 0.000 – 0.050 | **Conservador** | Preservação e liquidez |
| 0.051 – 0.290 | **Moderado** | Equilíbrio crescimento/proteção |
| 0.300 – 1.000 | **Arrojado** | Multiplicação de capital |

---

## 🚀 Como Executar

### Pré-requisitos

Configure o `.env` na raiz do projeto:

```env
AZURE_OPENAI_KEY=sua-chave-aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_MODEL=gpt-4o
AZURE_OPENAI_VERSION=2024-02-15-preview
```

### Backend (Terminal 1)

```bash
# Na raiz do projeto
export PYTHONPATH=$(pwd)
.\.venv\Scripts\Activate.ps1      # Windows PowerShell
python backend/main.py
# API disponível em: http://localhost:8000
```

### Frontend (Terminal 2)

```bash
cd frontend
npm install
npm run dev
# Interface disponível em: http://localhost:5173
```

---

## 🔒 Segurança em Camadas

| Camada | Onde | Mecanismo |
|---|---|---|
| 1 — Sanitização | DataOrganizer | `_sanitize_str/float/int/bool` + validação de campos |
| 2 — AML | ContextAnalyzer | 45 keywords + 12 regex de prompt injection |
| 3 — Blacklist | ContextAnalyzer + blacklist_manager | TXT + JSON persistente, lookup normalizado |
| 4 — Elegibilidade | DemographicAuditor | Menores de 16 bloqueados |
| 5 — Saúde Financeira | FinancialHealthAgent | LLM CFP + hard block (aporte > renda) |
| 6 — Compliance | ComplianceChecker | LLM revisa relatório + regex para leaks internos |

---

## 📦 Dependências Principais

### Backend
```
fastapi, uvicorn, langgraph, langchain, langchain-openai
pydantic, python-dotenv
```

### Frontend
```
react, vite, recharts, react-markdown, lucide-react
```
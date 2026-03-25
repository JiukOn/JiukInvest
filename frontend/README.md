# JiukInvest Frontend — Interface de Gestão de Wealth Management

> **Painel de Análise Estratégica assistido por IA** — Visualização em tempo real do pipeline multi-agente, relatórios personalizados e gráficos de evolução patrimonial.

Interface desenvolvida com **React + Vite**, projetada para gerentes de wealth management que precisam gerar estratégias de investimento hiperpersonalizadas para clientes. O sistema se conecta ao backend LangGraph via **Server-Sent Events (SSE)**, exibindo a execução de cada agente em tempo real.

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Uso |
|---|---|---|
| React | 18+ | Base da aplicação — componentes e hooks |
| Vite | 5+ | Build tool e servidor de desenvolvimento |
| Recharts | 2+ | Gráficos de alocação (pizza) e evolução patrimonial (área composta) |
| Lucide React | latest | Ícones vetoriais leves e consistentes |
| ReactMarkdown | latest | Renderização do relatório gerado pelo LLM em Markdown |
| CSS Puro | — | Glassmorphism 2.0 — Outfit font + design system de tokens |

> **Nota:** A comunicação com o backend usa `fetch` nativo com SSE (`ReadableStream`). Não há Axios neste projeto.

---

## 📂 Estrutura de Diretórios (`/src`)

```
src/
├── App.jsx                     # Componente raiz — layout grid: Input | Output
├── App.css                     # Grid, empty-state, dashboard-actions, PDF button
├── index.css                   # Design system global: tokens, glassmorphism, animações
├── main.jsx                    # Entrypoint React + StrictMode
│
├── components/
│   ├── Header.jsx              # Barra superior: logo animado, badge AI Online, perfil
│   ├── Header.css
│   ├── NewClientForm.jsx       # Formulário de captação do perfil do cliente
│   ├── NewClientForm.css       # Slider gradiente, chips de ativos, radio pills
│   ├── ReportDisplay.jsx       # Renderizador Markdown → HTML estilizado
│   ├── ReportDisplay.css       # Tabelas, blockquotes, h2/h3/h4, hover em linhas
│   ├── ClientSelector.jsx      # Seleção rápida de perfis mockados (carrega o form)
│   ├── StatusTimeline.jsx      # Pipeline visual de 9 agentes com conectores e animação
│   └── StatusTimeline.css
│
├── components/charts/
│   ├── AllocationPieChart.jsx  # Gráfico de rosca — distribuição de portfólio
│   └── EvolutionBarChart.jsx   # ComposedChart — JiukInvest vs Poupança vs Ibovespa
│
├── hooks/
│   └── useLangGraph.js         # Hook SSE — consome o stream do backend agente por agente
│
├── services/
│   └── api.js                  # fetchMockProfiles() + generateReport() (fetch nativo)
│
└── utils/
    └── exportPdf.js            # Print CSS — exporta o #pdf-report-area para PDF
```

---

## 🔄 Fluxo de Dados

```
[NewClientForm]
    │  onSubmit(formData)
    ▼
[useLangGraph.executeGraph()]
    │  POST /api/copilot/generate  →  StreamingResponse (SSE)
    │
    ├─ type: 'log' (agent: 'DataOrganizer')  →  setCurrentStepIndex(0)
    ├─ type: 'log' (agent: 'ContextAnalyzer')  →  setCurrentStepIndex(1)
    ├─ type: 'log' (agent: 'MathSpecialist')   →  setCurrentStepIndex(6)
    ├─ type: 'math_log'  →  [trace interno de cálculos]
    │
    └─ type: 'result'
           ├─ status: 'success'  →  setReportData(report + charts)
           ├─ status: 'blocked'  →  relatório de bloqueio AML
           ├─ status: 'restricted'  →  relatório de não-elegibilidade
           ├─ status: 'health_critical'  →  relatório de saúde crítica
           └─ status: 'validation_error'  →  relatório de dados inválidos
    │
    ▼
[App.jsx]
    ├─ [StatusTimeline] — atualiza step em tempo real
    ├─ [ReportDisplay] — renderiza markdown do relatório
    ├─ [AllocationPieChart] — gráfico de alocação de ativos
    └─ [EvolutionBarChart] — projeção patrimonial com benchmarks
```

---

## 🧩 Componentes Principais

### `NewClientForm.jsx`
Formulário de 3 seções:
1. **Dados Pessoais** — nome, idade, nível de conhecimento, experiência prévia
2. **Capacidade Financeira** — renda, patrimônio, aporte mensal, horizonte (slider gradiente)
3. **Preferências de Alocação** (visível para Intermediário/Avançado) — checkboxes por categoria + chips de ativos específicos

Comportamento: formulário começa **vazio** (sem mock). Ao selecionar um perfil via `ClientSelector`, os campos são preenchidos automaticamente.

### `StatusTimeline.jsx`
Exibe os **9 agentes** do pipeline em ordem com:
- Ícone único por agente
- Linha de conector animada (verde ao completar)
- Estado ativo com brilho violeta e pontos pulsantes
- Labels em português

### `useLangGraph.js`
Hook SSE com `SSE_STEP_MAP` que mapeia o nome do agente (campo `agent` do evento `log`) para o índice correto no `StatusTimeline`. Elimina a necessidade de timers artificiais — o progresso é **real e sincronizado** com o backend.

### `EvolutionBarChart.jsx`
`ComposedChart` com 3 séries de dados com áreas gradiente:
- 🟣 **JiukInvest** — projeção com taxa ponderada dos ativos selecionados
- 🔵 **Poupança** — benchmark de referência (0.5%/mês)
- 🟢 **Ibovespa** — benchmark histórico médio (1.0%/mês)

---

## 🎨 Design System

O sistema usa **Glassmorphism 2.0** com tokens CSS centralizados no `index.css`:

| Token | Valor | Uso |
|---|---|---|
| `--font-display` | `Outfit` | Headings, labels, botões |
| `--font-body` | `Inter` | Textos corridos, inputs |
| `--accent-primary` | `#8b5cf6` | Violeta — cor de ação principal |
| `--bg-base` | `#08080a` | Fundo da aplicação |
| `--glass-bg` | `rgba(18,18,20,0.7)` | Painéis glassmorphism |
| `--shadow-glow` | `0 0 24px var(--accent-glow)` | Glow em hover e estados ativos |

---

## 🚀 Como Executar

**Pré-requisito:** Node.js 18+ e o backend rodando em `localhost:8000`.

```bash
# Na pasta /frontend
npm install
npm run dev
# Disponível em: http://localhost:5173
```

---

## 📄 Exportação de PDF

O botão **Exportar PDF** aciona `exportToPdf()`, que usa `window.print()` com estilos CSS de impressão definidos no `index.css`:
- Oculta todos os elementos exceto `#pdf-report-area`
- Exibe o cabeçalho JiukInvest (`print-only-header`) com logo e data
- Formatação A4 compatível com todos os navegadores modernos
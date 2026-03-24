# GenAI Investment Copilot - Enterprise Architecture

Este repositório contém a solução completa para o Case GenAI para Investimentos. Projetado sob os pilares da escalabilidade corporativa, governança de dados e hiperpersonalização, o sistema atua como um orquestrador inteligente para gerentes bancários, transformando dados brutos em estratégias financeiras auditáveis e visualmente ricas.

## 🎯 Visão Estratégica e Planejamento

O desafio central na adoção de IA Generativa no setor financeiro é o equilíbrio entre personalização em massa e compliance estrito. Modelos fundacionais tendem a alucinar cálculos e assumir garantias indevidas. O planejamento desta arquitetura mitiga esses riscos através dos seguintes pilares:

1. **Workflow Agêntico (LangGraph):** Transição de um modelo de prompt único para uma máquina de estados finitos, onde múltiplos agentes especializados operam em sequência.
2. **Auditoria Contínua (LLM-as-a-Judge):** Implementação de um agente exclusivo que atua como *guardrail* final. Ele avalia criticamente o relatório e força ciclos de refação caso detecte promessas de rentabilidade ou tom inadequado.
3. **Determinismo Matemático:** Bloqueio da capacidade do LLM de realizar inferências matemáticas. O modelo aciona ferramentas (*Tools*) determinísticas codificadas em Python para calcular juros e projeções, garantindo exatidão.
4. **Desacoplamento de Domínios:** Separação absoluta entre a camada de apresentação (React), o motor lógico e de orquestração (FastAPI) e os contratos de dados (Pydantic).

## 🏗️ Topologia do Sistema

A arquitetura do projeto está fragmentada em três grandes domínios operacionais:

* **`/frontend` (Client-Side & UI):** Aplicação React via Vite. Responsável pela captação de parâmetros, escuta ativa dos *HTTP Status Codes* para observabilidade do ciclo dos agentes, renderização dos dados em formato Markdown e geração de gráficos iterativos através da biblioteca Recharts. Inclui rotinas para exportação direta do DOM para documentos PDF.
* **`/backend` (Server-Side & Orquestração):** API assíncrona baseada em FastAPI que encapsula o motor do LangGraph. Gerencia a tipagem de entrada e saída, expõe o pipeline HTTP e coordena o ciclo de vida dos quatro nós autônomos: Organizador, Analisador, Redator e Verificador de Compliance.
* **`/data` (Contratos e Mockups):** Módulo de padronização que abriga os esquemas Pydantic (`state_models.py`), ditando o formato exato da memória transitória dos agentes, além de prover as bases JSON estáticas que simulam o catálogo de produtos e perfis de clientes do banco.

## 🚀 Guia de Inicialização do Ambiente

Para habilitar o ecossistema completo localmente, os serviços de back-end e front-end devem ser iniciados simultaneamente.

**Pré-requisitos de Infraestrutura:**
* Node.js v18 ou superior
* Python 3.10 ou superior
* Criação de um arquivo `.env` na raiz do repositório contendo a credencial de acesso: `OPENAI_API_KEY=sua-chave-aqui`

### 1. Levantando a Infraestrutura de IA (Backend)

Abra um terminal na raiz do projeto e execute os comandos de ativação do ambiente e inicialização do servidor ASGI:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend
uvicorn main:app --reload --port 8000
```

A API estará operacional recebendo conexões em http://localhost:8000.

### 2. Levantando a Aplicação Client-Side (Frontend)

Em um segundo terminal, a partir da raiz do projeto, instale as dependências e inicie o servidor de desenvolvimento:

```bash
cd frontend
npm install
npm run dev
```

A interface do usuário ficará disponível no endereço padrão do Vite (http://localhost:5173), pronta para consumir os endpoints do orquestrador.
# Backend - GenAI Investment Copilot (Motor de Orquestração)

Este módulo atua como o núcleo de inteligência e governança do Case GenAI para Investimentos. Desenvolvido em **Python** com **FastAPI** e **LangGraph**, o sistema não é um mero conduíte para chamadas de API de LLMs, mas um pipeline de orquestração agêntica (*Stateful Agentic Workflow*) focado em segurança, precisão matemática e compliance bancário.

## 🛠️ Stack Tecnológica e Fundamentos

* **Python (v3.10+):** Base da aplicação e processamento de dados.
* **FastAPI & Uvicorn:** Framework ASGI assíncrono para exposição de endpoints RESTful de alta performance.
* **LangGraph:** Motor de orquestração baseado em grafos (DAGs cíclicos) para gestão de estado e fluxo de execução entre os agentes.
* **LangChain / OpenAI SDK:** Interface de comunicação e chamadas estruturadas (*Tool Calling*) com os modelos fundacionais.
* **Pydantic:** Tipagem estrita, validação e serialização do `AgentState` e dos payloads de entrada/saída.

## 📂 Padrão Arquitetural (`/backend`)

A estrutura do projeto aplica o princípio de Inversão de Controle e Separação de Conceitos (SoC), garantindo que a lógica de negócios, a engenharia de prompt e a exposição HTTP estejam totalmente desacopladas:

* **`main.py`**: Entrypoint da aplicação, inicialização do servidor ASGI e injeção de middlewares (CORS).
* **`api/routes.py`**: Controladores de rotas REST (ex: `POST /api/generate-report`). Atua como adaptador entre o cliente HTTP e o orquestrador interno.
* **`graph_orchestrator.py`**: O motor de transição de estados. Define os `Nodes` (agentes/funções) e as `Conditional Edges` (rotas lógicas de aprovação, reprovação e loop de refação).
* **`agents/`**: Atores independentes do sistema:
  * `data_organizer.py`: Middleware de normalização de input.
  * `profile_analyzer.py`: Avaliador de risco e integrador de contexto.
  * `report_writer.py`: Agente de síntese e redação de markdown/JSON estruturado.
  * `compliance_checker.py`: Implementação do padrão *LLM-as-a-Judge* para auditoria rigorosa de viés e promessas de rentabilidade.
* **`tools/`**: Módulos determinísticos acopláveis aos agentes:
  * `investment_api_mock.py`: Adaptador simulado para o banco de dados de produtos financeiros.
  * `financial_calculator.py`: Motor matemático isolado para evitar alucinações algorítmicas do LLM.
* **`prompts/system_prompts.py`**: Repositório central de engenharia de prompt, mantendo as diretrizes de comportamento isoladas da lógica do código.

## 🔄 Máquina de Estados (Lifecycle do LangGraph)

O payload trafega através de um estado global tipado (`AgentState`), sofrendo mutações sequenciais e condicionais:
1. `__start__` ➔ `DataOrganizer`
2. `DataOrganizer` ➔ `ProfileAnalyzer`
3. `ProfileAnalyzer` ➔ `ReportWriter`
4. `ReportWriter` ➔ `ComplianceChecker`
5. `ComplianceChecker` ➔ Avaliação:
   * **[Pass]** ➔ `__end__` (Payload finalizado retornado via API).
   * **[Fail]** ➔ Loop de retorno para `ReportWriter` injetando o log de erro para auto-correção.

## 🚀 Deployment Local

Certifique-se de configurar a variável `OPENAI_API_KEY` no arquivo `.env` na raiz do projeto antes da inicialização.

```bash
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000
```
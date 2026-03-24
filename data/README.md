# Data Layer - GenAI Investment Copilot

Este módulo centraliza a definição de contratos de dados e armazena os artefatos estáticos que simulam a infraestrutura de banco de dados do Banco XYZ. Sua função principal é garantir consistência estrutural, tipagem estrita e o isolamento da camada de dados em relação à lógica de orquestração (LangGraph) e à interface de usuário (React).

## 📂 Arquitetura de Diretórios (`/data`)

O diretório está segmentado em dois domínios operacionais: os registros estáticos (Mocks) e os validadores de tempo de execução (Schemas).

### 1. `/mocks` (Simulação de Infraestrutura)
Armazena os artefatos JSON que emulam os repositórios da instituição financeira.
* `mock_clients.json`: Base de perfis pré-cadastrados (Conservador, Moderado, Arrojado) projetada para testes de carga e demonstração de fluxo rápido (*Happy Path*).
* `product_catalog.json`: Catálogo oficial de ativos do banco. Este arquivo é injetado nas ferramentas determinísticas do back-end para realizar o *matching* de portfólio. Ele atua como uma trava de segurança (*grounding*) fundamental, impossibilitando o LLM de alucinar ou recomendar produtos fictícios.

### 2. `/schemas` (Contratos de Tipagem)
Abriga as validações de dados construídas sobre o Pydantic e estruturas nativas do Python.
* `state_models.py`: Define o `AgentState`, a espinha dorsal do projeto. Este arquivo modela exatamente quais chaves e tipos de dados viajam pelos nós do LangGraph. Ele dita a assinatura obrigatória do input do usuário e trava a estrutura de saída do agente redator (forçando a entrega de arrays específicos para a renderização dos gráficos no front-end).

## 🛡️ Princípios de Engenharia e Governança

* **Single Source of Truth (SSoT):** Qualquer mutação no contrato de dados exigida pelo front-end ou produzida pelo back-end deve ser originada e registrada nos schemas desta pasta.
* **Validação Estrita:** A utilização do Pydantic assegura que falhas de estruturação do LLM (ex: chaves JSON ausentes ou tipos incorretos) gerem exceções tratáveis antes que uma resposta malformada atinja o front-end.
* **Desacoplamento Orientado a Produção:** A separação física dos *mocks* garante que, em uma esteira de produção real, a transição de arquivos JSON locais para conexões em bancos de dados (SQL/NoSQL) ocorra sem refatoração da lógica de negócios central.
# Roteiro da Apresentação - Investment Copilot

## 1. Introdução e Contexto do Projeto
- **O que foi feito:** Desenvolvimento da interface (Frontend) do JiukInvest.
- **Objetivo:** Criar uma experiência de usuário fluida para visualização de relatórios de investimentos, histórico de clientes e dashboards analíticos.

## 2. Preparação de Dados (Mock Backend)
- **Desafio:** Era necessário ter dados consistentes e realistas para testar a interface antes da API oficial estar pronta.
- **Solução (Python e Pandas):** 
  - Criação de scripts temporários em Python utilizando a biblioteca **Pandas**.
  - Leitura dos dados originais a partir de planilhas Excel e conversão/tradução para uma base mockada de 8 clientes em formato **JSON** (`mock_clients.json`).
- **Pulo do Gato (Padronização):** Durante essa extração, as nomenclaturas das *tags* (chaves do JSON) foram todas padronizadas e organizadas em ordem lógica. Isso foi planejado para **facilitar imensamente a futura conexão e estruturação de acesso** quando o backend real for integrado.

## 3. Estrutura e Funcionalidades do Frontend
O projeto foi totalmente baseado em **React + Vite** (para alta performance). As principais features construídas foram:
- **ClientSelector:** Um seletor para trocar rapidamente os dados visualizados entre os 8 clientes.
- **NewClientForm:** Formulário completo e estruturado para cadastro ou edição de dados dos clientes.
- **StatusTimeline:** Uma linha do tempo visual que demonstra o andamento/ações de cada conta.
- **ReportDisplay:** Área dedicada à leitura dos relatórios (copilot) gerados sobre a carteira.
- **Gráficos:** Visualizações modulares dos dados do cliente.

## 4. Principais Bibliotecas Utilizadas
É importante destacar as ferramentas que viabilizaram as features acima:
- **Lucide-React:** Biblioteca escolhida para a iconografia do projeto. Fornece ícones modernos, leves e padronizados em todo o Frontend.
- **React-Markdown:** Utilizada no `ReportDisplay` para transformar os textos e análises geradas (que chegam em formato markdown) em texto formatado, rico e de fácil leitura para o usuário final.
- **Recharts:** Biblioteca empregada na construção dos gráficos do dashboard, permitindo que a visualização dos dados seja interativa e responsiva.
- **Pandas (Python):** Usado nos bastidores (scripts temporários) para tratamento e limpeza da base de dados Excel original para JSON.

## 5. Status Atual e Próximos Passos
- O código do Frontend foi refatorado e limpo (política de zero comentários/lixo de código).
- Com a interface homologada com os dados do mock json super estruturados, o projeto está **100% preparado para a integração com as APIs do Backend e o modelo de IA**.

## 6. Evolução de UI/UX e Motor Lógico "JiukInvest"
- Refatoração do esquema Pydantic (`ClientData`), delegando a decisão de Risco e Liquidez exclusivamente para o modelo de IA (baseado nos inputs empíricos do usuário).
- Criação de um formulário de "Perguntas de Nivelamento" condicional avançado:
  - Integração de `Sliders` para tempo de horizonte (de 6 meses a 35 anos).
  - Seleção dinâmica e encadeada de tipos de ativos disponíveis baseados no conhecimento do cliente (Ativos Nacionais vs Internacionais, Públicos vs Privados).
  - Áreas narrativas textuais (campo de comentários, sonhos, objetivos) para propiciar contexto analítico profundo à IA LLM.
- Reformulação de toda a UI para adotar uma Identidade Visual Violeta/Roxa (*Purple Glassmorphism* premium).
- Internacionalização defensiva da base do HTML (`pt-BR`) eliminando erros críticos causados por tradutores automáticos como o Brave/Chrome Translate.
- Expansão de um catálogo de investimentos diversificado (`product_catalog.json`) com pontuações de risco numéricas (`risk_score`) absolutas variando de `0.0` a `1.0`.
- Alteração formal e sistêmica da marca global do projeto para **JiukInvest**.

## 7. Mapeamento da Rubrica de Avaliação (Reverse Engineering)
- **Extração Analítica:** Utilizei um script automatizado (`python-pptx`) para decifrar a apresentação original do desafio (`CasePresentation.pptx`), extraindo as métricas exatas de pontuação exigidas pela banca.
- **Direcionamento Estratégico:** Todo o fluxo do projeto foi repensado com o objetivo explícito de atingir o **Nível 4 (Especialista/Excelente)**, focando 100% nas rubricas de "Personalização", "Qualidade GenAI" e "Diferenciais Comerciais", como os Logs de Auditoria e Guardrails.

## 8. Arquitetura Multi-Agentes (O Cérebro do Backend)
A fase mais complexa do projeto englobou a construção de uma **Topologia Multi-Agentes com LangGraph e FastAPI**, garantindo as exigências de compliance financeiro corporativo:
- **Separação de Preocupações (Tools Determinísticas):**
  - Implementação de ferramentas puramente matemáticas em Python (soma, subtração, cálculo exato de juros compostos em `financial_calculator.py`) para **erradicar a chance de alucinação matemática do LLM**.
- **Filtros de Barragem (Guardrails Inteligentes):**
  - **AML (Anti-Money Laundering):** Um agente especializado rastreia o texto em busca de indícios de crime ou fraude. Acionado, ele bloqueia o usuário e grava num registro em `blacklist.txt`.
  - **Auditor Demográfico:** Regras ativas que restringem ou alteram recomendações para menores de 16 ou 13 anos (foco social / educação em vez de aportes).
  - **Saúde Financeira:** Avisos críticos se o cliente planejar aportar mais de 70% do próprio salário, agindo como um consultor responsável que prioriza a "Reserva de Emergência".
- **Motor LangGraph e Integração LLM:**
  - `profile_analyzer.py` e `report_writer.py` foram integrados de forma nativa com a **OpenAI via LangChain**, tudo devidamente amarrado ao grafo `graph_orchestrator.py`.
- **Camada de Resiliência Inquebrável (Fallback Seguro):** 
  - O sistema foi intencionalmente programado para **nunca quebrar a aplicação**. Se o avaliador não inserir a `OPENAI_API_KEY` ao arquivo `.env`, ou se a API OpenAI ficar fora do ar, o sistema silenciosamente desvia o tráfego para os scripts condicionais determinísticos e emite o relatório perfeito de toda forma, provando maturidade em engenharia de software contínua.

## 9. Integração Full-Stack e Entrega Final
- **Comunicação Assíncrona:** O Frontend React foi totalmente conectado à Rota FastAPI (`/api/copilot/generate`), trocando JSONs validados em tempo real usando Fetch nativo.
- **Exportação de PDF Inteligente:** Atendendo aos diferenciais recomendados (Exportação de relatórios), a aplicação ganhou um botão nativo para baixar o relatório final utilizando uma manobra de estabilidade visual com CSS Print (`@media print`), gerando o documento limpo, direto e sem poluição de telas para o cliente.

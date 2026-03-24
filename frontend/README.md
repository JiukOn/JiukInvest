# Frontend - GenAI Investment Copilot

Módulo de interface de usuário (UI) do Case GenAI para Investimentos da NTT DATA. Desenvolvido com **React** e **Vite**, atua como o painel principal para a simulação e geração de relatórios de investimentos hiperpersonalizados, focado na experiência do gerente bancário e na observabilidade do sistema.

## 🛠️ Tecnologias Utilizadas

* **React (v18+) & Vite:** Base da aplicação para renderização otimizada e gestão de ciclo de vida de componentes.
* **Axios:** Cliente HTTP para comunicação RESTful assíncrona com o orquestrador LangGraph no back-end (FastAPI).
* **Recharts:** Biblioteca de visualização de dados para renderização nativa de gráficos de alocação de carteira e evolução patrimonial.
* **Lucide-react:** Pacote de iconografia vetorial limpa, leve e responsiva.
* **React Router DOM:** Gestão de rotas client-side (navegação fluida entre seleção de perfil e dashboard de relatórios).

## 📂 Arquitetura de Diretórios (`/src`)

A estrutura segue os princípios de modularidade e Separação de Conceitos (SoC), isolando a camada visual da lógica de integração:

* **`assets/`**: Arquivos estáticos, identidades visuais do Banco XYZ e tipografia corporativa.
* **`components/`**: Componentes modulares e reutilizáveis da interface.
  * `ClientSelector.jsx`: Ponto de entrada rápido utilizando perfis mockados (Conservador, Moderado, Arrojado).
  * `NewClientForm.jsx`: Formulário de captação de parâmetros para simulação de novos clientes dinâmicos.
  * `ReportDisplay.jsx`: Renderizador principal responsável por transformar o conteúdo estruturado da IA em uma interface de leitura amigável.
  * `StatusTimeline.jsx`: Componente de observabilidade que interpreta os *HTTP Status Codes* e exibe o progresso dos agentes do LangGraph em tempo real.
* **`components/charts/`**: Encapsulamento dos módulos do Recharts.
  * `AllocationPieChart.jsx`: Gráfico de rosca detalhando a distribuição de ativos.
  * `EvolutionBarChart.jsx`: Gráfico de barras projetando rendimentos futuros baseados nas ferramentas matemáticas do back-end.
* **`hooks/`**: Custom hooks para isolamento de regras de negócio do React.
  * `useLangGraph.js`: Gerencia a mutação de dados, estados de *loading* e tratamento de exceções do orquestrador.
* **`services/`**: Camada de integração com a infraestrutura.
  * `api.js`: Instância do Axios pré-configurada com `baseURL` e *interceptors* para a rota `/api/gerar-relatorio`.
* **`utils/`**: Funções utilitárias puras.
  * `exportPdf.js`: Lógica de *client-side* para capturar a árvore do DOM do relatório, aplicar estilos de impressão e gerar o documento A4 para download seguro.

## 🚀 Como Executar Localmente

**Pré-requisito:** Node.js (v18 ou superior) instalado. Para o fluxo completo de geração, garanta que o servidor back-end (FastAPI) esteja rodando na porta `8000`.

1. Instale as dependências locais:
```bash
npm install
```

2. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

3. Acesse a aplicação em: http://localhost:5173
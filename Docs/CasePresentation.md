# Guia de Avaliação e Escopo - Case GenAI (Banco XYZ)

Este documento foi extraído e sintetizado a partir da apresentação original (`CasePresentation.pptx`). Ele serve como o nosso "Norte" para garantir nota máxima (Faixa 4 - Excelente) na avaliação da NTT DATA.

## 1. O Desafio Central
O Banco XYZ deseja automatizar relatórios e comunicações de investimentos usando GenAI, garantindo que o texto reflita o **perfil de risco**, os **objetivos financeiros** e a **carteira** do cliente, evitando respostas genéricas ("alucinações" ou textos sem *grounding*).

## 2. Escopo Mínimo Obrigatório (O que FAZ o projeto ser aceito)
- [x] **Front-end** para selecionar um cliente e acionar a geração.
- [ ] Uso de um **LLM** para produzir o texto final.
- [ ] Uso dos **dados empíricos do cliente** como contexto garantido (Grounding).
- [ ] Exibição do conteúdo gerado em tela.

## 3. Diferenciais Opcionais (O que GARANTE a Nota Máxima)
A apresentação cita explicitamente várias "Boas Práticas" e "Extras" que elevam a nota para a Faixa 4 (Excelente). Nosso objetivo é incluí-los na arquitetura JiukInvest:
- **Trilha de Auditoria:** Logs claros do que a IA fez (já planejado no `AgentState`).
- **Guardrails e Compliance:** Validações para garantir que a IA não faça promessas irreais de retorno (já planejado via `compliance_checker`).
- **Exportação em PDF:** Permitir baixar o relatório final gerado.
- **Múltiplas Versões:** Opção de ter um relatório resumido e um detalhado (Expansão).
- **Gráficos Visuais:** Já implementados na Fase 1 (Recharts).
- **Comparativo de Perfis:** Demonstração clara da diferença entre recomendações para Conservadores vs Arrojados.

## 4. Critérios e Pesos de Avaliação
- **Funcionalidade (25%):** O fluxo ponta a ponta funciona bem?
- **Personalização (20%):** O texto realmente muda conforme o cliente?
- **Qualidade GenAI (20%):** A recomendação é plausível, bem escrita e usa *grounding*?
- **User Experience - UX (15%):** A interface é agradável e fácil de usar?
- **Robustez (10%):** Tem tratamentos de erros ou *guardrails*?
- **Diferenciais (10%):** Gráficos, PDF, Logs, etc.

## 5. Níveis de Entrega GenAI
Queremos atingir o **Nível 4 (Especialista)**, que exige validações de perfil, compliance, explicabilidade (audit logs) e exportação final.

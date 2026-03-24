import React from 'react';
import ReactMarkdown from 'react-markdown';
import { FileText } from 'lucide-react';
import './ReportDisplay.css';

const mockMarkdown = `
### Análise de Portfólio & Recomendação Estratégica

Com base no perfil apresentado—**35 anos**, um apetite **Moderado para risco** (avaliado pela nossa IA), e um **horizonte de investimento de 10 anos**—a estratégia a seguir prioriza o crescimento sustentável enquanto mitiga a volatilidade excessiva. 

A capacidade de aporte mensal de **R$ 3.000,00** combinada a um capital inicial de **R$ 100.000,00** cria uma forte base de juros compostos.

#### Estratégia Principal & Alocação de Ativos
1. **Renda Fixa (70%)**: Alocação pesada em CDBs Pós-fixados (110% CDI) para garantir rendimento real acima da inflação, e posições secundárias em Tesouro IPCA+ para travar o poder de compra ao longo da década.
2. **Renda Variável (30%)**: Uma mistura selecionada de Ações Brasileiras amplas (BOVA11) e Fundos Imobiliários (FIIs) para fornecer dividendos mensais e potencial de valorização de capital. Como ativos internacionais não foram priorizados nas preferências, o foco é 100% no mercado doméstico.

> **Nota do Especialista IA:** A preferência de liquidez de médio prazo é perfeitamente respeitada aqui. Os CDBs oferecem liquidez diária, e os FIIs garantem renda mensal, enquanto a porção de ações está focada no longo curso.

#### Próximos Passos
- Abrir as contas recomendadas.
- Configurar transferências mensais automáticas para os aportes de R$ 3.000.
- Revisar o rebalanceamento do portfólio anualmente com este Copiloto.
`;

const ReportDisplay = ({ markdown = mockMarkdown }) => {
  return (
    <div className="report-container glass-panel">
      <div className="report-header">
        <FileText size={20} className="report-icon" />
        <h2>Relatório Estratégico da IA</h2>
      </div>
      <div className="report-content">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
};

export default ReportDisplay;

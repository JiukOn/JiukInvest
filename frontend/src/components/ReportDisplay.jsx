import React from 'react';
import ReactMarkdown from 'react-markdown';
import { FileText, AlertTriangle, User, TrendingUp, Calendar, Wallet } from 'lucide-react';
import './ReportDisplay.css';

const ReportDisplay = ({ markdown, formData }) => {
  if (!markdown) {
    return (
      <div className="report-container glass-panel fallback-state">
        <div className="report-header error-header">
          <AlertTriangle size={24} className="error-icon" />
          <h2>Aviso: Erro na Conexão com a IA</h2>
        </div>
        
        <div className="error-body">
          <p className="error-msg">
            Não foi possível receber a análise estratégica em tempo real. 
            Abaixo estão os dados capturados que seriam processados:
          </p>

          {formData && (
            <div className="captured-data-grid">
              <div className="data-item">
                <User size={16} />
                <span><strong>Cliente:</strong> {formData.name} ({formData.age} anos)</span>
              </div>
              <div className="data-item">
                <TrendingUp size={16} />
                <span><strong>Conhecimento:</strong> {formData.knowledge_level}</span>
              </div>
              <div className="data-item">
                <Calendar size={16} />
                <span><strong>Horizonte:</strong> {formData.investment_horizon_months} meses</span>
              </div>
              <div className="data-item">
                <Wallet size={16} />
                <span><strong>Inicial:</strong> R$ {formData.initial_investment?.toLocaleString('pt-BR')}</span>
              </div>
            </div>
          )}

          <div className="error-instructions">
            <p><strong>Status do Servidor:</strong> <span className="error-code">CONNECTION_TIMEOUT / NO_RESPONSE</span></p>
            <p>Por favor, verifique se o backend (Terminal 1) está rodando e se não há bloqueios de rede/CORS.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="report-container glass-panel fade-in">
      <div className="print-only-header" style={{ display: 'none', marginBottom: '20px', borderBottom: '2px solid #9d4edd', paddingBottom: '10px' }}>
         <h1 style={{ color: '#9d4edd', margin: 0, fontSize: '24px' }}>JiukInvest</h1>
         <p style={{ color: '#444', margin: 0, fontSize: '12px', fontWeight: 'bold' }}>Relatório Oficial de Análise Digital via GenAI - Nível Especialista</p>
         <p style={{ color: '#666', margin: 0, fontSize: '10px' }}>Documento Emitido Eletronicamente via Múltiplos Agentes Autônomos</p>
      </div>
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

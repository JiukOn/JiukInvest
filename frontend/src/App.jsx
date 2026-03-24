import React from 'react';
import Header from './components/Header';
import NewClientForm from './components/NewClientForm';
import ReportDisplay from './components/ReportDisplay';
import AllocationPieChart from './components/charts/AllocationPieChart';
import EvolutionBarChart from './components/charts/EvolutionBarChart';
import ClientSelector from './components/ClientSelector';
import StatusTimeline from './components/StatusTimeline';
import './App.css';

import { generateReport } from './services/api';
import { exportToPdf } from './utils/exportPdf';

function App() {
  const [isGenerating, setIsGenerating] = React.useState(false);
  const [showResults, setShowResults] = React.useState(false);
  const [currentStepIndex, setCurrentStepIndex] = React.useState(0);
  const [formData, setFormData] = React.useState(null);
  const [reportData, setReportData] = React.useState(null);

  const handleGenerateStrategy = async (data) => {
    console.log('Form data submitted:', data);
    setFormData(data);
    setIsGenerating(true);
    setShowResults(false);
    setCurrentStepIndex(0);
    setReportData(null);
    
    const interval = setInterval(() => {
      setCurrentStepIndex(prev => {
        if(prev >= 4) { return prev; }
        return prev + 1;
      });
    }, 1500);

    try {
      const result = await generateReport(data);
      clearInterval(interval);
      setCurrentStepIndex(5);
      
      if (result.status === "error" || result.status === "restricted") {
        setReportData({
           markdown_text: `## AVISO DO SISTEMA\n\n**Status:** ${result.status.toUpperCase()}\n\n**Mensagem Oficial:** ${result.message}\n\n**Motivo:** ${result.reason || "Regra local restritiva."}`,
           charts: { allocation_pie: [], evolution_bar: [] }
        });
      } else {
        setReportData(result.report);
      }
      
      setShowResults(true);
    } catch (error) {
      clearInterval(interval);
      setReportData({
         markdown_text: `## Erro de Comunicação\n\nFalha ao interagir com o LangGraph.\n\nDetalhes: ${error.message}`,
         charts: { allocation_pie: [], evolution_bar: [] }
      });
      setShowResults(true);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      
      <main className="container main-grid">
        <section className="input-section glass-panel">
          <div className="section-header">
            <h2>Perfil do Cliente</h2>
            <p>Preencha os dados do cliente para iniciar a análise</p>
          </div>
          
          <ClientSelector onSelect={(data) => setFormData(data)} />
          
          <div className="placeholder-content" style={{ padding: 0, border: 'none', background: 'transparent' }}>
            <NewClientForm 
              onSubmit={handleGenerateStrategy} 
              isGenerating={isGenerating} 
              initialData={formData}
            />
          </div>

          {isGenerating && <StatusTimeline currentStepIndex={currentStepIndex} />}
        </section>

        <section className="output-section">
          {!showResults ? (
            <div className="glass-panel output-card initial-state">
              <div className="empty-state">
                <div className="pulse-circle"></div>
                <h3>Aguardando Dados</h3>
                <p>Preencha o perfil ao lado e envie para ver a análise e recomendação de portfólio da IA.</p>
              </div>
            </div>
          ) : (
            <div className="results-dashboard fade-in" id="pdf-report-area">
              <div className="dashboard-actions" style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '1rem' }}>
                 <button className="primary-button" onClick={exportToPdf} style={{ padding: '0.6rem 1.2rem', gap: '8px', display: 'flex', alignItems: 'center' }}>
                    Exportar Relatório PDF
                 </button>
              </div>
              <ReportDisplay markdown={reportData?.markdown_text} />
              <div className="charts-grid">
                <AllocationPieChart 
                  data={reportData?.charts?.allocation_pie?.length ? reportData.charts.allocation_pie : [
                    { name: 'Sem Dados de Alocação', value: 100 }
                  ]} 
                />
                <EvolutionBarChart 
                  data={reportData?.charts?.evolution_bar?.length ? reportData.charts.evolution_bar : [
                    { year: new Date().getFullYear(), value: 0 }
                  ]} 
                />
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;

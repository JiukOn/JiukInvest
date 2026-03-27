import React from 'react';
import Header from './components/Header';
import NewClientForm from './components/NewClientForm';
import ReportDisplay from './components/ReportDisplay';
import AllocationPieChart from './components/charts/AllocationPieChart';
import EvolutionBarChart from './components/charts/EvolutionBarChart';
import ClientSelector from './components/ClientSelector';
import StatusTimeline from './components/StatusTimeline';
import { Sparkles, Download } from 'lucide-react';
import './App.css';

import { exportToPdf } from './utils/exportPdf';
import { useLangGraph } from './hooks/useLangGraph';

function App() {
  const [formData, setFormData] = React.useState(null);
  const { isGenerating, showResults, currentStepIndex, reportData, executeGraph } = useLangGraph();

  const handleGenerateStrategy = (data) => {
    setFormData(data);
    executeGraph(data);
  };

  const hasPieData = reportData?.charts?.allocation_pie?.length > 0;
  const hasEvolutionData = reportData?.charts?.evolution_bar?.length > 0;

  return (
    <div className="app-container">
      <Header />

      <main className="container main-grid">
        <section className="input-section glass-panel">
          <div className="section-header">
            <h2>Perfil do Cliente</h2>
            <p>Dados financeiros e comportamentais para análise pela IA</p>
          </div>

          <ClientSelector onSelect={(data) => setFormData(data)} />

          <NewClientForm
            onSubmit={handleGenerateStrategy}
            isGenerating={isGenerating}
            initialData={formData}
          />

          {isGenerating && <StatusTimeline currentStepIndex={currentStepIndex} />}
        </section>

        <section className="output-section">
          {!showResults ? (
            <div className="glass-panel output-card initial-state">
              <div className="empty-state">
                <div className="pulse-circle" />
                <h3>Aguardando Análise</h3>
                <p>Preencha o perfil do cliente ao lado e execute a análise para receber o relatório estratégico personalizado da IA.</p>
              </div>
            </div>
          ) : (
            <div className="results-dashboard fade-in" id="pdf-report-area">
              <div className="dashboard-actions">
                <button onClick={exportToPdf} className="pdf-export-btn">
                  <Download size={15} />
                  Exportar PDF
                </button>
              </div>

              <ReportDisplay 
                markdown={reportData?.markdown_text} 
                formData={formData}
              />

              {(hasPieData || hasEvolutionData) && (
                <div className="charts-grid">
                  <AllocationPieChart
                    data={hasPieData ? reportData.charts.allocation_pie : [{ name: 'Sem Dados', value: 100 }]}
                  />
                  <EvolutionBarChart
                    data={hasEvolutionData ? reportData.charts.evolution_bar : [{ year: new Date().getFullYear(), value: 0 }]}
                  />
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;

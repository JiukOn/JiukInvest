import React from 'react';
import Header from './components/Header';
import NewClientForm from './components/NewClientForm';
import ReportDisplay from './components/ReportDisplay';
import AllocationPieChart from './components/charts/AllocationPieChart';
import EvolutionBarChart from './components/charts/EvolutionBarChart';
import ClientSelector from './components/ClientSelector';
import StatusTimeline from './components/StatusTimeline';
import './App.css';

function App() {
  const [isGenerating, setIsGenerating] = React.useState(false);
  const [showResults, setShowResults] = React.useState(false);
  const [currentStepIndex, setCurrentStepIndex] = React.useState(0);
  const [formData, setFormData] = React.useState(null);

  const handleGenerateStrategy = (data) => {
    console.log('Form data submitted:', data);
    setFormData(data);
    setIsGenerating(true);
    setShowResults(false);
    setCurrentStepIndex(0);
    
    const interval = setInterval(() => {
      setCurrentStepIndex(prev => {
        if(prev >= 4) {
          clearInterval(interval);
          return prev;
        }
        return prev + 1;
      });
    }, 800);

    setTimeout(() => {
      setIsGenerating(false);
      setShowResults(true);
    }, 3200);
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
            <div className="results-dashboard fade-in">
              <ReportDisplay />
              <div className="charts-grid">
                <AllocationPieChart 
                  data={[
                    { name: 'Tesouro Direto', value: 30 },
                    { name: 'CDB Pos-Fixado', value: 40 },
                    { name: 'Ações BR', value: 15 },
                    { name: 'FIIs', value: 15 }
                  ]} 
                />
                <EvolutionBarChart 
                  data={[
                    { year: 2024, value: 100000 },
                    { year: 2025, value: 136000 },
                    { year: 2026, value: 172000 },
                    { year: 2027, value: 208000 },
                    { year: 2028, value: 244000 }
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

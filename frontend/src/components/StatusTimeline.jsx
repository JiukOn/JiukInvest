import React from 'react';
import { CheckCircle2, Clock, CircleDashed, ShieldCheck, Brain, BarChart3, FileText, User, Heart, Database } from 'lucide-react';
import './StatusTimeline.css';

const STEPS = [
  { id: 'data_organizer', label: 'Organizando Dados', icon: Database },
  { id: 'context_analyzer', label: 'Verificação AML', icon: ShieldCheck },
  { id: 'demographics', label: 'Auditoria Demográfica', icon: User },
  { id: 'health_check', label: 'Saúde Financeira', icon: Heart },
  { id: 'emotional_analyzer', label: 'Análise Emocional', icon: Brain },
  { id: 'profile_analyzer', label: 'Perfil de Risco', icon: User },
  { id: 'math_specialist', label: 'Cálculos & Projeções', icon: BarChart3 },
  { id: 'report_writer', label: 'Geração do Relatório', icon: FileText },
  { id: 'compliance', label: 'Revisão de Compliance', icon: ShieldCheck },
];

const StatusTimeline = ({ currentStepIndex = 0 }) => {
  return (
    <div className="status-timeline glass-panel">
      <div className="timeline-header">
        <span className="timeline-badge">AI em execução</span>
        <h3 className="timeline-title">Pipeline de Agentes</h3>
      </div>
      <div className="timeline-steps">
        {STEPS.map((step, index) => {
          const isCompleted = index < currentStepIndex;
          const isActive = index === currentStepIndex;
          const StepIcon = step.icon;

          return (
            <div
              key={step.id}
              className={`timeline-step ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
            >
              <div className="step-connector">
                {index < STEPS.length - 1 && (
                  <div className={`connector-line ${isCompleted ? 'filled' : ''}`} />
                )}
              </div>
              <div className="step-icon-wrapper">
                {isCompleted ? (
                  <CheckCircle2 size={16} />
                ) : isActive ? (
                  <Clock size={16} className="spin-slow" />
                ) : (
                  <CircleDashed size={16} />
                )}
              </div>
              <div className="step-content">
                <span className="step-label">{step.label}</span>
                {isActive && (
                  <span className="step-status">
                    <span className="dot" />
                    <span className="dot" />
                    <span className="dot" />
                  </span>
                )}
                {isCompleted && <span className="step-done">Concluído</span>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusTimeline;

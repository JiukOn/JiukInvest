import React from 'react';
import { CheckCircle2, Clock, CircleDashed } from 'lucide-react';
import './StatusTimeline.css';

const STEPS = [
  { id: 'data_organizer', label: 'Data Organization' },
  { id: 'profile_analyzer', label: 'Profile Analysis' },
  { id: 'report_writer', label: 'Strategy Generation' },
  { id: 'compliance_checker', label: 'Compliance Review' }
];

const StatusTimeline = ({ currentStepIndex = 0 }) => {
  return (
    <div className="status-timeline glass-panel">
      <h3 className="timeline-title">Agent Workflow Status</h3>
      <div className="timeline-steps">
        {STEPS.map((step, index) => {
          const isCompleted = index < currentStepIndex;
          const isActive = index === currentStepIndex;

          return (
            <div 
              key={step.id} 
              className={`timeline-step ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
            >
              <div className="step-icon-wrapper">
                {isCompleted ? (
                  <CheckCircle2 size={20} className="step-icon text-success" />
                ) : isActive ? (
                  <Clock size={20} className="step-icon text-accent spin-slow" />
                ) : (
                  <CircleDashed size={20} className="step-icon text-muted" />
                )}
              </div>
              <div className="step-content">
                <span className="step-label">{step.label}</span>
                {isActive && <span className="step-status">Processing...</span>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StatusTimeline;

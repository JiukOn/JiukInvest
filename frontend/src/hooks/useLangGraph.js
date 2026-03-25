import { useState, useCallback } from 'react';
import { generateReport } from '../services/api';

const BLOCKED_STATUSES = new Set(['blocked', 'restricted', 'health_critical', 'validation_error']);

const buildBlockedReport = (message) => ({
  markdown_text: message,
  charts: { allocation_pie: [], evolution_bar: [] },
});

const SSE_STEP_MAP = {
  DataOrganizer: 0,
  ContextAnalyzer: 1,
  Demographics: 2,
  HealthCheck: 3,
  EmotionalAnalyzer: 4,
  ProfileAnalyzer: 5,
  MathSpecialist: 6,
  ReportWriter: 7,
  Compliance: 8,
};

export const useLangGraph = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [reportData, setReportData] = useState(null);

  const executeGraph = useCallback(async (data) => {
    setIsGenerating(true);
    setShowResults(false);
    setCurrentStepIndex(0);
    setReportData(null);

    try {
      const response = await generateReport(data);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: Erro ao comunicar com a API.`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split('\n\n');
        buffer = parts.pop();

        for (const part of parts) {
          const line = part.trim();
          if (!line.includes('{')) continue;

          try {
            const jsonStr = line.substring(line.indexOf('{'));
            const message = JSON.parse(jsonStr);

            if (message.type === 'log') {
              const stepIdx = SSE_STEP_MAP[message.agent];
              if (stepIdx !== undefined) {
                setCurrentStepIndex(stepIdx);
              }

            } else if (message.type === 'result') {
              setCurrentStepIndex(9);

              if (message.status === 'success') {
                const chartData = message.charts || message.report?.charts || { allocation_pie: [], evolution_bar: [] };
                setReportData({
                  ...message.report,
                  charts: chartData,
                  markdown_text: message.report?.markdown_text || '## Relatório Gerado com Sucesso',
                });

              } else if (BLOCKED_STATUSES.has(message.status)) {
                const statusLabels = {
                  blocked: '🔒 Acesso Bloqueado (AML/Blacklist)',
                  restricted: '🔞 Cliente Não Elegível',
                  health_critical: '⚠️ Saúde Financeira Crítica',
                  validation_error: '❌ Dados Inválidos',
                };
                const title = statusLabels[message.status] || 'Aviso de Governança';
                const md = [
                  `## ${title}`,
                  '',
                  `**Mensagem:** ${message.message}`,
                  message.reason ? `\n**Motivo:** ${message.reason}` : '',
                  message.recommendation ? `\n**Recomendação:** ${message.recommendation}` : '',
                  message.lifecycle_note ? `\n**Nota:** ${message.lifecycle_note}` : '',
                  '',
                  '### Log de Auditoria',
                  message.logs?.map(l => `- ${l}`).join('\n') || '',
                ].filter(Boolean).join('\n');

                setReportData(buildBlockedReport(md));
              }

            } else if (message.type === 'error') {
              throw new Error(message.detail || 'Erro desconhecido do servidor.');
            }
          } catch (_) { /* ignore individual parse errors */ }
        }
      }

      setShowResults(true);
    } catch (error) {
      setReportData(buildBlockedReport(
        `## Erro de Conexão\n\nFalha ao comunicar com o servidor JiukInvest.\n\n**Detalhes:** ${error.message}\n\n> Verifique se o backend está em execução em \`localhost:8000\`.`
      ));
      setShowResults(true);
    } finally {
      setIsGenerating(false);
    }
  }, []);

  return { isGenerating, showResults, currentStepIndex, reportData, executeGraph };
};

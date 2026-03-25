import React, { useState, useEffect } from 'react';
import { Send, DollarSign, Calendar, MessageSquare, Briefcase, User, TrendingUp, ShieldCheck } from 'lucide-react';
import './NewClientForm.css';

const ASSET_OPTIONS = [
  { id: 'Tesouro Direto', label: 'Tesouro Direto', category: 'public' },
  { id: 'CDB / LCI / LCA', label: 'CDB · LCI · LCA', category: 'private' },
  { id: 'Debêntures', label: 'Debêntures', category: 'private' },
  { id: 'Fundos de Crédito', label: 'Fundos de Crédito', category: 'private' },
  { id: 'FIIs', label: 'FIIs', category: 'national' },
  { id: 'Ações Nacionais', label: 'Ações Nacionais', category: 'national' },
  { id: 'Fundos Multimercado', label: 'Multimercado', category: 'national' },
  { id: 'Ações Internacionais', label: 'Ações Globais', category: 'international' },
  { id: 'ETFs Globais', label: 'ETFs Globais', category: 'international' },
  { id: 'Moedas Estrangeiras', label: 'Moedas FX', category: 'international' },
  { id: 'Criptomoedas', label: 'Cripto', category: 'other' },
  { id: 'Outros', label: 'Outros', category: 'other' },
];

const INITIAL_STATE = {
  name: '',
  age: '',
  knowledge_level: 'Iniciante',
  has_invested_before: false,
  past_investments: '',
  investment_horizon_months: 60,
  monthly_income: '',
  monthly_contribution: '',
  initial_investment: '',
  accepts_public_titles: true,
  accepts_private_titles: true,
  accepts_national: true,
  accepts_international: false,
  accepted_asset_types: [],
  additional_comments: '',
};

const formatBRL = (val) => {
  if (!val) return '';
  return Number(val).toLocaleString('pt-BR');
};

const horizonLabel = (months) => {
  if (months < 12) return `${months} meses`;
  const years = months / 12;
  return `${years % 1 === 0 ? years : years.toFixed(1)} ${years === 1 ? 'ano' : 'anos'}`;
};

const NewClientForm = ({ onSubmit, isGenerating, initialData }) => {
  const [formData, setFormData] = useState(INITIAL_STATE);

  useEffect(() => {
    if (initialData) {
      setFormData(prev => ({ ...prev, ...initialData }));
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleAssetToggle = (assetId) => {
    setFormData(prev => {
      const current = prev.accepted_asset_types;
      const updated = current.includes(assetId)
        ? current.filter(a => a !== assetId)
        : [...current, assetId];
      return { ...prev, accepted_asset_types: updated };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const isAdvanced = formData.knowledge_level !== 'Iniciante';

  const visibleAssets = ASSET_OPTIONS.filter(a => {
    if (a.category === 'public') return formData.accepts_public_titles;
    if (a.category === 'private') return formData.accepts_private_titles;
    if (a.category === 'national') return formData.accepts_national;
    if (a.category === 'international') return formData.accepts_international;
    return true;
  });

  return (
    <form className="profile-form" onSubmit={handleSubmit}>

      <div className="form-section-header">
        <User size={14} />
        Dados Pessoais
      </div>

      <div className="form-group-row">
        <div className="form-group flex-2">
          <label>Nome completo do cliente</label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder="Ex: Ana Paula Ferreira" required />
        </div>
        <div className="form-group flex-1">
          <label>Idade</label>
          <input type="number" name="age" min="13" max="100" value={formData.age} onChange={handleChange} placeholder="Ex: 38" required />
        </div>
      </div>

      <div className="form-group-row">
        <div className="form-group">
          <label>Nível de conhecimento do mercado</label>
          <select name="knowledge_level" value={formData.knowledge_level} onChange={handleChange} className="modern-select">
            <option value="Iniciante">Iniciante — Nunca investiu ou apenas poupança</option>
            <option value="Intermediário">Intermediário — Conhece CDB, Tesouro, Fundos</option>
            <option value="Avançado">Avançado — Opera ações, FIIs, derivativos</option>
          </select>
        </div>
      </div>

      <div className="form-group-row">
        <div className="form-group">
          <label>Possui experiência prévia com investimentos?</label>
          <div className="radio-group">
            <label className={`radio-pill ${formData.has_invested_before ? 'selected' : ''}`}>
              <input type="radio" name="has_invested_before" checked={formData.has_invested_before === true}
                onChange={() => setFormData(p => ({ ...p, has_invested_before: true }))} />
              ✓ Sim
            </label>
            <label className={`radio-pill ${!formData.has_invested_before ? 'selected' : ''}`}>
              <input type="radio" name="has_invested_before" checked={formData.has_invested_before === false}
                onChange={() => setFormData(p => ({ ...p, has_invested_before: false, past_investments: '' }))} />
              ✗ Não
            </label>
          </div>
        </div>
      </div>

      {formData.has_invested_before && (
        <div className="form-group fade-in">
          <label><Briefcase size={13} className="icon-inline" /> Quais ativos o cliente já possui ou possuiu?</label>
          <textarea
            name="past_investments" rows="2"
            value={formData.past_investments} onChange={handleChange}
            placeholder="Ex: Tesouro IPCA+, CDB Banco XP, cotas de BVMF3 na bolsa..."
            required
          />
        </div>
      )}

      <div className="form-divider" />

      <div className="form-section-header">
        <DollarSign size={14} />
        Capacidade Financeira
      </div>

      <div className="form-group-row">
        <div className="form-group">
          <label>Renda mensal bruta (R$)</label>
          <input type="number" name="monthly_income" min="0" value={formData.monthly_income} onChange={handleChange} placeholder="Ex: 12.000" required />
        </div>
        <div className="form-group">
          <label>Patrimônio disponível para investir (R$)</label>
          <input type="number" name="initial_investment" min="0" value={formData.initial_investment} onChange={handleChange} placeholder="Ex: 85.000" required />
        </div>
      </div>

      <div className="form-group">
        <label>Aporte mensal planejado (R$)</label>
        <input type="number" name="monthly_contribution" min="0" value={formData.monthly_contribution} onChange={handleChange} placeholder="Ex: 2.500" required />
      </div>

      <div className="form-group slide-container">
        <label>
          <Calendar size={13} className="icon-inline" />
          Horizonte de investimento planejado:&ensp;
          <strong className="horizon-value">{horizonLabel(formData.investment_horizon_months)}</strong>
        </label>
        <input
          type="range" name="investment_horizon_months"
          min="6" max="420" step="6"
          value={formData.investment_horizon_months} onChange={handleChange}
          className="modern-slider"
          style={{ '--pct': `${((formData.investment_horizon_months - 6) / (420 - 6)) * 100}%` }}
        />
        <div className="slider-labels">
          <span>6 meses</span>
          <span>5 anos</span>
          <span>10 anos</span>
          <span>35 anos</span>
        </div>
      </div>

      {isAdvanced && (
        <>
          <div className="form-divider" />

          <div className="form-section-header">
            <TrendingUp size={14} />
            Preferências de Alocação
          </div>

          <div className="form-group-row">
            {[
              { name: 'accepts_public_titles', label: 'Títulos Públicos' },
              { name: 'accepts_private_titles', label: 'Títulos Privados' },
              { name: 'accepts_national', label: 'Ativos Nacionais' },
              { name: 'accepts_international', label: 'Ativos Internacionais' },
            ].map(({ name, label }) => (
              <div className="form-group checkbox-group" key={name}>
                <label className="checkbox-container">
                  <input type="checkbox" name={name} checked={formData[name]} onChange={handleChange} />
                  <span className="checkmark" />
                  {label}
                </label>
              </div>
            ))}
          </div>

          <div className="form-group bg-tint">
            <label><ShieldCheck size={13} className="icon-inline" /> Selecione os ativos de interesse específico</label>
            <div className="chip-grid">
              {visibleAssets.map(asset => (
                <button
                  key={asset.id} type="button"
                  className={`asset-chip ${formData.accepted_asset_types.includes(asset.id) ? 'active' : ''}`}
                  onClick={() => handleAssetToggle(asset.id)}
                >
                  {asset.label}
                </button>
              ))}
            </div>
          </div>
        </>
      )}

      <div className="form-divider" />

      <div className="form-group comment-box">
        <label><MessageSquare size={13} className="icon-inline" /> Contexto adicional do cliente (objetivos, restrições, sonhos)</label>
        <textarea
          name="additional_comments" rows="3"
          value={formData.additional_comments} onChange={handleChange}
          placeholder="Ex: Estou planejando me aposentar em 15 anos. Tenho um filho de 5 anos e quero garantir a faculdade dele. Prefiro evitar alta volatilidade."
        />
      </div>

      <button type="submit" className={`generate-btn ${isGenerating ? 'loading' : ''}`} disabled={isGenerating}>
        {isGenerating ? (
          <span className="jumping-dots">Analisando Perfil<span>.</span><span>.</span><span>.</span></span>
        ) : (
          <><Send size={15} /> Gerar Estratégia Personalizada</>
        )}
      </button>
    </form>
  );
};

export default NewClientForm;

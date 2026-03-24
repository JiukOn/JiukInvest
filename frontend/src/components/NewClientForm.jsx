import React, { useState, useEffect } from 'react';
import { Send, DollarSign, Calendar, MessageSquare, Briefcase, User, Info } from 'lucide-react';
import './NewClientForm.css';

const MOCK_ASSETS = {
  national: ['Ações Nacionais', 'FIIs', 'Fundos Multimercado'],
  international: ['Ações Internacionais', 'Moedas Estrangeiras', 'ETFs Globais'],
  public: ['Tesouro Direto'],
  private: ['CDB / LCI / LCA', 'Debêntures', 'Fundos de Crédito'],
  other: ['Criptomoedas', 'Outros']
};

const NewClientForm = ({ onSubmit, isGenerating, initialData }) => {
  const [formData, setFormData] = useState({
    name: 'Cliente Exemplo',
    age: 35,
    knowledge_level: 'Iniciante',
    has_invested_before: false,
    past_investments: '',
    investment_horizon_months: 60,
    monthly_income: 15000,
    monthly_contribution: 3000,
    initial_investment: 100000,
    accepts_public_titles: true,
    accepts_private_titles: true,
    accepts_national: true,
    accepts_international: false,
    accepted_asset_types: [],
    additional_comments: '',
  });

  useEffect(() => {
    if (initialData) {
      setFormData(prev => ({ ...prev, ...initialData }));
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleAssetToggle = (asset) => {
    setFormData(prev => {
      const current = prev.accepted_asset_types;
      const updated = current.includes(asset) 
        ? current.filter(a => a !== asset)
        : [...current, asset];
      return { ...prev, accepted_asset_types: updated };
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const isAdvanced = formData.knowledge_level === 'Intermediário' || formData.knowledge_level === 'Avançado';
  
  // Dynamic available assets based on toggles
  let availableAssets = [...MOCK_ASSETS.other];
  if (formData.accepts_national) availableAssets.push(...MOCK_ASSETS.national);
  if (formData.accepts_international) availableAssets.push(...MOCK_ASSETS.international);
  if (formData.accepts_public_titles) availableAssets.push(...MOCK_ASSETS.public);
  if (formData.accepts_private_titles) availableAssets.push(...MOCK_ASSETS.private);

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <div className="form-section-title">Contexto Pessoal</div>
      
      <div className="form-group-row">
        <div className="form-group">
          <label>Nome do Cliente <User size={14} className="icon-inline" /></label>
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Idade</label>
          <input type="number" name="age" min="18" value={formData.age} onChange={handleChange} required />
        </div>
      </div>

      <div className="form-group-row">
        <div className="form-group">
          <label>Nível de Conhecimento do Mercado</label>
          <select name="knowledge_level" value={formData.knowledge_level} onChange={handleChange} className="modern-select">
            <option value="Iniciante">Iniciante</option>
            <option value="Intermediário">Intermediário</option>
            <option value="Avançado">Avançado</option>
          </select>
        </div>
        <div className="form-group">
          <label>Já investiu antes?</label>
          <div className="radio-group small-radio">
            <label className={`radio-pill ${formData.has_invested_before ? 'selected' : ''}`}>
              <input type="radio" name="has_invested_before" checked={formData.has_invested_before === true} onChange={() => setFormData(p => ({...p, has_invested_before: true}))} />
              Sim
            </label>
            <label className={`radio-pill ${!formData.has_invested_before ? 'selected' : ''}`}>
              <input type="radio" name="has_invested_before" checked={formData.has_invested_before === false} onChange={() => setFormData(p => ({...p, has_invested_before: false, past_investments: ''}))} />
              Não
            </label>
          </div>
        </div>
      </div>

      {formData.has_invested_before && (
        <div className="form-group fade-in">
          <label>Em quais tipos de ativos você já investiu? <Briefcase size={14} className="icon-inline" /></label>
          <textarea 
            name="past_investments" rows="2" 
            value={formData.past_investments} onChange={handleChange} 
            placeholder="Ex: Poupança, Tesouro Direto..." required
          ></textarea>
        </div>
      )}

      <div className="form-divisor"></div>
      <div className="form-section-title">Valores & Horizonte</div>

      <div className="form-group slide-container">
        <label>Tempo de Investimento Planejado: <strong>{(formData.investment_horizon_months / 12).toFixed(1).replace('.0', '')} anos</strong> <Calendar size={14} className="icon-inline" /></label>
        <input 
          type="range" name="investment_horizon_months" 
          min="6" max="420" step="6" 
          value={formData.investment_horizon_months} onChange={handleChange} 
          className="modern-slider" 
        />
        <div className="slider-labels">
          <span>6 meses</span>
          <span>35 anos</span>
        </div>
      </div>

      <div className="form-group-row">
        <div className="form-group">
          <label>Renda Mensal (R$)</label>
          <input type="number" name="monthly_income" min="0" step="100" value={formData.monthly_income} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Aporte Inicial (R$) <DollarSign size={14} className="icon-inline" /></label>
          <input type="number" name="initial_investment" min="0" step="1000" value={formData.initial_investment} onChange={handleChange} required />
        </div>
      </div>

      <div className="form-group">
        <label>Aporte Mensal Planejado (R$)</label>
        <input type="number" name="monthly_contribution" min="0" step="100" value={formData.monthly_contribution} onChange={handleChange} required />
      </div>

      {isAdvanced && (
        <>
          <div className="form-divisor"></div>
          <div className="form-section-title">Preferências Avançadas de Tipos de Ativos</div>
          
          <div className="form-group-row">
            <div className="form-group checkbox-group">
              <label className="checkbox-container">
                <input type="checkbox" name="accepts_public_titles" checked={formData.accepts_public_titles} onChange={handleChange} />
                <span className="checkmark"></span>
                Aceita Títulos Públicos
              </label>
            </div>
            <div className="form-group checkbox-group">
              <label className="checkbox-container">
                <input type="checkbox" name="accepts_private_titles" checked={formData.accepts_private_titles} onChange={handleChange} />
                <span className="checkmark"></span>
                Aceita Títulos Privados
              </label>
            </div>
          </div>

          <div className="form-group-row">
            <div className="form-group checkbox-group">
              <label className="checkbox-container">
                <input type="checkbox" name="accepts_national" checked={formData.accepts_national} onChange={handleChange} />
                <span className="checkmark"></span>
                Ativos Nacionais
              </label>
            </div>
            <div className="form-group checkbox-group">
              <label className="checkbox-container">
                <input type="checkbox" name="accepts_international" checked={formData.accepts_international} onChange={handleChange} />
                <span className="checkmark"></span>
                Ativos Internacionais
              </label>
            </div>
          </div>

          <div className="form-group fade-in bg-tint">
            <label className="mb-2 block"><Info size={14} className="icon-inline" /> Quais tipos de ativos aceitaria especificamente?</label>
            <div className="chip-grid">
              {availableAssets.map(asset => (
                <button 
                  key={asset} type="button" 
                  className={`asset-chip ${formData.accepted_asset_types.includes(asset) ? 'active' : ''}`}
                  onClick={() => handleAssetToggle(asset)}
                >
                  {asset}
                </button>
              ))}
            </div>
          </div>
        </>
      )}

      <div className="form-divisor"></div>
      
      <div className="form-group comment-box">
        <label>Área de Comentários (Opcional) <MessageSquare size={14} className="icon-inline" /></label>
        <textarea 
          name="additional_comments" rows="3" 
          value={formData.additional_comments} onChange={handleChange} 
          placeholder="Ex: Tenho um sonho de comprar uma casa no exterior em 10 anos..."
        ></textarea>
      </div>

      <button type="submit" className="generate-btn" disabled={isGenerating}>
        {isGenerating ? (
          <span className="jumping-dots">Gerando Análise<span>.</span><span>.</span><span>.</span></span>
        ) : (
          <>Verificar Perfil e Estratégia <Send size={16} /></>
        )}
      </button>
    </form>
  );
};

export default NewClientForm;

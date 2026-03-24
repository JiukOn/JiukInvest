import mockClientsData from '../../../data/mocks/mock_clients.json';

const mapMockToFormData = (client) => {
  let horizonMonths = 60;
  if (client.time_horizon === 'Curto Prazo') horizonMonths = 24;
  if (client.time_horizon === 'Longo Prazo') horizonMonths = 120;

  let knowledge = 'Intermediário';
  if (client.investment_knowledge === 'Básico' || client.investment_knowledge === 'Iniciante') knowledge = 'Iniciante';
  else if (client.investment_knowledge === 'Avançado') knowledge = 'Avançado';

  const hasInvested = client.active_products && client.active_products.length > 0;
  const pastInvestments = hasInvested ? client.active_products.join(', ') : '';

  const acceptsInt = client.suitability_profile === 'Arrojado';
  const acceptsPrivate = client.suitability_profile !== 'Conservador';
  
  const acceptedTypes = [];
  if (client.suitability_profile === 'Arrojado') {
    acceptedTypes.push('Ações Nacionais', 'FIIs', 'Fundos Multimercado', 'Ações Internacionais', 'Criptomoedas');
  } else if (client.suitability_profile === 'Moderado') {
    acceptedTypes.push('Tesouro Direto', 'CDB / LCI / LCA', 'Debêntures', 'Fundos de Crédito');
  } else {
    acceptedTypes.push('Tesouro Direto', 'CDB / LCI / LCA');
  }

  const extraComment = client.investment_objective 
    ? `Meu objetivo financeiro é focado em ${client.investment_objective}.`
    : '';

  return {
    name: client.name || 'Mock Client',
    age: client.age || 35,
    knowledge_level: knowledge,
    has_invested_before: hasInvested,
    past_investments: pastInvestments,
    investment_horizon_months: horizonMonths,
    monthly_income: client.monthly_income || 5000,
    monthly_contribution: client.average_ticket || 500,
    initial_investment: client.total_assets || 10000,
    accepts_public_titles: true,
    accepts_private_titles: acceptsPrivate,
    accepts_national: true,
    accepts_international: acceptsInt,
    accepted_asset_types: acceptedTypes,
    additional_comments: extraComment
  };
};

export const fetchMockProfiles = async () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const profiles = mockClientsData.map(c => ({
        id: c.client_id,
        name: `${c.name} - ${c.suitability_profile}`,
        data: mapMockToFormData(c)
      }));
      resolve(profiles);
    }, 300);
  });
};

import React from 'react';
import { ComposedChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Legend } from 'recharts';
import './Charts.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="chart-tooltip">
        <p className="tooltip-label">{label}</p>
        {payload.map((entry, i) => (
          <p key={i} style={{ color: entry.color, margin: '2px 0', fontSize: '12px' }}>
            {entry.name}: <strong>R$ {Number(entry.value).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</strong>
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const EvolutionBarChart = ({ data }) => {
  if (!data || data.length === 0) return <div className="chart-empty">Sem projeção calculada</div>;

  const isMonthly = data.length > 1 && String(data[1].year).includes('/');
  const periodCount = data.length > 1 ? data.length - 1 : 0;
  const periodLabel = isMonthly ? (periodCount === 1 ? 'Mês' : 'Meses') : (periodCount === 1 ? 'Ano' : 'Anos');

  const hasBenchmarks = data.some(d => d.value_poupanca > 0 || d.value_ibov > 0);

  return (
    <div className="chart-container">
      <h3 className="chart-title">{periodCount > 0 ? `Projeção Patrimonial (${periodCount} ${periodLabel})` : 'Projeção Patrimonial'}</h3>
      <div className="chart-wrapper bar-wrapper" style={{ minHeight: '300px', width: '100%', height: '300px' }}>
        <ResponsiveContainer width="99%" height={300}>
          <ComposedChart
            data={data}
            margin={{ top: 20, right: 10, left: 10, bottom: 5 }}
          >
            <defs>
              <linearGradient id="gradJiuk" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#9d4edd" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#9d4edd" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="gradIbov" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="gradPoup" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6b7280" stopOpacity={0.15}/>
                <stop offset="95%" stopColor="#6b7280" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
            <XAxis
              dataKey="year"
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
              dy={10}
              interval="preserveStartEnd"
              minTickGap={20}
            />
            <YAxis
              tickFormatter={(value) => value === 0 ? '0' : `R$${(value/1000).toFixed(0)}k`}
              axisLine={false}
              tickLine={false}
              tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
              dx={-10}
              domain={[0, 'auto']}
              allowDataOverflow={true}
            />
            <RechartsTooltip content={<CustomTooltip />} />
            {hasBenchmarks && (
              <Legend
                wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
                formatter={(value) => value === 'value' ? 'JiukInvest IA' : value === 'value_ibov' ? 'Ibovespa (histórico)' : 'Poupança'}
              />
            )}
            <Area
              type="monotone"
              dataKey="value"
              name="value"
              stroke="#9d4edd"
              strokeWidth={2.5}
              fill="url(#gradJiuk)"
              dot={false}
              activeDot={{ r: 5, fill: '#9d4edd' }}
              animationBegin={200}
              animationDuration={1000}
            />
            {hasBenchmarks && (
              <Area
                type="monotone"
                dataKey="value_ibov"
                name="value_ibov"
                stroke="#3b82f6"
                strokeWidth={1.5}
                strokeDasharray="5 4"
                fill="url(#gradIbov)"
                dot={false}
                activeDot={{ r: 4, fill: '#3b82f6' }}
              />
            )}
            {hasBenchmarks && (
              <Area
                type="monotone"
                dataKey="value_poupanca"
                name="value_poupanca"
                stroke="#6b7280"
                strokeWidth={1.5}
                strokeDasharray="3 3"
                fill="url(#gradPoup)"
                dot={false}
                activeDot={{ r: 4, fill: '#6b7280' }}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default EvolutionBarChart;

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from 'recharts';
import './Charts.css';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="chart-tooltip">
        <p className="tooltip-label">{label || payload[0].name}</p>
        <p className="tooltip-value">R$ {payload[0].value.toLocaleString('pt-BR')}</p>
      </div>
    );
  }
  return null;
};

const EvolutionBarChart = ({ data }) => {
  if (!data || data.length === 0) return <div className="chart-empty">No evolution data</div>;

  return (
    <div className="chart-container">
      <h3 className="chart-title">5-Year Equity Projection</h3>
      <div className="chart-wrapper bar-wrapper">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 10, left: 10, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
            <XAxis 
              dataKey="year" 
              axisLine={false} 
              tickLine={false} 
              tick={{ fill: 'var(--text-muted)', fontSize: 13 }} 
              dy={10}
            />
            <YAxis 
              tickFormatter={(value) => `R$${(value/1000)}k`} 
              axisLine={false} 
              tickLine={false}
              tick={{ fill: 'var(--text-muted)', fontSize: 13 }}
              dx={-10}
            />
            <RechartsTooltip cursor={{fill: 'var(--bg-surface-elevated)'}} content={<CustomTooltip />} />
            <Bar 
              dataKey="value" 
              fill="var(--accent-primary)" 
              radius={[4, 4, 0, 0]}
              animationBegin={200}
              animationDuration={1500}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={`url(#colorGradient)`} />
              ))}
            </Bar>
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={1}/>
                <stop offset="95%" stopColor="var(--accent-hover)" stopOpacity={0.8}/>
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default EvolutionBarChart;

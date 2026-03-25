import React from 'react';
import { LineChart, LayoutDashboard, UserCircle } from 'lucide-react';
import './Header.css';

const Header = () => {
  return (
    <header className="app-header glass-panel">
      <div className="container header-content">
        <div className="logo-section">
          <div className="logo-icon-wrapper">
            <img src="/favicon.svg" alt="JiukInvest Logo" width="22" height="22" className="logo-icon spin" style={{animationDuration: '18s'}} />
          </div>
          <h1 className="logo-text">Jiuk<span className="logo-accent">Invest</span></h1>
          <span className="header-badge">AI Online</span>
        </div>

        <nav className="header-nav" />

        <div className="user-profile">
          <div className="user-info">
            <span className="user-name">Manager Portal</span>
            <span className="user-role">Wealth Management</span>
          </div>
          <UserCircle size={30} className="user-avatar" />
        </div>
      </div>
    </header>
  );
};

export default Header;

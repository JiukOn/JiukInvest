import React from 'react';
import { LineChart, LayoutDashboard, UserCircle } from 'lucide-react';
import './Header.css';

const Header = () => {
  return (
    <header className="app-header glass-panel">
      <div className="container header-content">
        <div className="logo-section">
          <div className="logo-icon-wrapper">
            <LineChart className="logo-icon" size={24} />
          </div>
          <h1 className="logo-text">GenAI <span className="logo-accent">Copilot</span></h1>
        </div>
        
        <nav className="header-nav">
          <a href="#" className="nav-link active">
            <LayoutDashboard size={18} />
            <span>Workspace</span>
          </a>
        </nav>

        <div className="user-profile">
          <div className="user-info">
            <span className="user-name">Manager Portal</span>
            <span className="user-role">Wealth Management</span>
          </div>
          <UserCircle size={32} className="user-avatar" />
        </div>
      </div>
    </header>
  );
};

export default Header;

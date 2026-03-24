import React, { useState, useEffect } from 'react';
import { Users, Loader } from 'lucide-react';
import { fetchMockProfiles } from '../services/api';
import './ClientSelector.css';

const ClientSelector = ({ onSelect }) => {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadProfiles = async () => {
      try {
        const data = await fetchMockProfiles();
        setProfiles(data);
      } catch (error) {
        console.error("Error loading mock profiles", error);
      } finally {
        setLoading(false);
      }
    };
    
    loadProfiles();
  }, []);

  return (
    <div className="client-selector">
      <div className="selector-header">
        <Users size={16} className="selector-icon" />
        <span>Load Mocks</span>
      </div>
      <div className="selector-buttons">
        {loading ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px' }}>
            <Loader size={16} className="spin" /> Loading Profiles...
          </div>
        ) : (
          profiles.map(profile => (
            <button 
              key={profile.id} 
              type="button"
              className="mock-btn"
              onClick={() => onSelect(profile.data)}
            >
              {profile.name}
            </button>
          ))
        )}
      </div>
    </div>
  );
};

export default ClientSelector;

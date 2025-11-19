import { useState } from 'react';
import './Sidebar.css';

function Sidebar({ currentPage, onPageChange }) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Menu items avec icônes
  const menuItems = [
    { id: 'chat', icon: '💬', label: 'Chat IA', badge: null },
    { id: 'history', icon: '📖', label: 'Historique', badge: null },
    { id: 'quests', icon: '🎯', label: 'Quêtes', badge: '3' },
    { id: 'achievements', icon: '🏆', label: 'Succès', badge: null },
    { id: 'stats', icon: '📊', label: 'Statistiques', badge: null },
    { id: 'settings', icon: '⚙️', label: 'Paramètres', badge: null },
  ];

  return (
    <div className={`sidebar slide-in-left ${isCollapsed ? 'collapsed' : ''}`}>
      {/* Bouton pour réduire/agrandir la sidebar */}
      <button 
        className="sidebar-toggle"
        onClick={() => setIsCollapsed(!isCollapsed)}
        title={isCollapsed ? 'Agrandir' : 'Réduire'}
      >
        {isCollapsed ? '▶' : '◀'}
      </button>

      {/* Menu de navigation */}
      <nav className="sidebar-menu">
        {menuItems.map(item => (
          <button
            key={item.id}
            className={`menu-item ${currentPage === item.id ? 'active' : ''}`}
            onClick={() => onPageChange(item.id)}
            title={isCollapsed ? item.label : ''}
          >
            <span className="menu-icon">{item.icon}</span>
            {!isCollapsed && (
              <>
                <span className="menu-label">{item.label}</span>
                {item.badge && (
                  <span className="menu-badge">{item.badge}</span>
                )}
              </>
            )}
          </button>
        ))}
      </nav>

      {/* Footer avec info version */}
      {!isCollapsed && (
        <div className="sidebar-footer">
          <div className="version-info">
            <span className="version-label">Version</span>
            <span className="version-number">Beta 1.0</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default Sidebar;
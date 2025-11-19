import { useUserContext } from '../../context/UserContext';
import './TopBar.css';

function TopBar(){
    const {user} = useUserContext();

    const xpPercentage = (user.xp / user.xpToNextLevel) * 100;

    return (
    <div className="topbar slide-in-top">
      {/* Logo / Titre */}
      <div className="topbar-brand">
        <span className="brand-icon">🎓</span>
        <h1 className="brand-title gradient-text">AI Learning Arena</h1>
      </div>

      {/* Stats utilisateur */}
      <div className="topbar-stats">
        {/* Niveau */}
        <div className="stat-item">
          <span className="stat-label">Niveau</span>
          <span className="stat-value level-badge">{user.level}</span>
        </div>

        {/* Barre d'XP */}
        <div className="stat-item xp-container">
          <span className="stat-label">XP</span>
          <div className="xp-bar-container">
            <div 
              className="xp-bar-fill" 
              style={{ width: `${xpPercentage}%` }}
            />
            <span className="xp-text">
              {user.xp} / {user.xpToNextLevel}
            </span>
          </div>
        </div>

        {/* Streak */}
        <div className="stat-item">
          <span className="stat-label">🔥 Streak</span>
          <span className="stat-value">{user.streak} jours</span>
        </div>
      </div>

      {/* Avatar et pseudo */}
      <div className="topbar-user">
        <div className="user-avatar">{user.avatar}</div>
        <span className="user-pseudo">{user.pseudo}</span>
      </div>
    </div>
  );
}

export default TopBar;
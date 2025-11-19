import { createContext, useState, useContext, useEffect } from "react";

const UserContext =createContext();

export function UserProvider({children}) {

    const [user, setUser] = useState({
    pseudo: 'Aventurier',  // Pseudo par défaut
    avatar: '🎮',           // Emoji avatar
    level: 1,               // Niveau actuel
    xp: 0,                  // Points d'expérience
    xpToNextLevel: 100,     // XP nécessaire pour le prochain niveau
    streak: 0,              // Jours consécutifs
    totalMessages: 0,       // Messages totaux envoyés
    achievements: [],       // Liste des badges obtenus
  });

  const addXP = (amount = 10) => {
    setUser(prev => {
        const newXP = prev.xp + amount;

        if (newXP >= prev.xpToNextLevel) {
            const newLevel = prev.level +1;
            const remainingXP = newXP - prev.xpToNextLevel;
            const newXPToNextLevel = prev.xpToNextLevel + 50;

            return {
                ...prev,
                xp:newXP,
                totalMessages: prev.totalMessages + 1
            };
        }

        return {
          ...prev,
          xp: newXP,
          totalMessages: prev.totalMessages + 1
        };
    });
  };

  const unlockAchievement = (achivementId) => {
    setUser(prev => {
      if (prev.achievements.includes(achievementId)) {
        return prev;
      }

      return{
        ...prev, 
        achievements: [...prev.achievements, achievementId]
      };
    });
  };

  const updatePseudo = (newPseudo) => {
    setUser(prev => ({
      ...prev,
      pseudo: newPseudo
    }));
  };

  const updateAvatar = (newAvatar) => {
    setUser(prev => ({
      ...prev,
      avatar:newAvatar
    }));
  };

  const value = {
    user,
    addXP,
    unlockAchievement,
    updatePseudo,
    updateAvatar
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

export function useUserContext() {
  const context = useContext(UserContext);

  if(!context){
    throw new Error('useUserContext doit etre utilisé à l\'interieur de UserProvider');
  }

  return context;
}
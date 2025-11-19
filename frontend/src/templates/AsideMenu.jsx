import React from "react";
import { Link } from "react-router-dom";
import { useState, useEffect } from "react";

function AsideMenu() {

    const [user, setUser] = useState(null);
    
        useEffect(() => {
            const token = localStorage.getItem("access_token");
            const userId = localStorage.getItem("user_id");
            console.log('userId:', token);
            console.log('token:', userId);
            if (token && userId) {
                fetch(`http://localhost:8000/users/${userId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
                    .then((res) => {
                        if (!res.ok) throw new Error("Erreur utilisateur");
                        return res.json();
                    })
                    .then((data) => setUser(data))
                    .catch(() => setUser(null));
    
            
            }
            
        }, []);
  return (
    <aside className="aside-menu">
      <nav>
        <ul className="aside-menu-list">
          <li><Link to="/Accueil">Accueil</Link></li>
          <li><Link to="/user">Profil</Link></li>
          <li><Link to="/chat">Mes cours IA</Link></li>
          <li><Link to="/Accueil" onClick={() => {localStorage.removeItem("access_token");
            localStorage.removeItem("user_id");
            window.location.href = "/Login";
          }}>Déconnexion</Link></li>
          
        </ul>
      </nav>
    </aside>
  );
}

export default AsideMenu;

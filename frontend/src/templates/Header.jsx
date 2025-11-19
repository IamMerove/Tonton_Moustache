import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Header_template() {
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
        <div className="header-container">
            <div className="header-title">
                <h1>Tonton Moustache</h1>
            </div>
            <div className="header-link">
                <Link to="/Accueil">Accueil</Link>
                {!user ? (<Link to="/Inscription">Inscription</Link>) : ("")}
                {!user ? (<Link to="/Login">Login</Link>) : ("")}
                
            </div>
            <div className="card-connection">
                {!user ? (<span className="label-connection">Connection</span>) : (<span></span>)}
                
                {user ? (
                    <div>
                        <div>Nom : {user.nom}</div>
                        <div>Prénom : {user.prenom}</div>
                        <button
                            className="bouton-deco"
                            onClick={() => {
                                localStorage.removeItem("access_token");
                                localStorage.removeItem("user_id");
                                window.location.href = "/Login";
                            }}
                        >Déconnexion</button>
                    </div>
                ) : (
                    <p>Non connecté</p>
                )}
            </div>
        </div>
    );
}

export default Header_template;
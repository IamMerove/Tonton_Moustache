import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../App.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

        if (response.ok && data.access_token) {
          // ✅ Stocke le token dans le localStorage
          localStorage.setItem("access_token", data.access_token);
          localStorage.setItem("user_id", data.user.user_id);
          navigate('/user');
          window.location.reload(); // recharge la page pour mettre à jour le header
          navigate('/user');
        } else {
          setError(data.detail || "Identifiants invalides");
      }
    } catch (err) {
      setError("Erreur de connexion au serveur.");
    }
  };

  return (
    <div className="login-container">
      <h2>Connexion</h2>
      <form className="login-form" onSubmit={handleSubmit}>
        <label>Email</label>
        <input
          type="email"
          placeholder="Votre email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Mot de passe</label>
        <input
          type="password"
          placeholder="Votre mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit">Se connecter</button>
        {error && <p className="error-message">{error}</p>}
        <p style={{color:"#000", display:"flex"}}>A enlever !!!</p>
        <p style={{color:"#000", display:"flex"}}>admin_email = "admin@tontonmoustache.com"
        admin_password = "Admin123!"</p>
      </form>

      <footer className="login-footer">
        <p>@2025 Tonton Moustasssss. Tous droits réservés.</p>
        
      </footer>
    </div>
  );
}

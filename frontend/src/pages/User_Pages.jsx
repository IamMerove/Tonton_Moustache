
import { useEffect, useState } from "react";
import MainLayout from "../templates/MainLayout";


function User() {
    const [user, setUser] = useState(null);
    const [roleName, setRoleName] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Récupère l'id et le token du localStorage
    const userId = localStorage.getItem("user_id");
    const token = localStorage.getItem("access_token");

    useEffect(() => {
        async function fetchUser() {
            setLoading(true);
            setError("");
            try {
                const res = await fetch(`http://localhost:8000/users/${userId}`, {
                    headers: {
                        "Authorization": `Bearer ${token}`,
                    },
                });
                if (!res.ok) throw new Error("Impossible de charger le profil utilisateur");
                const data = await res.json();
                setUser(data);
                // Récupère le nom du rôle
                if (data.id_role) {
                    const roleRes = await fetch(`http://localhost:8000/roles/${data.id_role}`);
                    if (roleRes.ok) {
                        const roleData = await roleRes.json();
                        setRoleName(roleData.nom_role);
                    } else {
                        setRoleName("");
                    }
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        if (userId && token) fetchUser();
        else {
            setError("Non connecté");
            setLoading(false);
        }
    }, [userId, token]);

    // Barre de progression XP fictive (à adapter si backend fournit XP)
    const xp = 70; // XP actuel (exemple)
    const xpToNext = 100; // XP pour prochain niveau (exemple)
    const level = 2; // Niveau (exemple)

    return (
        <MainLayout>
            <div className="user-profile-container">
                {loading ? (
                    <div className="loading">Chargement du profil...</div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : user ? (
                    <div className="profile-card card-gaming fade-in">
                        <div className="profile-header">
                            <div className="avatar-large" title="Avatar">
                                {user.avatar ? (
                                    <img src={user.avatar} alt="avatar" className="avatar-img" />
                                ) : (
                                    <span role="img" aria-label="avatar" style={{fontSize: "3rem"}}>👤</span>
                                )}
                            </div>
                            <div className="profile-info">
                                <h2 className="gradient-text">{user.prenom} {user.nom}</h2>
                                <p className="profile-email">{user.email}</p>
                                <p className="profile-role">Rôle : <b>{roleName || user.id_role}</b></p>
                                <p className="profile-niveau">Niveau : <b>{user.id_niveau}</b></p>
                                <p className="profile-date">Inscrit le : {new Date(user.date_inscription).toLocaleDateString()}</p>
                            </div>
                        </div>
                        <div className="profile-xp-section">
                            <div className="xp-label">Niveau <b>{level}</b> — XP : {xp} / {xpToNext}</div>
                            <div className="xp-bar-bg">
                                <div className="xp-bar-fill" style={{width: `${(xp/xpToNext)*100}%`}}></div>
                            </div>
                        </div>
                        <div className="profile-actions">
                            <button className="btn-gaming">Modifier le pseudo</button>
                            <button className="btn-gaming">Changer l'avatar</button>
                        </div>
                        <div className="profile-badges">
                            <span className="badge-gaming">🎯 Débutant</span>
                            <span className="badge-gaming">🔥 Série 3 jours</span>
                            {/* Ajouter d'autres badges dynamiquement */}
                        </div>
                    </div>
                ) : null}
            </div>
            <style>{`
                .user-profile-container {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 60vh;
                }
                .profile-card {
                    background: var(--bg-card);
                    border-radius: 1.5rem;
                    box-shadow: var(--glow-purple);
                    padding: 2.5rem 2rem;
                    min-width: 1040px;
                    max-width: 620px;
                    margin: 2rem 0;
                }
                .profile-header {
                    display: flex;
                    align-items: center;
                    gap: 1.5rem;
                }
                .avatar-large {
                    width: 80px;
                    height: 80px;
                    border-radius: 50%;
                    background: var(--primary-cyan);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                }
                .avatar-img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
                .profile-info h2 {
                    margin: 0 0 0.2em 0;
                }
                .profile-email, .profile-role, .profile-niveau, .profile-date {
                    color: var(--text-secondary);
                    font-size: 1em;
                    margin: 0.1em 0;
                }
                .profile-xp-section {
                    margin: 1.5em 0 1em 0;
                }
                .xp-label {
                    font-size: 1em;
                    margin-bottom: 0.3em;
                }
                .xp-bar-bg {
                    width: 100%;
                    height: 14px;
                    background: #222c;
                    border-radius: 8px;
                    overflow: hidden;
                }
                .xp-bar-fill {
                    height: 100%;
                    background: linear-gradient(90deg, var(--primary-pink), var(--primary-cyan));
                    border-radius: 8px;
                    transition: width 0.5s;
                }
                .profile-actions {
                    display: flex;
                    gap: 1em;
                    margin: 1.2em 0 0.5em 0;
                }
                .btn-gaming {
                    background: var(--primary-purple);
                    color: #fff;
                    border: none;
                    border-radius: 8px;
                    padding: 0.5em 1.2em;
                    font-weight: bold;
                    cursor: pointer;
                    box-shadow: 0 2px 8px #0002;
                    transition: background 0.2s;
                }
                .btn-gaming:hover {
                    background: var(--primary-cyan);
                }
                .profile-badges {
                    margin-top: 1.2em;
                }
                .badge-gaming {
                    display: inline-block;
                    background: var(--primary-cyan);
                    color: #fff;
                    border-radius: 1em;
                    padding: 0.3em 1em;
                    margin-right: 0.5em;
                    font-size: 1em;
                    box-shadow: 0 1px 4px #0002;
                }
                .loading, .error {
                    color: var(--primary-pink);
                    font-size: 1.2em;
                    text-align: center;
                    margin-top: 3em;
                }
            `}</style>
        </MainLayout>
    );
}

export default User;
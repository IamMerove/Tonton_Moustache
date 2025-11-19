import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Formulaire() {
    const [nom, setNom] = useState("");
    const [prenom, setPrenom] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [consentement, setConsentement] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const [roles, setRoles] = useState([]);
    const [niveaux, setNiveaux] = useState([]);
    const [selectedRole, setSelectedRole] = useState(null);
    const [selectedRoleName, setSelectedRoleName] = useState("");
    const [selectedNiveau, setSelectedNiveau] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        // Fetch roles
        const fetchRoles = async () => {
            try {
                const resp = await fetch("http://localhost:8000/roles/read_all_role");
                if (!resp.ok) return;
                const data = await resp.json();
                setRoles(data);
                                if (data.length > 0) {
                    // Prefer a student/user role when available
                    const preferred = data.find((r) => {
                        const n = (r.nom_role || "").toLowerCase();
                        return n.includes("etudiant") || n.includes("élève") || n.includes("eleve") || n.includes("user") || n.includes("student");
                    });
                                    const chosen = preferred ? preferred : data[0];
                                    setSelectedRole(chosen.id_role);
                                    setSelectedRoleName(chosen.nom_role || "");
                }
            } catch (err) {
                // ignore silently or set error
            }
        };

        const fetchNiveaux = async () => {
            try {
                const resp = await fetch("http://localhost:8000/niveau/read_all_niveau");
                if (!resp.ok) return;
                const data = await resp.json();
                setNiveaux(data);
                if (data.length > 0) setSelectedNiveau(data[0].id_niveau);
            } catch (err) {
                // ignore silently or set error
            }
        };

        fetchRoles();
        fetchNiveaux();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        if (!consentement) {
            setError("Vous devez accepter les conditions.");
            return;
        }

        const payload = {
            nom,
            prenom,
            email,
            password,
            avatar: null,
            id_niveau: selectedNiveau || 1,
            id_role: selectedRole || 1,
            consentement_rgpd: consentement,
        };

        try {
            setLoading(true);
            const resp = await fetch("http://localhost:8000/users/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const data = await resp.json();
            if (!resp.ok) {
                const detail = data.detail || data.message || JSON.stringify(data);
                setError(detail);
            } else {
                setSuccess("Inscription réussie. Redirection vers la page de connexion...");
                // small delay then redirect to Login route
                setTimeout(() => navigate("/Login"), 1200);
            }
        } catch (err) {
            setError(String(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="formulaire_inscription" onSubmit={handleSubmit}>
            <div className="form_group">
                <input
                    type="text"
                    placeholder="Nom"
                    value={nom}
                    onChange={(e) => setNom(e.target.value)}
                    required
                />
            </div>

            <div className="form_group">
                <input
                    type="text"
                    placeholder="Prénom"
                    value={prenom}
                    onChange={(e) => setPrenom(e.target.value)}
                    required
                />
            </div>

            <div className="form_group">
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>

            <div className="form_group">
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={6}
                />
            </div>

            {/* Rôle attribué automatiquement — non modifiable par l'utilisateur */}
            <div className="form_group">
                <small>Rôle attribué automatiquement lors de l'inscription.</small>
                <div style={{ marginTop: 6, fontWeight: 600 }}>
                    Rôle attribué : {selectedRoleName || "(chargement...)"}
                </div>
            </div>

            <div className="form_group">
                <label>Niveau</label>
                <select value={selectedNiveau || ""} onChange={(e) => setSelectedNiveau(Number(e.target.value))}>
                    {niveaux.length === 0 && <option value="">-- Aucun niveau --</option>}
                    {niveaux.map((n) => (
                        <option key={n.id_niveau} value={n.id_niveau}>
                            {n.nom_niveau}
                        </option>
                    ))}
                </select>
            </div>

            <div className="form_group">
                <label>
                    <input
                        type="checkbox"
                        checked={consentement}
                        onChange={(e) => setConsentement(e.target.checked)}
                    />
                    &nbsp;J'accepte les conditions
                </label>
            </div>

            {error && <div className="form_error">{error}</div>}
            {success && <div className="form_success">{success}</div>}

            <div className="form_group">
                <button type="submit" disabled={loading}>
                    {loading ? "En cours..." : "S'inscrire"}
                </button>
            </div>
        </form>
    );
}

export default Formulaire;
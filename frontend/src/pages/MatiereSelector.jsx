import { useEffect, useState } from "react";
import MainLayout from "../templates/MainLayout";

function MatiereSelector({ onSelect }) {
  const [matieres, setMatieres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchMatieres() {
      setLoading(true);
      setError("");
      try {
        const res = await fetch("http://localhost:8000/matieres/");
        if (!res.ok) throw new Error("Impossible de charger les matières");
        const data = await res.json();
        setMatieres(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchMatieres();
  }, []);

  return (
    <MainLayout>
      <div className="matiere-selector-container">
        <h2 className="gradient-text">Choisis ta matière</h2>
        <p className="matiere-explainer">
          Sélectionne la matière sur laquelle tu veux discuter ou poser une question. Le chatbot sera configuré pour t'aider spécifiquement sur ce sujet !
        </p>
        {loading ? (
          <div>Chargement...</div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : (
          <div className="matiere-list">
            {matieres.map((m) => (
              <button
                key={m.id_matieres}
                className="matiere-btn"
                onClick={() => onSelect(m)}
              >
                {m.nom_matieres}
              </button>
            ))}
          </div>
        )}
      </div>
      <style>{`
        .matiere-selector-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          margin-top: 3em;
        }
        .matiere-explainer {
          color: var(--text-secondary);
          font-size: 1.1em;
          margin-top: 0.5em;
          margin-bottom: 1.5em;
          text-align: center;
          max-width: 500px;
        }
        .matiere-list {
          display: flex;
          flex-wrap: wrap;
          gap: 1.5em;
          margin-top: 2em;
        }
        .matiere-btn {
          background: var(--primary-cyan);
          color: #fff;
          border: none;
          border-radius: 1em;
          padding: 1em 2em;
          font-size: 1.2em;
          font-weight: bold;
          cursor: pointer;
          box-shadow: 0 2px 8px #0002;
          transition: background 0.2s;
        }
        .matiere-btn:hover {
          background: var(--primary-pink);
        }
      `}</style>
    </MainLayout>
  );
}

export default MatiereSelector;

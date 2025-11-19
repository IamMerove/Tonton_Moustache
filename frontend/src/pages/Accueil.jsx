


import React from 'react';

function Page_Accueil() {
    return (
        <div className="container">
            <header className="header">
                <h1 className="title">Bienvenue sur Tonton Moustache : L'Éducation Réinventée</h1>
                <p className="subtitle">
                    Votre enfant est au collège ou au lycée (de la 6ème à la Terminale) et cherche l'excellence ?
                    Notre plateforme est conçue pour transformer la manière d'apprendre, en offrant un soutien scolaire complet et personnalisé, 24h/24.
                </p>
            </header>
            <div className='container-section'>
                <section className="section">
                    <h2 className="sectionTitle">Pourquoi choisir Tonton Moustache ?</h2>
                    <p>
                        Fini les heures passées à chercher une réponse ou à relire une leçon incomprise.
                        Nous avons intégré un Chat IA révolutionnaire, conçu spécifiquement pour l'éducation secondaire.
                    </p>
                    <ul className="list">
                        <li className="listItem">
                            <strong className="strong">Clarification Instantanée :</strong>
                            Posez n'importe quelle question sur le programme (Maths, Français, Histoire-Géo, Sciences...) et recevez une réponse pédagogique immédiate et adaptée à votre niveau.
                        </li>
                        <li className="listItem">
                            <strong className="strong">Aide aux Devoirs :</strong>
                            Besoin d'un coup de pouce pour démarrer un exercice ou vérifier une démarche ? Notre IA vous guide étape par étape sans jamais donner la solution directe, favorisant l'autonomie et la compréhension.
                        </li>
                        <li className="listItem">
                            <strong className="strong">Réviser à Votre Rythme :</strong>
                            L'IA peut générer des quiz personnalisés sur un chapitre précis ou reformuler un concept complexe avec des exemples concrets et ludiques.
                        </li>
                    </ul>
                </section>

                <section className="section">
                    <h2 className="sectionTitle">Un Contenu Conforme aux Programmes Officiels</h2>
                    <p>
                        De la 6ème à la Terminale, accédez à des ressources de haute qualité, alignées sur les programmes de l'Éducation Nationale.
                    </p>
                    <ul className="list">
                        <li className="listItem">
                            <strong className="strong">Cours Complètement Structurés :</strong>
                            Accédez à des cours détaillés et organisés pour chaque matière et niveau.
                        </li>
                        <li className="listItem">
                            <strong className="strong">Des Milliers d'Exercices Corrigés :</strong>
                            Pratiquez avec des exercices variés et obtenez des corrections détaillées.
                        </li>
                        <li className="listItem">
                            <strong className="strong">Parcours Personnalisés :</strong>
                            Suivez un chemin d'apprentissage adapté à vos besoins et progrès.
                        </li>
                    </ul>
                </section>
            </div>
            
        </div>
    );
}

export default Page_Accueil;
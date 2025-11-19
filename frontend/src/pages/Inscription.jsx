import Formulaire from "../templates/Form_inscription";

function Inscription_Page() {
    return (
        <div className="inscription-container">
            <h2 style={{ color: "var(--primary-cyan)", marginBottom: 18 }}>Inscription</h2>
            <Formulaire />
        </div>
    );
}

export default Inscription_Page;
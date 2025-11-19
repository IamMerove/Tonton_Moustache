import Formulaire from "../templates/Form_inscription";

function Inscription_Page() {
    return (
        <div className="inscription-center-container">
            <h2 className="inscription-title-gaming">Inscrivez-vous</h2>
            <Formulaire />
        </div>
    );
}

export default Inscription_Page;
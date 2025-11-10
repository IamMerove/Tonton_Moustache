

function Formulaire(params) {
    return(
        <>
           <form className="formulaire_inscription">

                <div className="form_group">
                    <input type="text" placeholder="Nom" />
                </div>

                <div className="form_group">
                    <input type="text" placeholder="Prénom" />
                </div>

                <div className="form_group">
                    <input type="email" placeholder="Email" />
                </div>

                <div className="form_group">
                    <input type="password" placeholder="Password" />
                </div>

                <div className="form_group">
                    <input type="button" value="S'inscrire" />
                </div>

                <div className="form_group">
                    <input type="checkbox" name="checkbox"/> Accepter ca gaaaarrssss!
                </div>

           </form>
        </>
    )
}

export default Formulaire;
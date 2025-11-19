import { Link } from "react-router-dom";

function Header_template(params) {
    return(
        <div className="header-container">
            <div className="header-title">
                <h1>Tonton Moustache</h1>
            </div>
            <div className="header-link">
                <Link to="/">Accueil</Link> 
                <Link to="/Inscription">Inscription</Link>
                <Link to="/Login">Login</Link>
            </div>
            <div className="card-connection">
                <span className="label-connection">Connection</span>
                <p>Administrateur</p>
            </div>
            
        </ div>
    )
}

export default Header_template;
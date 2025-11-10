import { Link } from "react-router-dom";

function Header_template(params) {
    return(
        <>
            <Link to="/">Accueil</Link> 
            <Link to="/Inscription">Inscription</Link>
            <Link to="/Login">Login</Link>
        </>
    )
}

export default Header_template;
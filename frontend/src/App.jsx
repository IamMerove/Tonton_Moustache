import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Page_Accueil from './pages/Accueil'
import Header_template from './templates/Header'
import Footer_template from './templates/Footer'
import Inscription_Page from './pages/Inscription'

function App() {
  return (
    <BrowserRouter>
      <Header_template />
      <Routes>
        <Route path="/Acceuil" element={<Page_Accueil />} />
        <Route path="/Inscription" element={<Inscription_Page />} />
        
      </Routes>
      <Footer_template />
    </BrowserRouter>
  )
}

export default App

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Page_Accueil from './pages/Accueil'
import Header_template from './templates/Header'
import Footer_template from './templates/Footer'

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Page_Accueil />} />
        <Route path="/" element={<Page_Accueil />} />

      </Routes>
      <Footer />
    </BrowserRouter>
  )
}

export default App

import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'
import Accueil from './pages/Accueil'
import Header_template from './templates/Header'
import Footer_template from './templates/Footer'
import Inscription_Page from './pages/Inscription'
import Login_page from './pages/Login'
import User from './pages/User_Pages'
import Chat from './templates/Chat_card'

function App() {
  return (
    <BrowserRouter>
      <Header_template />
      <Routes>
        <Route path="/Accueil" element={<Accueil />} />
        <Route path="/user" element={<User />} />
        <Route path="/Inscription" element={<Inscription_Page />} />
        <Route path="/Login" element={<Login_page />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
      <Footer_template />
    </BrowserRouter>
  )
}

export default App

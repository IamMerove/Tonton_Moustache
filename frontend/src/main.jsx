import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// IMPORTS OBLIGATOIRES
import { ChatProvider } from './context/ChatContext.jsx'
import { UserProvider } from './context/UserContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* LES DEUX PROVIDERS DOIVENT ENVELOPPE TOUT */}
    <UserProvider>
      <ChatProvider>
        <App />
      </ChatProvider>
    </UserProvider>
  </StrictMode>
)
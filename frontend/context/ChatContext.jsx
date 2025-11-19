// src/context/ChatContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import { useUserContext } from './UserContext';

const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);

  const { addXP } = useUserContext();

  // Charger l'historique au démarrage
  useEffect(() => {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
      setConversationHistory(JSON.parse(saved));
    }
  }, []);

  // Sauvegarder automatiquement après chaque réponse de l'IA
  useEffect(() => {
    if (messages.length > 1 && messages[messages.length - 1].role === 'assistant') {
      const userFirstMessage = messages.find(m => m.role === 'user')?.content || 'Nouvelle conversation';
      const title = userFirstMessage.substring(0, 40) + (userFirstMessage.length > 40 ? '...' : '');

      const newConv = {
        id: Date.now(),
        title,
        date: new Date().toLocaleDateString('fr-FR'),
        time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }),
        messages: [...messages]
      };

      const updatedHistory = [newConv, ...conversationHistory.filter(c => c.id !== newConv.id)];
      setConversationHistory(updatedHistory);
      localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
    }
  }, [messages]);

  const sendMessage = async (content) => {
    if (!content.trim()) return;

    const userMessage = { role: 'user', content: content.trim() };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: [...messages, userMessage] })
      });

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      addXP(15);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: '❌ Erreur de connexion au serveur' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearMessages = () => {
    setMessages([]);
  };

  const loadConversation = (conv) => {
    setMessages(conv.messages);
  };

  return (
    <ChatContext.Provider value={{
      messages,
      setMessages,               // ← indispensable pour History.jsx
      isLoading,
      sendMessage,
      clearMessages,
      conversationHistory,
      loadConversation: (conv) => setMessages(conv.messages),
    }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChatContext doit être utilisé dans ChatProvider');
  return context;
};
import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useChatContext } from '../../context/ChatContext';
import { useUserContext } from '../../context/UserContext';
import MainLayout from './MainLayout';


function Chat({ matiere }) {
    const { messages, isLoading, sendMessage } = useChatContext();
    const { addXP } = useUserContext();
    const [inputValue, setInputValue] = useState('');
    const [currentPage, setCurrentPage] = useState('chat');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Nouvelle fonction pour envoyer la matière
    const handleSendMessage = () => {
        sendMessage(inputValue, matiere);
        addXP(10);
        setInputValue('');
    };
    return (<>
        <MainLayout>
                <div className="chat-page">
                <div className="chat-header">
                    <h2 className="page-title gradient-text">💬 Assistant IA {matiere?.nom_matieres ? `: ${matiere.nom_matieres}` : 'Personnel'}</h2>
                    <p className="page-subtitle">Pose-moi toutes tes questions sur {matiere?.nom_matieres || 'tes cours'} !</p>
                    <button 
                    onClick={() => setMessages([])}
                    className="bouton-new"
                    >
                    🔄 Nouvelle conversation
                    </button>
                </div>

                <div className="messages-container card-gaming">
                    {messages.length === 0 ? (
                    <div className="empty-state fade-in">
                        <div className="empty-icon">🚀</div>
                        <h3>Commence ton aventure d'apprentissage !</h3>
                        <p>Pose ta première question pour gagner de l'XP</p>
                    </div>
                    ) : (
                    messages.map((message, index) => (
                        <div 
                        key={index} 
                        className={`message ${message.role} fade-in`}
                        >
                        <div className="message-avatar">
                            {message.role === 'user' ? '👤' : '🤖'}
                        </div>
                        <div className="message-content prose prose-invert max-w-none" style={{ whiteSpace: 'pre-line' }}>
                            {message.role === 'assistant' ? (
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                            ) : (
                                <span>{message.content}</span>
                            )}
                        </div>
                        </div>
                    ))
                    )}
                    
                    {isLoading && (
                    <div className="message assistant fade-in">
                        <div className="message-avatar">🤖</div>
                        <div className="message-content loading">
                        <span className="typing-indicator">●●●</span>
                        </div>
                    </div>
                    )}
                    
                    <div ref={messagesEndRef} />
                </div>

                <div className="input-container">
                    <textarea 
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                        }
                    }}
                    placeholder="💭 Tape ta question ici... (Entrée pour envoyer)"
                    rows="2"
                    disabled={isLoading}
                    className="chat-input"
                    />
                    <button 
                    onClick={handleSendMessage}
                    disabled={isLoading || inputValue.trim() === ''}
                    className="send-button"
                    >
                    {isLoading ? '⏳' : '🚀'}
                    <span>{isLoading ? 'Réflexion...' : 'Envoyer'}</span>
                    </button>
                </div>
            </div>
        </MainLayout>
        
    );
    </>)
}

export default Chat;
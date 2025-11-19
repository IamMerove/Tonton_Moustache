import { useChatContext } from '../context/ChatContext';
import { useUserContext } from '../context/UserContext';

export default function History() {
  const { conversationHistory, setMessages } = useChatContext();    // ← IMPORTANT
  const { setCurrentPage } = useUserContext();

  const loadConversation = (conv) => {
    setMessages(conv.messages);      // ← on passe l'objet complet
    setCurrentPage('chat');          // retour automatique sur le chat
  };

  if (conversationHistory.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center p-10">
        <div className="text-8xl mb-6">📖</div>
        <h2 className="text-4xl gradient-text mb-4">Aucune conversation</h2>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-5xl font-bold gradient-text text-center mb-12">📜 Historique</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {conversationHistory.map(conv => (
          <div
            key={conv.id}
            onClick={() => loadConversation(conv)}   // ← on passe conv entier
            className="card-gaming p-6 cursor-pointer hover:scale-105 transition-all duration-300 border-2 border-transparent hover:border-cyan-500"
          >
            <h3 className="text-xl font-bold text-cyan-400 mb-3 line-clamp-2">
              {conv.title}
            </h3>
            <div className="text-sm text-gray-400 space-y-1">
              <p>📅 {conv.date} à {conv.time}</p>
              <p>💬 {conv.messages.length} messages</p>
            </div>
            <div className="mt-6 text-right">
              <span className="bg-gradient-to-r from-cyan-500 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-bold">
                Reprendre →
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
import { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Code2, Loader2 } from 'lucide-react';
import { fetchApi } from '../lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
}

interface Chat {
  id: string;
  title: string;
}

export default function ChatPage() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatId, setChatId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isSending]);

  useEffect(() => {
    const initializeChat = async () => {
      try {
        // 1. Fetch existing chats
        const chats: Chat[] = await fetchApi('/api/chats/');
        
        let activeChatId = null;
        if (chats.length > 0) {
          activeChatId = chats[0].id;
        } else {
          // 2. Create new chat if none exists
          const newChat = await fetchApi('/api/chats/', {
            method: 'POST',
            body: JSON.stringify({ title: 'New Conversation', repository_id: null })
          });
          activeChatId = newChat.id;
        }
        
        setChatId(activeChatId);
        
        // 3. Load messages for the active chat
        if (activeChatId) {
          const chatDetails = await fetchApi(`/api/chats/${activeChatId}`);
          setMessages(chatDetails.messages || []);
        }
      } catch (error) {
        console.error('Failed to initialize chat:', error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeChat();
  }, []);

  const handleSendMessage = async () => {
    if (!input.trim() || !chatId || isSending) return;

    const userMessageContent = input.trim();
    setInput('');
    setIsSending(true);

    // Optimistically add user message to UI
    const tempUserMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: userMessageContent,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, tempUserMessage]);

    try {
      // Send to backend
      const response = await fetchApi(`/api/chats/${chatId}/messages`, {
        method: 'POST',
        body: JSON.stringify({ content: userMessageContent })
      });
      
      // We need to re-fetch the whole chat to get the server-assigned IDs and timestamps
      // for both the user message and assistant message safely, or just append the response.
      // For speed, let's just append the assistant's response.
      setMessages(prev => [...prev, response]);
    } catch (error: any) {
      console.error('Failed to send message:', error);
      // Append an error message from system
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: `Error: ${error.message}`,
        created_at: new Date().toISOString(),
      }]);
    } finally {
      setIsSending(false);
    }
  };

  const formatTime = (isoString: string) => {
    return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="animate-spin text-[var(--color-primary)]" size={32} />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] relative animate-in fade-in duration-500">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Agent Chat</h1>
        <div className="glass-card px-4 py-2 rounded-lg flex items-center gap-2 text-sm border-[var(--color-primary)]/30">
          <Code2 size={16} className="text-[var(--color-primary)]" />
          <span>Context: <span className="font-medium text-white">General</span></span>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 glass-card rounded-2xl p-6 flex flex-col relative overflow-hidden border border-[var(--color-border)]">
        
        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-6 pr-2 mb-4 scrollbar-thin">
          {messages.length === 0 && (
            <div className="text-center text-[var(--color-text-secondary)] mt-10">
              <Bot size={48} className="mx-auto mb-4 opacity-50" />
              <p>No messages yet. Say hello to your AI Agent!</p>
            </div>
          )}
          
          {messages.map((msg) => (
            <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : ''}`}>
              {msg.role === 'assistant' && (
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center shrink-0">
                  <Bot size={20} className="text-white" />
                </div>
              )}
              {msg.role === 'system' && (
                <div className="w-10 h-10 rounded-xl bg-[var(--color-error)] flex items-center justify-center shrink-0">
                  <Code2 size={20} className="text-white" />
                </div>
              )}
              
              <div className={`max-w-[75%] rounded-2xl p-4 shadow-sm ${
                msg.role === 'user' 
                  ? 'bg-[var(--color-primary)] text-white rounded-tr-sm' 
                  : msg.role === 'system'
                    ? 'bg-[var(--color-error)]/20 border border-[var(--color-error)]/50 text-[var(--color-error)] rounded-tl-sm'
                    : 'bg-[var(--color-surface)] border border-[var(--color-border)] rounded-tl-sm'
              }`}>
                <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
                <div className={`text-[10px] mt-2 ${msg.role === 'user' ? 'text-white/70' : 'text-[var(--color-text-secondary)]'}`}>
                  {formatTime(msg.created_at)}
                </div>
              </div>

              {msg.role === 'user' && (
                <div className="w-10 h-10 rounded-xl bg-slate-700 flex items-center justify-center shrink-0">
                  <User size={20} className="text-white" />
                </div>
              )}
            </div>
          ))}
          
          {isSending && (
            <div className="flex gap-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent)] flex items-center justify-center shrink-0">
                <Bot size={20} className="text-white" />
              </div>
              <div className="max-w-[75%] rounded-2xl p-4 shadow-sm bg-[var(--color-surface)] border border-[var(--color-border)] rounded-tl-sm flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-[var(--color-text-secondary)] animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 rounded-full bg-[var(--color-text-secondary)] animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 rounded-full bg-[var(--color-text-secondary)] animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="relative mt-auto">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about your code, generate features, or find bugs..."
            disabled={isSending}
            className="w-full bg-[var(--color-bg-base)] border border-[var(--color-border)] rounded-xl py-4 pl-4 pr-12 focus:outline-none focus:border-[var(--color-accent)] transition-colors text-white disabled:opacity-50"
          />
          <button 
            onClick={handleSendMessage}
            disabled={isSending || !input.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg bg-[var(--color-accent)]/10 text-[var(--color-accent)] hover:bg-[var(--color-accent)] hover:text-white disabled:opacity-50 disabled:hover:bg-[var(--color-accent)]/10 disabled:hover:text-[var(--color-accent)] transition-colors"
          >
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}

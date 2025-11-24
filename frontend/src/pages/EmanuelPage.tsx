import React, { useState, useRef, useEffect } from 'react';

interface Message {
    role: 'user' | 'emanuel';
    content: string;
}

const EmanuelPage: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user' as const, content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080';
            const response = await fetch(`${apiBaseUrl}/emanuel`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userMessage.content }),
            });

            if (!response.body) throw new Error('No response body');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            setMessages(prev => [...prev, { role: 'emanuel', content: '' }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });

                setMessages(prev => {
                    const newMessages = [...prev];
                    const lastMessage = newMessages[newMessages.length - 1];
                    if (lastMessage.role === 'emanuel') {
                        lastMessage.content += chunk;
                    }
                    return newMessages;
                });
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { role: 'emanuel', content: 'Sorry, I encountered an error. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', height: '80vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <h1>Chat with Emanuel</h1>
                <p style={{ color: '#666' }}>Ask me anything about Nightscout and Loop documentation.</p>
            </div>

            <div className="chat-window" style={{
                flex: 1,
                overflowY: 'auto',
                border: '1px solid #ddd',
                borderRadius: '12px',
                padding: '20px',
                backgroundColor: '#f9f9f9',
                marginBottom: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '15px'
            }}>
                {messages.length === 0 && (
                    <div style={{ textAlign: 'center', color: '#999', marginTop: '50px' }}>
                        <p>No messages yet. Start the conversation!</p>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div key={index} style={{
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        maxWidth: '70%',
                        padding: '12px 16px',
                        borderRadius: '12px',
                        backgroundColor: msg.role === 'user' ? '#007bff' : '#ffffff',
                        color: msg.role === 'user' ? '#ffffff' : '#333333',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                        borderBottomRightRadius: msg.role === 'user' ? '4px' : '12px',
                        borderBottomLeftRadius: msg.role === 'emanuel' ? '4px' : '12px'
                    }}>
                        <div style={{ fontSize: '0.8em', marginBottom: '4px', opacity: 0.8 }}>
                            {msg.role === 'user' ? 'You' : 'Emanuel'}
                        </div>
                        <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.5' }}>{msg.content}</div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area" style={{ display: 'flex', gap: '10px' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Type your message..."
                    disabled={isLoading}
                    style={{
                        flex: 1,
                        padding: '12px',
                        borderRadius: '8px',
                        border: '1px solid #ddd',
                        fontSize: '16px',
                        outline: 'none'
                    }}
                />
                <button
                    onClick={sendMessage}
                    disabled={isLoading || !input.trim()}
                    style={{
                        padding: '12px 24px',
                        borderRadius: '8px',
                        border: 'none',
                        backgroundColor: isLoading ? '#ccc' : '#007bff',
                        color: 'white',
                        fontSize: '16px',
                        cursor: isLoading ? 'not-allowed' : 'pointer',
                        transition: 'background-color 0.2s'
                    }}
                >
                    {isLoading ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
};

export default EmanuelPage;

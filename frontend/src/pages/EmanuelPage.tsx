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
            const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
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
        <div className="container" style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px', height: '85vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ textAlign: 'center', marginBottom: '30px' }}>
                <h1 className="text-pop" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Chat with Emanuel</h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '1.1rem' }}>Your expert guide to Nightscout and Loop documentation.</p>
            </div>

            <div className="chat-window" style={{
                flex: 1,
                overflowY: 'auto',
                border: '1px solid rgba(255, 255, 255, 0.1)',
                borderRadius: '20px',
                padding: '25px',
                backgroundColor: 'var(--card-bg)',
                marginBottom: '20px',
                display: 'flex',
                flexDirection: 'column',
                gap: '20px',
                boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)'
            }}>
                {messages.length === 0 && (
                    <div style={{ textAlign: 'center', color: 'rgba(255, 255, 255, 0.4)', marginTop: '80px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
                        <img src="/src/assets/emanuel.png" alt="Emanuel" style={{ width: '100px', height: '100px', borderRadius: '50%', opacity: 0.6, filter: 'grayscale(50%)' }} />
                        <p style={{ fontSize: '1.2rem' }}>Hello! I'm Emanuel. How can I help you today?</p>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div key={index} style={{
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        maxWidth: '80%',
                        display: 'flex',
                        gap: '12px',
                        flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                    }}>
                        {msg.role === 'emanuel' && (
                            <img
                                src="/src/assets/emanuel.png"
                                alt="Emanuel"
                                style={{
                                    width: '35px',
                                    height: '35px',
                                    borderRadius: '50%',
                                    marginTop: '5px',
                                    border: '2px solid var(--primary-color)'
                                }}
                            />
                        )}

                        <div style={{
                            padding: '15px 20px',
                            borderRadius: '18px',
                            backgroundColor: msg.role === 'user' ? 'var(--primary-color)' : 'rgba(255, 255, 255, 0.05)',
                            color: 'var(--text-color)',
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                            borderBottomRightRadius: msg.role === 'user' ? '4px' : '18px',
                            borderBottomLeftRadius: msg.role === 'emanuel' ? '4px' : '18px',
                            border: msg.role === 'emanuel' ? '1px solid rgba(255, 255, 255, 0.1)' : 'none'
                        }}>
                            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6' }}>{msg.content}</div>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area" style={{ display: 'flex', gap: '15px', position: 'relative' }}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask about Nightscout or Loop..."
                    disabled={isLoading}
                    style={{
                        flex: 1,
                        padding: '16px 24px',
                        borderRadius: '16px',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        fontSize: '16px',
                        outline: 'none',
                        backgroundColor: 'rgba(15, 23, 42, 0.6)',
                        color: 'var(--text-color)',
                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
                        transition: 'all 0.3s ease'
                    }}
                />
                <button
                    onClick={sendMessage}
                    disabled={isLoading || !input.trim()}
                    style={{
                        padding: '16px 32px',
                        borderRadius: '16px',
                        border: 'none',
                        background: isLoading ? 'rgba(255, 255, 255, 0.1)' : 'linear-gradient(135deg, var(--primary-color), var(--accent-color))',
                        color: 'white',
                        fontSize: '16px',
                        fontWeight: '600',
                        cursor: isLoading ? 'not-allowed' : 'pointer',
                        transition: 'all 0.3s ease',
                        boxShadow: isLoading ? 'none' : '0 4px 12px rgba(129, 140, 248, 0.3)'
                    }}
                >
                    {isLoading ? (
                        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            <span className="spinner" style={{ width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: 'white', borderRadius: '50%' }}></span>
                            Thinking...
                        </span>
                    ) : 'Send'}
                </button>
            </div>
        </div>
    );
};

export default EmanuelPage;

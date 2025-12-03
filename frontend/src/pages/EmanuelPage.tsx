import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import '../styles/BloodDrop.css';

interface Message {
    role: 'user' | 'emanuel';
    content: string;
}

interface UsageMetadata {
    input_tokens: number;
    output_tokens: number;
}

const EmanuelPage: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [metadata, setMetadata] = useState<UsageMetadata | null>(null);
    const [systemPrompt, setSystemPrompt] = useState<string | null>(null);
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
        setMetadata(null); // Reset metadata for new request

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

            let buffer = '';

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');

                // Process all complete lines
                buffer = lines.pop() || ''; // Keep the last incomplete line in buffer

                for (const line of lines) {
                    if (!line.trim()) continue;

                    try {
                        const data = JSON.parse(line);

                        if (data.type === 'content') {
                            setMessages(prev => {
                                const newMessages = [...prev];
                                const lastMessage = newMessages[newMessages.length - 1];
                                if (lastMessage.role === 'emanuel') {
                                    lastMessage.content += data.text;
                                }
                                return newMessages;
                            });
                        } else if (data.type === 'prompt') {
                            setSystemPrompt(data.text);
                        } else if (data.type === 'usage') {
                            setMetadata({
                                input_tokens: data.input_tokens,
                                output_tokens: data.output_tokens
                            });
                        } else if (data.type === 'error') {
                            console.error('Backend error:', data.text);
                            setMessages(prev => [...prev, { role: 'emanuel', content: `Error: ${data.text}` }]);
                        }
                    } catch (e) {
                        console.error('Error parsing JSON chunk:', e, line);
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { role: 'emanuel', content: 'Sorry, I encountered an error. Please try again later.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="container" style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', height: '95vh', display: 'flex', flexDirection: 'column' }}>
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                <h1 className="text-pop" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Chat with Emanuel</h1>
                <p style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '1.1rem' }}>Your expert guide to Nightscout and Loop documentation.</p>

                {metadata && (
                    <div style={{
                        marginTop: '10px',
                        padding: '8px 16px',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '20px',
                        display: 'inline-block',
                        fontSize: '0.9rem',
                        color: 'rgba(255, 255, 255, 0.9)'
                    }}>
                        <span style={{ marginRight: '15px' }}>Input Tokens: <strong>{metadata.input_tokens}</strong></span>
                        <span>Output Tokens: <strong>{metadata.output_tokens}</strong></span>
                    </div>
                )}
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
                            <div className="markdown-content" style={{ lineHeight: '1.6', overflowWrap: 'break-word' }}>
                                <ReactMarkdown
                                    remarkPlugins={[remarkGfm]}
                                    components={{
                                        a: ({ node, ...props }) => <a {...props} style={{ color: '#60a5fa', textDecoration: 'underline' }} target="_blank" rel="noopener noreferrer" />,
                                        p: ({ node, ...props }) => <p {...props} style={{ marginBottom: '10px' }} />,
                                        ul: ({ node, ...props }) => <ul {...props} style={{ paddingLeft: '20px', marginBottom: '10px' }} />,
                                        ol: ({ node, ...props }) => <ol {...props} style={{ paddingLeft: '20px', marginBottom: '10px' }} />,
                                        code: ({ node, ...props }) => {
                                            const match = /language-(\w+)/.exec(props.className || '')
                                            return match ? (
                                                <div style={{ backgroundColor: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', overflowX: 'auto', margin: '10px 0' }}>
                                                    <code {...props} className={props.className} />
                                                </div>
                                            ) : (
                                                <code {...props} style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '2px 4px', borderRadius: '4px' }} />
                                            )
                                        }
                                    }}
                                >
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area" style={{ display: 'flex', gap: '15px', position: 'relative', marginBottom: '20px' }}>
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
                            <div className="blood-drop-wrapper" style={{ padding: 0, width: '20px', height: '20px' }}>
                                <div className="blood-drop" style={{ width: '12px', height: '12px' }}></div>
                            </div>
                            Thinking...
                        </span>
                    ) : 'Send'}
                </button>
            </div>

            {systemPrompt && (
                <div style={{
                    marginTop: 'auto',
                    padding: '15px',
                    backgroundColor: 'rgba(0, 0, 0, 0.2)',
                    borderRadius: '10px',
                    fontSize: '0.8rem',
                    color: 'rgba(255, 255, 255, 0.5)',
                    maxHeight: '150px',
                    overflowY: 'auto',
                    border: '1px solid rgba(255, 255, 255, 0.05)'
                }}>
                    <details>
                        <summary style={{ cursor: 'pointer', fontWeight: 'bold', marginBottom: '5px' }}>System Prompt (Debug)</summary>
                        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', margin: 0 }}>{systemPrompt}</pre>
                    </details>
                </div>
            )}
        </div>
    );
};

export default EmanuelPage;

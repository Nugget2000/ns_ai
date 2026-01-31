import React from 'react';
import { type SessionEvent } from '../api';
import { useSettings } from '../contexts/SettingsContext';
import './SessionDetailModal.css';

interface SessionDetailModalProps {
    events: SessionEvent[];
    onClose: () => void;
    sessionId: string;
}

const getEventIcon = (eventType: string): string => {
    switch (eventType) {
        case 'login': return '🔐';
        case 'chat_message': return '💬';
        case 'chat_response': return '🤖';
        case 'error': return '❌';
        case 'page_view': return '👁️';
        default: return '📝';
    }
};

const SessionDetailModal: React.FC<SessionDetailModalProps> = ({ events, onClose, sessionId }) => {
    const { formatDateTime } = useSettings();
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>Session Events</h2>
                    <span className="session-id">ID: {sessionId.slice(0, 8)}...</span>
                    <button className="close-btn" onClick={onClose}>×</button>
                </div>

                <div className="events-timeline">
                    {events.length === 0 ? (
                        <div className="no-events">No events recorded for this session</div>
                    ) : (
                        events.map((event) => (
                            <div
                                key={event.event_id}
                                className={`event-card ${event.event_type} ${event.error_info ? 'has-error' : ''}`}
                            >
                                <div className="event-header">
                                    <span className="event-icon">{getEventIcon(event.event_type)}</span>
                                    <span className="event-type">{event.event_type.replace('_', ' ')}</span>
                                    <span className="event-time">{formatDateTime(event.timestamp)}</span>
                                </div>

                                <div className="event-body">
                                    {/* Login Event */}
                                    {event.event_type === 'login' && (
                                        <div className="event-details">
                                            <p><strong>Email:</strong> {String(event.data.email || 'N/A')}</p>
                                            {'user_agent' in event.data && event.data.user_agent ? (
                                                <p className="user-agent"><strong>Browser:</strong> {String(event.data.user_agent)}</p>
                                            ) : null}
                                            {'ip' in event.data && event.data.ip ? (
                                                <p><strong>IP:</strong> {String(event.data.ip)}</p>
                                            ) : null}
                                        </div>
                                    )}

                                    {/* Chat Message */}
                                    {event.event_type === 'chat_message' && (
                                        <div className="chat-message-content">
                                            <div className="message-bubble user">
                                                {String(event.data.message || '')}
                                            </div>
                                            <span className="message-length">
                                                {Number(event.data.message_length) || 0} chars
                                            </span>
                                        </div>
                                    )}

                                    {/* Chat Response */}
                                    {event.event_type === 'chat_response' && (
                                        <div className="chat-response-content">
                                            <div className="message-bubble assistant">
                                                {String(event.data.response || '')}
                                                {Number(event.data.response_length) > 2000 && (
                                                    <span className="truncated"> ... (truncated)</span>
                                                )}
                                            </div>
                                            <div className="metrics">
                                                {'input_tokens' in event.data && event.data.input_tokens ? (
                                                    <span className="metric">
                                                        📥 {Number(event.data.input_tokens)} input tokens
                                                    </span>
                                                ) : null}
                                                {'output_tokens' in event.data && event.data.output_tokens ? (
                                                    <span className="metric">
                                                        📤 {Number(event.data.output_tokens)} output tokens
                                                    </span>
                                                ) : null}
                                                {'duration_ms' in event.data && event.data.duration_ms ? (
                                                    <span className="metric">
                                                        ⏱️ {(Number(event.data.duration_ms) / 1000).toFixed(1)}s
                                                    </span>
                                                ) : null}
                                            </div>
                                        </div>
                                    )}

                                    {/* Error Event */}
                                    {(event.event_type === 'error' || event.error_info) && (
                                        <div className="error-content">
                                            <div className="error-info">
                                                <p className="error-type">
                                                    <strong>Type:</strong> {event.error_info?.error_type || 'Unknown'}
                                                </p>
                                                <p className="error-message">
                                                    <strong>Message:</strong> {event.error_info?.message || 'No message'}
                                                </p>
                                                {'endpoint' in event.data && event.data.endpoint ? (
                                                    <p><strong>Endpoint:</strong> {String(event.data.endpoint)}</p>
                                                ) : null}
                                            </div>
                                            {event.stacktrace && (
                                                <details className="stacktrace-container">
                                                    <summary>View Stacktrace</summary>
                                                    <pre className="stacktrace">{event.stacktrace}</pre>
                                                </details>
                                            )}
                                        </div>
                                    )}

                                    {/* Page View */}
                                    {event.event_type === 'page_view' && (
                                        <div className="event-details">
                                            <p><strong>Page:</strong> {String(event.data.page || 'N/A')}</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default SessionDetailModal;

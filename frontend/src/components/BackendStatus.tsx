import React, { useState, useEffect } from 'react';
import { getHealth, getVersion, getPageLoad } from '../api';

type HealthStatus = 'loading' | 'healthy' | 'unhealthy';

const BackendStatus: React.FC = () => {
    const [status, setStatus] = useState<HealthStatus>('loading');
    const [version, setVersion] = useState<string>('');
    const [pageCount, setPageCount] = useState<number | null>(null);
    const [statusMessage, setStatusMessage] = useState<string>('Checking backend...');

    const checkBackend = async () => {
        try {
            const [healthData, versionData] = await Promise.all([
                getHealth(),
                getVersion(),
            ]);

            if (healthData.status === 'ok') {
                setStatus('healthy');
                setVersion(versionData.version);
                setStatusMessage(`Backend healthy - v${versionData.version}`);
            } else {
                setStatus('unhealthy');
                setStatusMessage('Backend returned unexpected status');
            }
        } catch {
            setStatus('unhealthy');
            setStatusMessage('Backend unavailable');
        }
    };

    const trackPageLoad = async () => {
        try {
            const pageLoadData = await getPageLoad();
            setPageCount(pageLoadData.count);
        } catch (error) {
            console.error('Failed to track page load:', error);
        }
    };

    useEffect(() => {
        let mounted = true;

        const check = async () => {
            if (mounted) await checkBackend();
        };

        const track = async () => {
            if (mounted) await trackPageLoad();
        };

        // Initial check
        void check();
        void track();

        // Auto-refresh health every 5 minutes
        const interval = setInterval(() => {
             void check();
        }, 300000);

        return () => {
            mounted = false;
            clearInterval(interval);
        };
    }, []);

    const getStatusIcon = () => {
        switch (status) {
            case 'healthy':
                return (
                    <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="status-icon status-healthy"
                    >
                        <defs>
                            <linearGradient id="healthyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="#10b981" />
                                <stop offset="100%" stopColor="#059669" />
                            </linearGradient>
                            <filter id="healthyShadow">
                                <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#10b981" floodOpacity="0.4" />
                            </filter>
                        </defs>
                        <circle
                            cx="12"
                            cy="12"
                            r="10"
                            fill="url(#healthyGradient)"
                            filter="url(#healthyShadow)"
                        />
                        <path
                            d="M8 12L11 15L16 9"
                            stroke="white"
                            strokeWidth="2.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                );
            case 'unhealthy':
                return (
                    <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="status-icon status-unhealthy"
                    >
                        <defs>
                            <linearGradient id="unhealthyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="#ef4444" />
                                <stop offset="100%" stopColor="#dc2626" />
                            </linearGradient>
                            <filter id="unhealthyShadow">
                                <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#ef4444" floodOpacity="0.4" />
                            </filter>
                        </defs>
                        <circle
                            cx="12"
                            cy="12"
                            r="10"
                            fill="url(#unhealthyGradient)"
                            filter="url(#unhealthyShadow)"
                        />
                        <path
                            d="M8.5 8.5L15.5 15.5M15.5 8.5L8.5 15.5"
                            stroke="white"
                            strokeWidth="2.5"
                            strokeLinecap="round"
                        />
                    </svg>
                );
            case 'loading':
                return (
                    <svg
                        width="24"
                        height="24"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        className="status-icon status-loading"
                    >
                        <defs>
                            <linearGradient id="loadingGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stopColor="#f59e0b" />
                                <stop offset="100%" stopColor="#d97706" />
                            </linearGradient>
                        </defs>
                        <circle
                            cx="12"
                            cy="12"
                            r="10"
                            stroke="url(#loadingGradient)"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeDasharray="15 45"
                            fill="none"
                        />
                    </svg>
                );
        }
    };

    return (
        <div className="backend-status" title={statusMessage}>
            {getStatusIcon()}
            {version && (
                <span className="backend-version">v{version}</span>
            )}
            {pageCount !== null && (
                <>
                    <span style={{
                        margin: '0 0.5rem',
                        color: 'rgba(248, 250, 252, 0.3)',
                        fontSize: '0.9rem'
                    }}>•</span>
                    <span className="backend-version" title={`Total page visits: ${pageCount}`}>
                        👁️ {pageCount.toLocaleString()}
                    </span>
                </>
            )}
        </div>
    );
};

export default BackendStatus;

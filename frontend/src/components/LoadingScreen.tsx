import React from 'react';
import './LoadingScreen.css';

interface LoadingScreenProps {
    message?: string;
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({
    message = "Initializing AI-powered diabetes analytics..."
}) => {
    return (
        <div className="loading-screen">
            {/* Neural network background decorations */}
            <div className="loading-neural-bg">
                <div className="loading-neural-node" style={{ top: '15%', left: '10%', animationDelay: '0s' }} />
                <div className="loading-neural-node" style={{ top: '25%', left: '85%', animationDelay: '0.5s' }} />
                <div className="loading-neural-node" style={{ top: '70%', left: '15%', animationDelay: '1s' }} />
                <div className="loading-neural-node" style={{ top: '80%', left: '90%', animationDelay: '1.5s' }} />
                <div className="loading-neural-node" style={{ top: '45%', left: '5%', animationDelay: '0.3s' }} />
                <div className="loading-neural-node" style={{ top: '55%', left: '95%', animationDelay: '0.8s' }} />
            </div>

            {/* Main icon with pulse rings */}
            <div className="loading-icon-container">
                <div className="loading-pulse-ring" />
                <div className="loading-pulse-ring" />
                <div className="loading-pulse-ring" />
                <svg className="loading-icon" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                    {/* Blood drop outline - diabetes symbol */}
                    <path
                        d="M60 20 C60 20, 40 45, 40 65 C40 78, 48 88, 60 88 C72 88, 80 78, 80 65 C80 45, 60 20, 60 20 Z"
                        stroke="url(#loadingGrad1)"
                        strokeWidth="2.5"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="loading-drop-path"
                    />

                    {/* Neural network nodes - AI symbol */}
                    <circle cx="60" cy="45" r="4" fill="url(#loadingGrad2)" opacity="0.9" className="loading-node loading-node-1" />
                    <circle cx="50" cy="58" r="3.5" fill="url(#loadingGrad3)" opacity="0.8" className="loading-node loading-node-2" />
                    <circle cx="70" cy="58" r="3.5" fill="url(#loadingGrad3)" opacity="0.8" className="loading-node loading-node-3" />
                    <circle cx="45" cy="70" r="3" fill="url(#loadingGrad2)" opacity="0.7" className="loading-node loading-node-4" />
                    <circle cx="60" cy="72" r="3" fill="url(#loadingGrad2)" opacity="0.7" className="loading-node loading-node-5" />
                    <circle cx="75" cy="70" r="3" fill="url(#loadingGrad2)" opacity="0.7" className="loading-node loading-node-6" />

                    {/* Neural connections */}
                    <line x1="60" y1="45" x2="50" y2="58" stroke="url(#loadingGrad2)" strokeWidth="1.5" className="loading-connection loading-connection-1" />
                    <line x1="60" y1="45" x2="70" y2="58" stroke="url(#loadingGrad2)" strokeWidth="1.5" className="loading-connection loading-connection-2" />
                    <line x1="50" y1="58" x2="45" y2="70" stroke="url(#loadingGrad3)" strokeWidth="1.5" className="loading-connection loading-connection-3" />
                    <line x1="50" y1="58" x2="60" y2="72" stroke="url(#loadingGrad3)" strokeWidth="1.5" className="loading-connection loading-connection-4" />
                    <line x1="70" y1="58" x2="60" y2="72" stroke="url(#loadingGrad3)" strokeWidth="1.5" className="loading-connection loading-connection-5" />
                    <line x1="70" y1="58" x2="75" y2="70" stroke="url(#loadingGrad3)" strokeWidth="1.5" className="loading-connection loading-connection-6" />

                    {/* Gradient definitions */}
                    <defs>
                        <linearGradient id="loadingGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#818cf8" />
                            <stop offset="50%" stopColor="#38bdf8" />
                            <stop offset="100%" stopColor="#c084fc" />
                        </linearGradient>
                        <linearGradient id="loadingGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#38bdf8" />
                            <stop offset="100%" stopColor="#818cf8" />
                        </linearGradient>
                        <linearGradient id="loadingGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#c084fc" />
                            <stop offset="50%" stopColor="#818cf8" />
                            <stop offset="100%" stopColor="#38bdf8" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>

            <h1 className="loading-title">NS AI</h1>
            <p className="loading-subtitle">The microbolus generation</p>

            {/* Glucose wave visualization */}
            <div className="loading-glucose-wave-container">
                <svg className="loading-glucose-wave" viewBox="0 0 400 50" preserveAspectRatio="none">
                    <path
                        d="M0 25 Q25 10, 50 25 T100 25 T150 25 T200 25 T250 25 T300 25 T350 25 T400 25"
                        stroke="url(#loadingWaveGrad)"
                        strokeWidth="2"
                        fill="none"
                        strokeLinecap="round"
                    />
                    <defs>
                        <linearGradient id="loadingWaveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#818cf8" stopOpacity="0" />
                            <stop offset="50%" stopColor="#38bdf8" />
                            <stop offset="100%" stopColor="#c084fc" stopOpacity="0" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>

            {/* Loading dots */}
            <div className="loading-dots">
                <div className="loading-dot" />
                <div className="loading-dot" />
                <div className="loading-dot" />
            </div>

            <p className="loading-message">{message}</p>
        </div>
    );
};

export default LoadingScreen;

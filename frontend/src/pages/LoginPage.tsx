import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loader } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import DiabetesAIIcon from '../components/DiabetesAIIcon';

const LoginPage: React.FC = () => {
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async () => {
        setError('');
        setIsLoading(true);
        try {
            await login();
            navigate('/');
        } catch (err) {
            setError('Failed to sign in. Please try again.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <DiabetesAIIcon size={80} interactive={true} />
                    <h1 className="text-pop" style={{ fontSize: '2.5rem', margin: '1.5rem 0 0.5rem' }}>
                        NS AI
                    </h1>
                    <p style={{
                        color: 'rgba(255, 255, 255, 0.7)',
                        fontSize: '1rem',
                        marginBottom: '2rem'
                    }}>
                        Sign in with Google to continue
                    </p>
                </div>

                <div className="login-form">
                    {error && (
                        <div className="error-message" role="alert">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <circle cx="12" cy="12" r="10" />
                                <line x1="12" y1="8" x2="12" y2="12" />
                                <line x1="12" y1="16" x2="12.01" y2="16" />
                            </svg>
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleLogin}
                        className="login-button"
                        disabled={isLoading}
                    >
                        {isLoading ? (
                            <>
                                <Loader className="spinner" size={20} />
                                <span>Signing in...</span>
                            </>
                        ) : (
                            'Sign in with Google'
                        )}
                    </button>
                </div>

                <div className="login-footer">
                    <p style={{
                        color: 'rgba(255, 255, 255, 0.5)',
                        fontSize: '0.875rem',
                        textAlign: 'center'
                    }}>
                        Secure access to your diabetes AI assistant
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;

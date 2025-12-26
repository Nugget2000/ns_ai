import React from 'react';
import underConstructionImg from '../assets/insights_under_construction.png';

const InsightsPage: React.FC = () => {
    return (
        <div className="container" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '80vh',
            textAlign: 'center'
        }}>
            <h1 className="text-pop" style={{ fontSize: '3rem', marginBottom: '1rem' }}>AI Insights</h1>

            <div style={{
                maxWidth: '800px',
                width: '100%',
                borderRadius: '24px',
                overflow: 'hidden',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)',
                border: '1px solid rgba(255,255,255,0.1)',
                backgroundColor: 'rgba(15, 23, 42, 0.4)',
                backdropFilter: 'blur(10px)',
                padding: '2rem',
                marginBottom: '2rem'
            }}>
                <img
                    src={underConstructionImg}
                    alt="AI Personas under construction"
                    style={{
                        width: '100%',
                        height: 'auto',
                        borderRadius: '16px',
                        marginBottom: '1.5rem',
                        border: '1px solid rgba(129, 140, 248, 0.2)'
                    }}
                />
                <h2 style={{ color: 'var(--primary-color)', fontSize: '1.5rem', marginBottom: '0.5rem' }}>
                    Systems Offline - The insight section is under development
                </h2>
                <p style={{ color: 'rgba(255, 255, 255, 0.6)', fontSize: '1.1rem' }}>
                    Benny, Cora, and Hanna are currently recalibrating the data core.
                </p>
            </div>

            <p style={{ color: 'rgba(255, 255, 255, 0.4)' }}>
                Connect again soon for full access.
            </p>
        </div>
    );
};

export default InsightsPage;

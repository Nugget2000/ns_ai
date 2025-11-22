import React from 'react';
import { Link } from 'react-router-dom';
import emanuel from '../assets/emanuel.png';
import hanna from '../assets/hanna.png';
import cora from '../assets/cora.png';
import benny from '../assets/benny.png';
import DiabetesAIIcon from '../components/DiabetesAIIcon';

const LandingPage: React.FC = () => {
    return (
        <div className="container">
            <header style={{ textAlign: 'center', marginTop: '3rem', marginBottom: '5rem' }}>
                <div style={{ marginBottom: '2rem' }}>
                    <DiabetesAIIcon size={120} interactive={true} />
                </div>
                <h1 className="text-pop" style={{ fontSize: '4rem', marginBottom: '1rem', lineHeight: '1' }}>
                    NS AI
                </h1>
                <p style={{
                    fontSize: '1.5rem',
                    color: 'var(--secondary-color)',
                    fontWeight: '600',
                    marginTop: '1rem'
                }}>
                    The microbolus generation is here
                </p>
                <p style={{
                    fontSize: '1rem',
                    color: 'rgba(248, 250, 252, 0.7)',
                    maxWidth: '700px',
                    margin: '2rem auto 0',
                    lineHeight: '1.6'
                }}>
                    AI-powered analysis and management for Type 1 diabetes using Nightscout and Loop.
                    Built on the incredible work of the open source community.
                </p>
            </header>

            <section style={{ marginBottom: '5rem' }}>
                <h2 style={{
                    textAlign: 'center',
                    fontSize: '2.5rem',
                    marginBottom: '3rem',
                    color: 'var(--primary-color)'
                }}>
                    Meet Your AI Personas
                </h2>
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                    gap: '2rem'
                }}>
                    <div className="card">
                        <img src={emanuel} alt="Emanuel Reading" className="persona-image" />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--secondary-color)' }}>
                            Emanuel Reading
                        </h3>
                        <p style={{ marginBottom: '1.5rem', color: 'rgba(248, 250, 252, 0.8)' }}>
                            Expert on Nightscout and Loop documentation. Get immediate answers to your questions.
                        </p>
                        <Link
                            to="/emanuel"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                background: 'linear-gradient(135deg, var(--primary-color), var(--accent-color))',
                                color: '#fff',
                                borderRadius: '8px',
                                fontWeight: '600',
                                transition: 'transform 0.2s ease'
                            }}
                        >
                            Chat with Emanuel →
                        </Link>
                    </div>

                    <div className="card">
                        <img src={hanna} alt="Hanna Horizon" className="persona-image" />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--secondary-color)' }}>
                            Hanna Horizon
                        </h3>
                        <p style={{ marginBottom: '1.5rem', color: 'rgba(248, 250, 252, 0.8)' }}>
                            Data analyst for overarching retrospective analysis. Calculates KPIs and provides insights.
                        </p>
                        <Link
                            to="/insights"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                background: 'linear-gradient(135deg, var(--primary-color), var(--accent-color))',
                                color: '#fff',
                                borderRadius: '8px',
                                fontWeight: '600',
                                transition: 'transform 0.2s ease'
                            }}
                        >
                            Get Insights →
                        </Link>
                    </div>

                    <div className="card">
                        <img src={cora} alt="Cora Carbcount" className="persona-image" />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--secondary-color)' }}>
                            Cora Carbcount
                        </h3>
                        <p style={{ marginBottom: '1.5rem', color: 'rgba(248, 250, 252, 0.8)' }}>
                            Detailed event analysis expert. Finds significant patterns and provides actionable insights.
                        </p>
                        <Link
                            to="/insights"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                background: 'linear-gradient(135deg, var(--primary-color), var(--accent-color))',
                                color: '#fff',
                                borderRadius: '8px',
                                fontWeight: '600',
                                transition: 'transform 0.2s ease'
                            }}
                        >
                            Get Insights →
                        </Link>
                    </div>

                    <div className="card">
                        <img src={benny} alt="Benny Basal" className="persona-image" />
                        <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--secondary-color)' }}>
                            Benny Basal
                        </h3>
                        <p style={{ marginBottom: '1.5rem', color: 'rgba(248, 250, 252, 0.8)' }}>
                            Settings analysis specialist. Verifies and optimizes your pump settings.
                        </p>
                        <Link
                            to="/insights"
                            style={{
                                display: 'inline-block',
                                padding: '0.75rem 1.5rem',
                                background: 'linear-gradient(135deg, var(--primary-color), var(--accent-color))',
                                color: '#fff',
                                borderRadius: '8px',
                                fontWeight: '600',
                                transition: 'transform 0.2s ease'
                            }}
                        >
                            Get Insights →
                        </Link>
                    </div>
                </div>
            </section>

            <section style={{ marginBottom: '4rem' }}>
                <div
                    className="card"
                    style={{
                        borderLeft: '4px solid var(--accent-color)',
                        background: 'linear-gradient(135deg, rgba(192, 132, 252, 0.1), rgba(129, 140, 248, 0.1))'
                    }}
                >
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: 'var(--accent-color)' }}>
                        ⚠️ Important Disclaimer
                    </h3>
                    <p style={{ color: 'rgba(248, 250, 252, 0.9)', lineHeight: '1.6' }}>
                        The insights and recommendations provided by this application and its AI personas are for
                        informational and educational purposes only. They should be used as advice to support your
                        diabetes management, not as a replacement for professional medical guidance. Always consult
                        with your healthcare provider before making any medical decisions or changes to your treatment plan.
                    </p>
                </div>
            </section>

            <section style={{ textAlign: 'center', marginBottom: '4rem' }}>
                <h2 style={{
                    fontSize: '2.5rem',
                    marginBottom: '2rem',
                    color: 'var(--primary-color)'
                }}>
                    How It Works
                </h2>
                <p style={{
                    fontSize: '1.2rem',
                    maxWidth: '800px',
                    margin: '0 auto',
                    color: 'rgba(248, 250, 252, 0.8)',
                    lineHeight: '1.8'
                }}>
                    Connect your Nightscout data and let our AI personas analyze your diabetes management patterns
                    to provide actionable insights. Emanuel is ready for immediate interaction to help you understand
                    the documentation. For deeper analysis with Hanna, Cora, and Benny, you'll need to sign up and
                    provide access to your Nightscout data.
                </p>
            </section>
        </div>
    );
};

export default LandingPage;

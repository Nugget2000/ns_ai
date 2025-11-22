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
                    marginBottom: '4rem',
                    color: 'var(--primary-color)'
                }}>
                    Meet Your AI Personas
                </h2>

                {/* Documentation Category */}
                <div style={{ marginBottom: '4rem' }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '1rem',
                        marginBottom: '2rem'
                    }}>
                        <div style={{
                            display: 'inline-block',
                            padding: '0.5rem 1.5rem',
                            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2))',
                            border: '2px solid rgba(99, 102, 241, 0.5)',
                            borderRadius: '20px',
                            fontSize: '0.9rem',
                            fontWeight: '700',
                            letterSpacing: '0.05em',
                            textTransform: 'uppercase',
                            color: 'var(--secondary-color)'
                        }}>
                            📚 Documentation
                        </div>
                        <div style={{
                            flex: 1,
                            height: '2px',
                            background: 'linear-gradient(90deg, rgba(99, 102, 241, 0.5), transparent)'
                        }}></div>
                    </div>

                    <div style={{
                        display: 'flex',
                        justifyContent: 'center'
                    }}>
                        <div className="card" style={{
                            maxWidth: '500px',
                            background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.05))',
                            borderColor: 'rgba(99, 102, 241, 0.3)',
                            transform: 'scale(1.02)',
                            boxShadow: '0 8px 32px rgba(99, 102, 241, 0.2)'
                        }}>
                            <img src={emanuel} alt="Emanuel Reading" className="persona-image" style={{
                                border: '3px solid rgba(99, 102, 241, 0.5)'
                            }} />
                            <h3 style={{ fontSize: '1.8rem', marginBottom: '0.5rem', color: 'var(--secondary-color)' }}>
                                Emanuel Reading
                            </h3>
                            <p style={{ marginBottom: '1.5rem', color: 'rgba(248, 250, 252, 0.9)', fontSize: '1.05rem' }}>
                                Expert on Nightscout and Loop documentation. Get immediate answers to your questions.
                            </p>
                            <Link
                                to="/emanuel"
                                style={{
                                    display: 'inline-block',
                                    padding: '0.875rem 2rem',
                                    background: 'linear-gradient(135deg, #6366f1, #a855f7)',
                                    color: '#fff',
                                    borderRadius: '12px',
                                    fontWeight: '700',
                                    fontSize: '1.05rem',
                                    transition: 'all 0.3s ease',
                                    boxShadow: '0 4px 16px rgba(99, 102, 241, 0.4)'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 8px 24px rgba(99, 102, 241, 0.5)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = '0 4px 16px rgba(99, 102, 241, 0.4)';
                                }}
                            >
                                Chat with Emanuel →
                            </Link>
                        </div>
                    </div>
                </div>

                {/* AI Analysis Category */}
                <div>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '1rem',
                        marginBottom: '2rem'
                    }}>
                        <div style={{
                            display: 'inline-block',
                            padding: '0.5rem 1.5rem',
                            background: 'linear-gradient(135deg, rgba(192, 132, 252, 0.2), rgba(129, 140, 248, 0.2))',
                            border: '2px solid rgba(192, 132, 252, 0.5)',
                            borderRadius: '20px',
                            fontSize: '0.9rem',
                            fontWeight: '700',
                            letterSpacing: '0.05em',
                            textTransform: 'uppercase',
                            color: 'var(--accent-color)'
                        }}>
                            🤖 AI Analysis
                        </div>
                        <div style={{
                            flex: 1,
                            height: '2px',
                            background: 'linear-gradient(90deg, rgba(192, 132, 252, 0.5), transparent)'
                        }}></div>
                    </div>

                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                        gap: '2rem'
                    }}>
                        <div className="card" style={{
                            background: 'linear-gradient(135deg, rgba(192, 132, 252, 0.08), rgba(129, 140, 248, 0.05))',
                            borderColor: 'rgba(192, 132, 252, 0.3)'
                        }}>
                            <img src={hanna} alt="Hanna Horizon" className="persona-image" />
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--accent-color)' }}>
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
                                    transition: 'all 0.3s ease'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 6px 20px rgba(192, 132, 252, 0.4)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                Get Insights →
                            </Link>
                        </div>

                        <div className="card" style={{
                            background: 'linear-gradient(135deg, rgba(192, 132, 252, 0.08), rgba(129, 140, 248, 0.05))',
                            borderColor: 'rgba(192, 132, 252, 0.3)'
                        }}>
                            <img src={cora} alt="Cora Carbcount" className="persona-image" />
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--accent-color)' }}>
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
                                    transition: 'all 0.3s ease'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 6px 20px rgba(192, 132, 252, 0.4)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                Get Insights →
                            </Link>
                        </div>

                        <div className="card" style={{
                            background: 'linear-gradient(135deg, rgba(192, 132, 252, 0.08), rgba(129, 140, 248, 0.05))',
                            borderColor: 'rgba(192, 132, 252, 0.3)'
                        }}>
                            <img src={benny} alt="Benny Basal" className="persona-image" />
                            <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', color: 'var(--accent-color)' }}>
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
                                    transition: 'all 0.3s ease'
                                }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.transform = 'translateY(-2px)';
                                    e.currentTarget.style.boxShadow = '0 6px 20px rgba(192, 132, 252, 0.4)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.transform = 'translateY(0)';
                                    e.currentTarget.style.boxShadow = 'none';
                                }}
                            >
                                Get Insights →
                            </Link>
                        </div>
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

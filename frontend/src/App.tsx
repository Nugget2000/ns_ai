import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import EmanuelPage from './pages/EmanuelPage';
import InsightsPage from './pages/InsightsPage';
import FeedbackPage from './pages/FeedbackPage';
import AboutPage from './pages/AboutPage';
import TributePage from './pages/TributePage';
import BackendStatus from './components/BackendStatus';
import DiabetesAIIcon from './components/DiabetesAIIcon';
import emanuel from './assets/emanuel.png';
import hanna from './assets/hanna.png';
import cora from './assets/cora.png';
import benny from './assets/benny.png';

const App: React.FC = () => {
  // Icon component for consistent styling
  const NavIcon: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div style={{
      width: '24px',
      height: '24px',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'rgba(192, 132, 252, 0.2)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      opacity: 0.8
    }}>
      {children}
    </div>
  );

  return (
    <Router>
      <nav style={{
        padding: '1rem 2rem',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: 'rgba(30, 41, 59, 0.5)',
        backdropFilter: 'blur(10px)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <DiabetesAIIcon size={40} interactive={true} />
          <span className="text-pop" style={{ fontSize: '1.5rem', fontWeight: '900' }}>NS AI</span>
          <BackendStatus />
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <Link to="/" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <NavIcon>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
                <polyline points="9 22 9 12 15 12 15 22" />
              </svg>
            </NavIcon>
            Home
          </Link>
          <Link to="/emanuel" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <img src={emanuel} alt="" style={{
              width: '24px',
              height: '24px',
              borderRadius: '50%',
              objectFit: 'cover',
              objectPosition: 'center 20%',
              opacity: 0.8,
              border: '1px solid rgba(255, 255, 255, 0.2)'
            }} />
            Emanuel
          </Link>
          <Link to="/insights" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <div style={{ display: 'flex', marginLeft: '-4px' }}>
              <img src={hanna} alt="" style={{
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                objectFit: 'cover',
                opacity: 0.8,
                border: '1px solid rgba(255, 255, 255, 0.2)',
                marginLeft: '-6px'
              }} />
              <img src={cora} alt="" style={{
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                objectFit: 'cover',
                opacity: 0.8,
                border: '1px solid rgba(255, 255, 255, 0.2)',
                marginLeft: '-6px'
              }} />
              <img src={benny} alt="" style={{
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                objectFit: 'cover',
                opacity: 0.8,
                border: '1px solid rgba(255, 255, 255, 0.2)',
                marginLeft: '-6px'
              }} />
            </div>
            Insights
          </Link>
          <Link to="/feedback" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <NavIcon>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
            </NavIcon>
            Feedback
          </Link>
          <Link to="/about" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <NavIcon>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
            </NavIcon>
            About
          </Link>
          <Link to="/tribute" className="nav-link" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
            <NavIcon>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
              </svg>
            </NavIcon>
            Tribute
          </Link>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/emanuel" element={<EmanuelPage />} />
        <Route path="/insights" element={<InsightsPage />} />
        <Route path="/feedback" element={<FeedbackPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/tribute" element={<TributePage />} />
      </Routes>
    </Router>
  );
};

export default App;

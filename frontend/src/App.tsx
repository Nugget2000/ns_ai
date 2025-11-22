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

const App: React.FC = () => {
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
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/emanuel" className="nav-link">Emanuel</Link>
          <Link to="/insights" className="nav-link">Insights</Link>
          <Link to="/feedback" className="nav-link">Feedback</Link>
          <Link to="/about" className="nav-link">About</Link>
          <Link to="/tribute" className="nav-link">Tribute</Link>
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

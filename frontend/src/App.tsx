import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './pages/LandingPage';
import EmanuelPage from './pages/EmanuelPage';
import InsightsPage from './pages/InsightsPage';
import FeedbackPage from './pages/FeedbackPage';
import AboutPage from './pages/AboutPage';
import TributePage from './pages/TributePage';
import LoginPage from './pages/LoginPage';
import Navbar from './components/Navbar';

const AppContent: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<ProtectedRoute><LandingPage /></ProtectedRoute>} />
        <Route path="/emanuel" element={<ProtectedRoute><EmanuelPage /></ProtectedRoute>} />
        <Route path="/insights" element={<ProtectedRoute><InsightsPage /></ProtectedRoute>} />
        <Route path="/feedback" element={<ProtectedRoute><FeedbackPage /></ProtectedRoute>} />
        <Route path="/about" element={<ProtectedRoute><AboutPage /></ProtectedRoute>} />
        <Route path="/tribute" element={<ProtectedRoute><TributePage /></ProtectedRoute>} />
      </Routes>
    </>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
};

export default App;


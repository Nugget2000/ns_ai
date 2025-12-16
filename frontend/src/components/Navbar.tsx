import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import BackendStatus from './BackendStatus';
import DiabetesAIIcon from './DiabetesAIIcon';
import emanuel from '../assets/emanuel.png';
import hanna from '../assets/hanna.png';
import cora from '../assets/cora.png';
import benny from '../assets/benny.png';
import { Menu, X, Home, MessageSquare, Info, Heart, LogOut, Shield } from 'lucide-react';
import './Navbar.css';

const Navbar: React.FC = () => {
    const { logout, userProfile, firebaseUser } = useAuth();
    const navigate = useNavigate();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const handleLogout = () => {
        logout();
        navigate('/login');
        setIsMobileMenuOpen(false);
    };

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    const closeMobileMenu = () => {
        setIsMobileMenuOpen(false);
    };

    const NavIcon: React.FC<{ children: React.ReactNode }> = ({ children }) => (
        <div className="nav-icon">
            {children}
        </div>
    );

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <DiabetesAIIcon size={40} interactive={true} />
                <span className="text-pop navbar-brand-text">NS AI</span>
                <BackendStatus />
            </div>

            <button className="mobile-menu-button" onClick={toggleMobileMenu}>
                {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>

            <div className="navbar-links">
                <Link to="/" className="nav-link">
                    <NavIcon><Home size={14} /></NavIcon>
                    Home
                </Link>
                <Link to="/emanuel" className="nav-link">
                    <img src={emanuel} alt="" className="nav-image-single" />
                    Emanuel
                </Link>
                <Link to="/insights" className="nav-link">
                    <div className="nav-image-group">
                        <img src={hanna} alt="" className="nav-image" />
                        <img src={cora} alt="" className="nav-image" />
                        <img src={benny} alt="" className="nav-image" />
                    </div>
                    Insights
                </Link>
                <Link to="/feedback" className="nav-link">
                    <NavIcon><MessageSquare size={14} /></NavIcon>
                    Feedback
                </Link>
                <Link to="/about" className="nav-link">
                    <NavIcon><Info size={14} /></NavIcon>
                    About
                </Link>
                <Link to="/tribute" className="nav-link">
                    <NavIcon><Heart size={14} /></NavIcon>
                    Tribute
                </Link>
                {userProfile?.role === 'admin' && (
                    <Link to="/admin" className="nav-link">
                        <NavIcon><Shield size={14} /></NavIcon>
                        Admin
                    </Link>
                )}
                <button onClick={handleLogout} className="logout-button">
                    <LogOut size={14} />
                    {firebaseUser?.displayName?.split(' ')[0] || 'User'}
                </button>
            </div>

            {/* Mobile Menu */}
            <div className={`mobile-menu ${isMobileMenuOpen ? 'open' : ''}`}>
                <Link to="/" className="nav-link" onClick={closeMobileMenu}>
                    <NavIcon><Home size={14} /></NavIcon>
                    Home
                </Link>
                <Link to="/emanuel" className="nav-link" onClick={closeMobileMenu}>
                    <img src={emanuel} alt="" className="nav-image-single" />
                    Emanuel
                </Link>
                <Link to="/insights" className="nav-link" onClick={closeMobileMenu}>
                    <div className="nav-image-group">
                        <img src={hanna} alt="" className="nav-image" />
                        <img src={cora} alt="" className="nav-image" />
                        <img src={benny} alt="" className="nav-image" />
                    </div>
                    Insights
                </Link>
                <Link to="/feedback" className="nav-link" onClick={closeMobileMenu}>
                    <NavIcon><MessageSquare size={14} /></NavIcon>
                    Feedback
                </Link>
                <Link to="/about" className="nav-link" onClick={closeMobileMenu}>
                    <NavIcon><Info size={14} /></NavIcon>
                    About
                </Link>
                <Link to="/tribute" className="nav-link" onClick={closeMobileMenu}>
                    <NavIcon><Heart size={14} /></NavIcon>
                    Tribute
                </Link>
                <button onClick={handleLogout} className="logout-button" style={{ width: '100%', justifyContent: 'center' }}>
                    <LogOut size={14} />
                    {firebaseUser?.displayName?.split(' ')[0] || 'User'}
                </button>
            </div>
        </nav>
    );
};

export default Navbar;

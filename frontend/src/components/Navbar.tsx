import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import DiabetesAIIcon from './DiabetesAIIcon';
import emanuel from '../assets/emanuel.png';
import hanna from '../assets/hanna.png';
import cora from '../assets/cora.png';
import benny from '../assets/benny.png';
import { Menu, X, Home, LogOut, Shield, Settings } from 'lucide-react';
import './Navbar.css';

const Navbar: React.FC = () => {
    const { logout, userProfile, firebaseUser } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
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

    const isActive = (path: string) => location.pathname === path;

    const NavIcon: React.FC<{ children: React.ReactNode }> = ({ children }) => (
        <div className="nav-icon">
            {children}
        </div>
    );

    type NavLink = {
        to: string;
        label: string;
        icon: React.ReactNode | null;
        image: string | null;
        images?: string[];
    };

    const navLinks: NavLink[] = [
        { to: '/', label: 'Home', icon: <Home size={18} />, image: null },
        { to: '/emanuel', label: 'Emanuel', icon: null, image: emanuel },
        { to: '/insights', label: 'Insights', icon: null, image: 'group', images: [hanna, cora, benny] },
        { to: '/settings', label: 'Settings', icon: <Settings size={18} />, image: null },
    ];

    if (userProfile?.role === 'admin') {
        navLinks.push({ to: '/admin', label: 'Admin', icon: <Shield size={18} />, image: null });
    }

    return (
        <nav className="navbar">
            <div className="navbar-container">
                <Link to="/" className="navbar-brand" onClick={closeMobileMenu}>
                    <DiabetesAIIcon size={36} interactive={true} />
                    <span className="navbar-brand-text">NS AI</span>
                </Link>

                <button
                    className={`mobile-menu-button ${isMobileMenuOpen ? 'active' : ''}`}
                    onClick={toggleMobileMenu}
                    aria-label="Toggle menu"
                >
                    {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </button>

                <div className="navbar-links">
                    {navLinks.map((link) => (
                        <Link
                            key={link.to}
                            to={link.to}
                            className={`nav-link ${isActive(link.to) ? 'active' : ''}`}
                        >
                            {link.icon && <NavIcon>{link.icon}</NavIcon>}
                            {link.image === 'group' && (
                                <div className="nav-image-group">
                                    {link.images?.map((img, idx) => (
                                        <img key={idx} src={img} alt="" className="nav-image" />
                                    ))}
                                </div>
                            )}
                            {link.image && link.image !== 'group' && (
                                <img src={link.image} alt="" className="nav-image-single" />
                            )}
                            <span className="nav-link-text">{link.label}</span>
                        </Link>
                    ))}
                    <button onClick={handleLogout} className="logout-button">
                        <LogOut size={18} />
                        <span className="logout-text">{firebaseUser?.displayName?.split(' ')[0] || 'User'}</span>
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            <div className={`mobile-menu ${isMobileMenuOpen ? 'open' : ''}`}>
                <div className="mobile-menu-content">
                    {navLinks.map((link) => (
                        <Link
                            key={link.to}
                            to={link.to}
                            className={`nav-link ${isActive(link.to) ? 'active' : ''}`}
                            onClick={closeMobileMenu}
                        >
                            {link.icon && <NavIcon>{link.icon}</NavIcon>}
                            {link.image === 'group' && (
                                <div className="nav-image-group">
                                    {link.images?.map((img, idx) => (
                                        <img key={idx} src={img} alt="" className="nav-image" />
                                    ))}
                                </div>
                            )}
                            {link.image && link.image !== 'group' && (
                                <img src={link.image} alt="" className="nav-image-single" />
                            )}
                            <span className="nav-link-text">{link.label}</span>
                        </Link>
                    ))}
                    <button
                        onClick={handleLogout}
                        className="logout-button mobile-logout"
                    >
                        <LogOut size={18} />
                        <span className="logout-text">{firebaseUser?.displayName?.split(' ')[0] || 'User'}</span>
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

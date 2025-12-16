import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';


interface ProtectedRouteProps {
    children: React.ReactNode;
    requiredRole?: 'admin' | 'user' | 'pending'; // hierarchy: admin > user > pending
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
    const { isAuthenticated, userProfile } = useAuth();

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (requiredRole && userProfile) {
        if (requiredRole === 'admin' && userProfile.role !== 'admin') {
            return <div>Access Denied. Admins only.</div>; // Simple fallback
        }
        if (requiredRole === 'user' && userProfile.role === 'pending') {
            return <div>Access Denied. Account pending approval.</div>;
        }
    }

    // If userProfile is loading, we might show loading? 
    // But AuthContext handles initial loading. 
    // If api call for profile is slower than auth?
    // userProfile might be null initially even if authenticated if fetch is async inside useEffect.
    // We should probably check if userProfile is loaded if we require a role.
    if (isAuthenticated && !userProfile && requiredRole) {
        return <div>Loading profile...</div>;
    }

    return <>{children}</>;
};

export default ProtectedRoute;

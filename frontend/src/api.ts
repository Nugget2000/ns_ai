import { auth } from './lib/firebase';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getAuthHeaders = async () => {
    const token = await auth.currentUser?.getIdToken();
    return token ? {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    } : {
        'Content-Type': 'application/json'
    };
};

export interface HealthResponse {
    status: string;
}

export interface VersionResponse {
    version: string;
}

export interface PageLoadResponse {
    count: number;
}

export const getHealth = async (): Promise<HealthResponse> => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE_URL}/health`, { headers });
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Unable to connect to backend');
    }
};

export const getVersion = async (): Promise<VersionResponse> => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE_URL}/version`, { headers });
        if (!response.ok) {
            throw new Error('Version check failed');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Unable to fetch version');
    }
};

export const getPageLoad = async (): Promise<PageLoadResponse> => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE_URL}/page-load`, { headers });
        if (!response.ok) {
            throw new Error('Page load tracking failed');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Unable to fetch page load count');
    }
};

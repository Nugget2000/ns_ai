import { auth } from './lib/firebase';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const getAuthHeaders = async (): Promise<HeadersInit> => {
    const token = await auth.currentUser?.getIdToken();
    if (token) {
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };
    }
    return {
        'Content-Type': 'application/json'
    };
};


export interface User {
    uid: string;
    email: string;
    role: 'pending' | 'user' | 'admin';
    created_at?: string;
    last_login?: string;
}

export interface HealthResponse {
    status: string;
}

export interface VersionResponse {
    version: string;
}

export interface PageLoadResponse {
    count: number;
}

export interface FileStoreInfoResponse {
    size_mb: number;
    upload_date: string | null;
    display_name: string | null;
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

export const getMe = async (): Promise<User> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/users/me`, { headers });
    if (!response.ok) {
        throw new Error('Failed to fetch user profile');
    }
    return await response.json();
};

export const getUsers = async (): Promise<User[]> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/users/`, { headers });
    if (!response.ok) {
        throw new Error('Failed to fetch users');
    }
    return await response.json();
};

export const updateUserRole = async (uid: string, role: string): Promise<User> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/users/${uid}/role`, {
        method: 'PUT',
        headers: {
            ...headers as Record<string, string>,
        },
        body: JSON.stringify({ role })
    });
    if (!response.ok) {
        throw new Error('Failed to update user role');
    }
    return await response.json();
};

export const getFileStoreInfo = async (): Promise<FileStoreInfoResponse[]> => {
    try {
        const headers = await getAuthHeaders();
        const response = await fetch(`${API_BASE_URL}/emanuel/file-store-info`, { headers });
        if (!response.ok) {
            throw new Error('Failed to fetch file store info');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Unable to fetch file store info');
    }
};

const API_BASE_URL = 'http://localhost:8085';

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
        const response = await fetch(`${API_BASE_URL}/health`);
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
        const response = await fetch(`${API_BASE_URL}/version`);
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
        const response = await fetch(`${API_BASE_URL}/page-load`);
        if (!response.ok) {
            throw new Error('Page load tracking failed');
        }
        return await response.json();
    } catch (error) {
        throw new Error('Unable to fetch page load count');
    }
};

const API_BASE_URL = 'http://localhost:8000';

export interface HealthResponse {
    status: string;
}

export interface VersionResponse {
    version: string;
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

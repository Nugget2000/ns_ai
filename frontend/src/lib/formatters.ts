import { auth } from './firebase';

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

// ==================== User Settings ====================

export type GlucoseUnit = 'mg/dL' | 'mmol/L';

export interface UserSettings {
    locale: string;
    timezone: string;
    glucose_unit: GlucoseUnit;
}

export interface UserSettingsUpdate {
    locale?: string;
    timezone?: string;
    glucose_unit?: GlucoseUnit;
}

export const getUserSettings = async (): Promise<UserSettings> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/users/me/settings`, { headers });
    if (!response.ok) {
        throw new Error('Failed to fetch user settings');
    }
    return await response.json();
};

export const updateUserSettings = async (settings: UserSettingsUpdate): Promise<UserSettings> => {
    const headers = await getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}/users/me/settings`, {
        method: 'PUT',
        headers: {
            ...headers as Record<string, string>,
        },
        body: JSON.stringify(settings)
    });
    if (!response.ok) {
        throw new Error('Failed to update user settings');
    }
    return await response.json();
};


// ==================== Formatting Utilities ====================

/**
 * Format a date according to locale and timezone.
 * For Swedish (sv-SE): yyyy-mm-dd
 */
export const formatDate = (
    date: Date | string | null | undefined,
    locale: string = 'en-US',
    timezone: string = 'UTC'
): string => {
    if (!date) return '-';
    const d = typeof date === 'string' ? new Date(date) : date;

    return d.toLocaleDateString(locale, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        timeZone: timezone
    });
};

/**
 * Format a date with time according to locale and timezone.
 * For Swedish (sv-SE): yyyy-mm-dd HH:mm
 */
export const formatDateTime = (
    date: Date | string | null | undefined,
    locale: string = 'en-US',
    timezone: string = 'UTC'
): string => {
    if (!date) return '-';
    const d = typeof date === 'string' ? new Date(date) : date;

    return d.toLocaleString(locale, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZone: timezone
    });
};

/**
 * Format a number according to locale.
 * For Swedish (sv-SE): space as thousand separator, comma for decimal
 */
export const formatNumber = (
    value: number | null | undefined,
    locale: string = 'en-US',
    decimals: number = 0
): string => {
    if (value === null || value === undefined) return '-';

    return value.toLocaleString(locale, {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
};

/**
 * Format a blood glucose value, converting units if needed.
 * mg/dL to mmol/L: divide by 18
 */
export const formatGlucose = (
    value: number | null | undefined,
    targetUnit: GlucoseUnit = 'mg/dL',
    locale: string = 'en-US',
    sourceUnit: GlucoseUnit = 'mg/dL'
): string => {
    if (value === null || value === undefined) return '-';

    let displayValue = value;

    // Convert if needed
    if (sourceUnit === 'mg/dL' && targetUnit === 'mmol/L') {
        displayValue = value / 18;
    } else if (sourceUnit === 'mmol/L' && targetUnit === 'mg/dL') {
        displayValue = value * 18;
    }

    // mmol/L typically uses 1 decimal, mg/dL uses 0
    const decimals = targetUnit === 'mmol/L' ? 1 : 0;

    return formatNumber(displayValue, locale, decimals);
};

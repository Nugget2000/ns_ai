import React, { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { useAuth } from './AuthContext';
import {
    getUserSettings,
    updateUserSettings as updateSettingsApi,
    formatDate as formatDateUtil,
    formatDateTime as formatDateTimeUtil,
    formatNumber as formatNumberUtil,
    formatGlucose as formatGlucoseUtil,
    type UserSettings,
    type UserSettingsUpdate,
    type GlucoseUnit
} from '../lib/formatters';

interface SettingsContextType {
    settings: UserSettings;
    loading: boolean;
    updateSettings: (updates: UserSettingsUpdate) => Promise<void>;
    // Formatting utilities that use current settings
    formatDate: (date: Date | string | null | undefined) => string;
    formatDateTime: (date: Date | string | null | undefined) => string;
    formatNumber: (value: number | null | undefined, decimals?: number) => string;
    formatGlucose: (value: number | null | undefined, sourceUnit?: GlucoseUnit) => string;
}

const defaultSettings: UserSettings = {
    locale: 'en-US',
    timezone: 'UTC',
    glucose_unit: 'mg/dL'
};

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const { isAuthenticated, firebaseUser } = useAuth();
    const [settings, setSettings] = useState<UserSettings>(defaultSettings);
    const [loading, setLoading] = useState(true);

    // Fetch settings when user is authenticated
    useEffect(() => {
        const fetchSettings = async () => {
            if (isAuthenticated && firebaseUser) {
                try {
                    const userSettings = await getUserSettings();
                    setSettings(userSettings);
                } catch (error) {
                    console.error('Failed to fetch user settings, using defaults:', error);
                    setSettings(defaultSettings);
                }
            } else {
                setSettings(defaultSettings);
            }
            setLoading(false);
        };

        fetchSettings();
    }, [isAuthenticated, firebaseUser]);

    const updateSettings = useCallback(async (updates: UserSettingsUpdate) => {
        try {
            const updatedSettings = await updateSettingsApi(updates);
            setSettings(updatedSettings);
        } catch (error) {
            console.error('Failed to update settings:', error);
            throw error;
        }
    }, []);

    // Formatting utilities bound to current settings
    const formatDate = useCallback(
        (date: Date | string | null | undefined) =>
            formatDateUtil(date, settings.locale, settings.timezone),
        [settings.locale, settings.timezone]
    );

    const formatDateTime = useCallback(
        (date: Date | string | null | undefined) =>
            formatDateTimeUtil(date, settings.locale, settings.timezone),
        [settings.locale, settings.timezone]
    );

    const formatNumber = useCallback(
        (value: number | null | undefined, decimals: number = 0) =>
            formatNumberUtil(value, settings.locale, decimals),
        [settings.locale]
    );

    const formatGlucose = useCallback(
        (value: number | null | undefined, sourceUnit: GlucoseUnit = 'mg/dL') =>
            formatGlucoseUtil(value, settings.glucose_unit, settings.locale, sourceUnit),
        [settings.glucose_unit, settings.locale]
    );

    const value: SettingsContextType = {
        settings,
        loading,
        updateSettings,
        formatDate,
        formatDateTime,
        formatNumber,
        formatGlucose
    };

    return (
        <SettingsContext.Provider value={value}>
            {children}
        </SettingsContext.Provider>
    );
};

export const useSettings = (): SettingsContextType => {
    const context = useContext(SettingsContext);
    if (!context) {
        throw new Error('useSettings must be used within a SettingsProvider');
    }
    return context;
};

// Re-export types for convenience
export type { UserSettings, UserSettingsUpdate, GlucoseUnit };

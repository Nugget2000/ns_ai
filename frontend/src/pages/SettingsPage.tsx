import React, { useState, useEffect } from 'react';
import { useSettings, type GlucoseUnit } from '../contexts/SettingsContext';
import { Settings, Globe, Clock, Droplet, Save, Check } from 'lucide-react';
import './SettingsPage.css';

// Common locales with their display names
const LOCALES = [
    { value: 'en-US', label: 'English (US)', datePreview: '01/31/2026, 10:30 PM', numberPreview: '1,234.56' },
    { value: 'en-GB', label: 'English (UK)', datePreview: '31/01/2026, 22:30', numberPreview: '1,234.56' },
    { value: 'sv-SE', label: 'Svenska (Swedish)', datePreview: '2026-01-31 22:30', numberPreview: '1 234,56' },
    { value: 'de-DE', label: 'Deutsch (German)', datePreview: '31.01.2026, 22:30', numberPreview: '1.234,56' },
    { value: 'fr-FR', label: 'Français (French)', datePreview: '31/01/2026 22:30', numberPreview: '1 234,56' },
    { value: 'es-ES', label: 'Español (Spanish)', datePreview: '31/01/2026, 22:30', numberPreview: '1.234,56' },
    { value: 'nb-NO', label: 'Norsk (Norwegian)', datePreview: '31.01.2026, 22:30', numberPreview: '1 234,56' },
    { value: 'da-DK', label: 'Dansk (Danish)', datePreview: '31.01.2026 22.30', numberPreview: '1.234,56' },
    { value: 'fi-FI', label: 'Suomi (Finnish)', datePreview: '31.1.2026 klo 22.30', numberPreview: '1 234,56' },
];

// Common timezones
const TIMEZONES = [
    { value: 'UTC', label: 'UTC' },
    { value: 'Europe/Stockholm', label: 'Stockholm (CET/CEST)' },
    { value: 'Europe/London', label: 'London (GMT/BST)' },
    { value: 'Europe/Paris', label: 'Paris (CET/CEST)' },
    { value: 'Europe/Berlin', label: 'Berlin (CET/CEST)' },
    { value: 'Europe/Helsinki', label: 'Helsinki (EET/EEST)' },
    { value: 'Europe/Oslo', label: 'Oslo (CET/CEST)' },
    { value: 'Europe/Copenhagen', label: 'Copenhagen (CET/CEST)' },
    { value: 'America/New_York', label: 'New York (EST/EDT)' },
    { value: 'America/Chicago', label: 'Chicago (CST/CDT)' },
    { value: 'America/Denver', label: 'Denver (MST/MDT)' },
    { value: 'America/Los_Angeles', label: 'Los Angeles (PST/PDT)' },
    { value: 'Asia/Tokyo', label: 'Tokyo (JST)' },
    { value: 'Asia/Shanghai', label: 'Shanghai (CST)' },
    { value: 'Australia/Sydney', label: 'Sydney (AEST/AEDT)' },
];

const GLUCOSE_UNITS: { value: GlucoseUnit; label: string; description: string }[] = [
    { value: 'mg/dL', label: 'mg/dL', description: 'Milligrams per deciliter (US standard)' },
    { value: 'mmol/L', label: 'mmol/L', description: 'Millimoles per liter (International standard)' },
];

const SettingsPage: React.FC = () => {
    const { settings, updateSettings, loading } = useSettings();

    const [locale, setLocale] = useState(settings.locale);
    const [timezone, setTimezone] = useState(settings.timezone);
    const [glucoseUnit, setGlucoseUnit] = useState<GlucoseUnit>(settings.glucose_unit);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Update local state when settings load
    useEffect(() => {
        if (!loading) {
            setLocale(settings.locale);
            setTimezone(settings.timezone);
            setGlucoseUnit(settings.glucose_unit);
        }
    }, [settings, loading]);

    const hasChanges =
        locale !== settings.locale ||
        timezone !== settings.timezone ||
        glucoseUnit !== settings.glucose_unit;

    const handleSave = async () => {
        setSaving(true);
        setError(null);
        try {
            await updateSettings({
                locale,
                timezone,
                glucose_unit: glucoseUnit
            });
            setSaved(true);
            setTimeout(() => setSaved(false), 2000);
        } catch (err) {
            setError('Failed to save settings. Please try again.');
        } finally {
            setSaving(false);
        }
    };

    // Preview values for current selections
    const previewDate = new Date();
    const previewNumber = 1234.56;
    const previewGlucose = 120; // mg/dL

    if (loading) {
        return (
            <div className="settings-page">
                <div className="settings-loading">Loading settings...</div>
            </div>
        );
    }

    return (
        <div className="settings-page">
            <div className="settings-container">
                <header className="settings-header">
                    <Settings size={32} className="settings-icon" />
                    <div>
                        <h1>Settings</h1>
                        <p>Customize your display preferences</p>
                    </div>
                </header>

                <div className="settings-sections">
                    {/* Locale Section */}
                    <section className="settings-section">
                        <div className="section-header">
                            <Globe size={20} />
                            <h2>Locale & Format</h2>
                        </div>
                        <p className="section-description">
                            Choose how dates and numbers are displayed throughout the app.
                        </p>

                        <div className="setting-field">
                            <label htmlFor="locale-select">Display Language/Format</label>
                            <select
                                id="locale-select"
                                value={locale}
                                onChange={(e) => setLocale(e.target.value)}
                            >
                                {LOCALES.map((loc) => (
                                    <option key={loc.value} value={loc.value}>
                                        {loc.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="preview-box">
                            <div className="preview-row">
                                <span className="preview-label">Date & Time:</span>
                                <span className="preview-value">
                                    {previewDate.toLocaleString(locale, {
                                        year: 'numeric',
                                        month: '2-digit',
                                        day: '2-digit',
                                        hour: '2-digit',
                                        minute: '2-digit',
                                        timeZone: timezone
                                    })}
                                </span>
                            </div>
                            <div className="preview-row">
                                <span className="preview-label">Number:</span>
                                <span className="preview-value">
                                    {previewNumber.toLocaleString(locale, {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    })}
                                </span>
                            </div>
                        </div>
                    </section>

                    {/* Timezone Section */}
                    <section className="settings-section">
                        <div className="section-header">
                            <Clock size={20} />
                            <h2>Timezone</h2>
                        </div>
                        <p className="section-description">
                            Set your timezone for accurate time display.
                        </p>

                        <div className="setting-field">
                            <label htmlFor="timezone-select">Timezone</label>
                            <select
                                id="timezone-select"
                                value={timezone}
                                onChange={(e) => setTimezone(e.target.value)}
                            >
                                {TIMEZONES.map((tz) => (
                                    <option key={tz.value} value={tz.value}>
                                        {tz.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="preview-box">
                            <div className="preview-row">
                                <span className="preview-label">Current time:</span>
                                <span className="preview-value">
                                    {new Date().toLocaleTimeString(locale, {
                                        hour: '2-digit',
                                        minute: '2-digit',
                                        second: '2-digit',
                                        timeZone: timezone
                                    })}
                                </span>
                            </div>
                        </div>
                    </section>

                    {/* Blood Glucose Unit Section */}
                    <section className="settings-section">
                        <div className="section-header">
                            <Droplet size={20} />
                            <h2>Blood Glucose Unit</h2>
                        </div>
                        <p className="section-description">
                            Choose how blood glucose values are displayed.
                        </p>

                        <div className="glucose-unit-options">
                            {GLUCOSE_UNITS.map((unit) => (
                                <label
                                    key={unit.value}
                                    className={`glucose-unit-option ${glucoseUnit === unit.value ? 'selected' : ''}`}
                                >
                                    <input
                                        type="radio"
                                        name="glucose-unit"
                                        value={unit.value}
                                        checked={glucoseUnit === unit.value}
                                        onChange={(e) => setGlucoseUnit(e.target.value as GlucoseUnit)}
                                    />
                                    <div className="unit-content">
                                        <span className="unit-label">{unit.label}</span>
                                        <span className="unit-description">{unit.description}</span>
                                    </div>
                                </label>
                            ))}
                        </div>

                        <div className="preview-box">
                            <div className="preview-row">
                                <span className="preview-label">Example glucose:</span>
                                <span className="preview-value glucose-value">
                                    {glucoseUnit === 'mmol/L'
                                        ? (previewGlucose / 18).toLocaleString(locale, { minimumFractionDigits: 1, maximumFractionDigits: 1 })
                                        : previewGlucose.toLocaleString(locale)
                                    } {glucoseUnit}
                                </span>
                            </div>
                        </div>
                    </section>
                </div>

                {/* Save Button */}
                <div className="settings-actions">
                    {error && <div className="settings-error">{error}</div>}
                    <button
                        className={`save-button ${saved ? 'saved' : ''} ${!hasChanges ? 'disabled' : ''}`}
                        onClick={handleSave}
                        disabled={saving || !hasChanges}
                    >
                        {saving ? (
                            <>Saving...</>
                        ) : saved ? (
                            <>
                                <Check size={18} />
                                Saved!
                            </>
                        ) : (
                            <>
                                <Save size={18} />
                                Save Changes
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;

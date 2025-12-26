import React, { useState, useEffect } from 'react';
import { getVersion, getPageLoad } from '../api';
import './Footer.css';

const Footer: React.FC = () => {
    const [version, setVersion] = useState<string>('');
    const [pageCount, setPageCount] = useState<number | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [versionData, pageLoadData] = await Promise.all([
                    getVersion(),
                    getPageLoad(),
                ]);
                setVersion(versionData.version);
                setPageCount(pageLoadData.count);
            } catch (error) {
                console.error('Failed to fetch footer data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <footer className="app-footer">
            <div className="footer-content">
                <div className="footer-section">
                    {version && (
                        <div className="footer-item">
                            <span className="footer-value">v{version}</span>
                        </div>
                    )}
                    {pageCount !== null && (
                        <div className="footer-item">
                            <span className="footer-label">views</span>
                            <span className="footer-value">{pageCount.toLocaleString()}</span>
                        </div>
                    )}
                </div>
            </div>
        </footer>
    );
};

export default Footer;


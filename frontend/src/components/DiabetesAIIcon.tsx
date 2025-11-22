import React, { useState, useEffect, useRef } from 'react';

interface DiabetesAIIconProps {
    size?: number;
    interactive?: boolean;
}

const DiabetesAIIcon: React.FC<DiabetesAIIconProps> = ({ size = 120, interactive = true }) => {
    const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
    const iconRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!interactive) return;

        const handleMouseMove = (e: MouseEvent) => {
            if (iconRef.current) {
                const rect = iconRef.current.getBoundingClientRect();
                const iconCenterX = rect.left + rect.width / 2;
                const iconCenterY = rect.top + rect.height / 2;

                // Calculate distance from icon center
                const deltaX = e.clientX - iconCenterX;
                const deltaY = e.clientY - iconCenterY;

                // Normalize to -1 to 1 range with max distance of 500px
                const maxDistance = 500;
                const normalizedX = Math.max(-1, Math.min(1, deltaX / maxDistance));
                const normalizedY = Math.max(-1, Math.min(1, deltaY / maxDistance));

                setMousePos({ x: normalizedX, y: normalizedY });
            }
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, [interactive]);

    // Calculate rotation based on mouse position
    const rotateX = interactive ? -mousePos.y * 20 : 0;
    const rotateY = interactive ? mousePos.x * 20 : 0;
    const rotateZ = interactive ? mousePos.x * 5 : 0;

    return (
        <div
            ref={iconRef}
            style={{
                width: `${size}px`,
                height: `${size}px`,
                perspective: '1000px',
                cursor: interactive ? 'pointer' : 'default',
                display: 'inline-block'
            }}
        >
            <div
                style={{
                    width: '100%',
                    height: '100%',
                    transition: interactive ? 'transform 0.3s ease-out' : 'none',
                    transform: `rotateX(${rotateX}deg) rotateY(${rotateY}deg) rotateZ(${rotateZ}deg)`,
                    transformStyle: 'preserve-3d'
                }}
            >
                <svg
                    width={size}
                    height={size}
                    viewBox="0 0 120 120"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    style={{ filter: 'drop-shadow(0 0 20px rgba(129, 140, 248, 0.5))' }}
                >
                    {/* Blood drop outline - diabetes symbol */}
                    <path
                        d="M60 20 C60 20, 40 45, 40 65 C40 78, 48 88, 60 88 C72 88, 80 78, 80 65 C80 45, 60 20, 60 20 Z"
                        stroke="url(#grad1)"
                        strokeWidth="2.5"
                        fill="none"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    {/* Neural network nodes - AI symbol */}
                    <circle cx="60" cy="45" r="4" fill="url(#grad2)" opacity="0.9" />
                    <circle cx="50" cy="58" r="3.5" fill="url(#grad3)" opacity="0.8" />
                    <circle cx="70" cy="58" r="3.5" fill="url(#grad3)" opacity="0.8" />
                    <circle cx="45" cy="70" r="3" fill="url(#grad2)" opacity="0.7" />
                    <circle cx="60" cy="72" r="3" fill="url(#grad2)" opacity="0.7" />
                    <circle cx="75" cy="70" r="3" fill="url(#grad2)" opacity="0.7" />

                    {/* Neural connections */}
                    <line x1="60" y1="45" x2="50" y2="58" stroke="url(#grad2)" strokeWidth="1.5" opacity="0.6" />
                    <line x1="60" y1="45" x2="70" y2="58" stroke="url(#grad2)" strokeWidth="1.5" opacity="0.6" />
                    <line x1="50" y1="58" x2="45" y2="70" stroke="url(#grad3)" strokeWidth="1.5" opacity="0.5" />
                    <line x1="50" y1="58" x2="60" y2="72" stroke="url(#grad3)" strokeWidth="1.5" opacity="0.5" />
                    <line x1="70" y1="58" x2="60" y2="72" stroke="url(#grad3)" strokeWidth="1.5" opacity="0.5" />
                    <line x1="70" y1="58" x2="75" y2="70" stroke="url(#grad3)" strokeWidth="1.5" opacity="0.5" />

                    {/* Circuit board pattern - tech symbol */}
                    <path
                        d="M48 35 L52 35 M52 35 L52 40 M68 35 L72 35 M68 35 L68 40"
                        stroke="url(#grad1)"
                        strokeWidth="1.5"
                        opacity="0.5"
                        strokeLinecap="round"
                    />

                    {/* Data points representing glucose readings */}
                    <circle cx="35" cy="55" r="1.5" fill="url(#grad3)" opacity="0.6" />
                    <circle cx="38" cy="62" r="1.5" fill="url(#grad3)" opacity="0.6" />
                    <circle cx="82" cy="62" r="1.5" fill="url(#grad3)" opacity="0.6" />
                    <circle cx="85" cy="55" r="1.5" fill="url(#grad3)" opacity="0.6" />

                    {/* Gradient definitions */}
                    <defs>
                        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#818cf8" />
                            <stop offset="50%" stopColor="#38bdf8" />
                            <stop offset="100%" stopColor="#c084fc" />
                        </linearGradient>
                        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#38bdf8" />
                            <stop offset="100%" stopColor="#818cf8" />
                        </linearGradient>
                        <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stopColor="#c084fc" />
                            <stop offset="50%" stopColor="#818cf8" />
                            <stop offset="100%" stopColor="#38bdf8" />
                        </linearGradient>
                    </defs>
                </svg>
            </div>
        </div>
    );
};

export default DiabetesAIIcon;

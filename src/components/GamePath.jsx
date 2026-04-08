import React, { useRef, useEffect, useState } from 'react';
import { Star } from 'lucide-react';

const GamePath = ({ totalSteps = 10, currentStep, stars = [] }) => {

    const pathPoints = [
        { x: 10, y: 80 },
        { x: 20, y: 65 },
        { x: 35, y: 55 },
        { x: 50, y: 50 },
        { x: 65, y: 45 },
        { x: 80, y: 30 },
        { x: 90, y: 15 },
        { x: 80, y: 10 },
        { x: 60, y: 15 },
        { x: 90, y: 80 }
    ];

    const getPoint = (i, total) => {
        const t = i / (total - 1);
        const x = 10 + (t * 80);

        const y = 50 + Math.sin(t * Math.PI * 2) * 20;
        return { x, y };
    };

    const points = Array.from({ length: totalSteps }).map((_, i) => getPoint(i, totalSteps));

    const svgPath = points.reduce((acc, p, i) => {
        if (i === 0) return `M ${p.x} ${p.y} `;

        return `${acc} L ${p.x} ${p.y} `;
    }, "");

    return (
        <div style={{
            height: '100px', 
            width: '100%',
            maxWidth: '800px',
            marginBottom: '0.5rem',
            position: 'relative',
            margin: '0 auto'
        }}>
            <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', overflow: 'visible', zIndex: 0 }} viewBox="0 0 100 100" preserveAspectRatio="none">
                {}
                <path d={svgPath} fill="none" stroke="rgba(0,0,0,0.1)" strokeWidth="4" strokeLinecap="round" transform="translate(0, 2)" />
                {}
                <path d={svgPath} fill="none" stroke="white" strokeWidth="4" strokeLinecap="round" strokeDasharray="1 2" />
            </svg>

            {}
            {points.map((p, index) => {
                const isBefore = index < currentStep;
                const isCurrent = index === currentStep;
                const hasStar = stars[index];

                return (
                    <div key={index} style={{
                        position: 'absolute',
                        left: `${p.x}% `,
                        top: `${p.y}% `,
                        transform: 'translate(-50%, -50%)',
                        zIndex: 10 + index
                    }}>
                        {}
                        <div className="step-node" style={{
                            width: '35px', height: '35px', 
                            background: isBefore ? (hasStar ? '#fcd34d' : 'rgba(255,255,255,0.1)') : 'rgba(255,255,255,0.1)',
                            borderRadius: '50%',
                            boxShadow: isBefore && hasStar ? '0 0 10px #fcd34d' : 'none',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transition: 'all 0.4s',
                            transform: isCurrent ? 'scale(1.2)' : 'scale(1)',
                            border: isBefore && hasStar ? '2px solid #fff' : '1px dashed rgba(255,255,255,0.4)'
                        }}>
                            {hasStar && <Star size={18} fill="#b45309" color="#b45309" />}
                            {}
                            {!isBefore && !isCurrent && <span style={{ color: '#94a3b8', fontSize: '1rem', fontWeight: 'bold' }}>{index + 1}</span>}
                        </div>
                    </div>
                );
            })}

            {}
            <div style={{
                position: 'absolute',
                left: `${points[currentStep] ? points[currentStep].x : 0}% `,
                top: `${points[currentStep] ? points[currentStep].y : 0}% `,
                width: '60px',
                height: '60px',
                transition: 'all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
                zIndex: 100,
                pointerEvents: 'none'
            }}>
                <img
                    src={`${import.meta.env.BASE_URL}assets/images/spongebob_fixed.png`}
                    alt="Player"
                    style={{
                        width: '100%', height: '100%', objectFit: 'contain',
                        filter: 'drop-shadow(0 10px 5px rgba(0,0,0,0.3))',
                        animation: 'bounce 2s infinite'
                    }}
                />
            </div>
            <style>{`
                @media (max-width: 600px) {
                    .step-node { width: 30px !important; height: 30px !important; }
                }
            `}</style>
        </div>
    );
};

export default GamePath;

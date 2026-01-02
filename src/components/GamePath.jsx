import React, { useRef, useEffect, useState } from 'react';
import { Star } from 'lucide-react';

const GamePath = ({ totalSteps = 10, currentStep, stars = [] }) => {
    // We want a curved path like a level map (e.g. Candy Crush saga style).
    // We can use an SVG path for the line, and position elements along it.

    // Hardcoded curve points for 10 steps (S-shape)
    // Coords are percent [x, y] relative to container
    // Designed for desktop/tablet landscape mainly
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
        { x: 90, y: 80 } // Goal (Chest?) or final spot
    ];

    // Better generated curve: a sine wave or simple arc
    // Let's generate points dynamically for smoothness
    const getPoint = (i, total) => {
        const t = i / (total - 1);
        const x = 10 + (t * 80); // 10% to 90% width
        // Add a sine wave for Y
        const y = 50 + Math.sin(t * Math.PI * 2) * 20;
        return { x, y };
    };

    const points = Array.from({ length: totalSteps }).map((_, i) => getPoint(i, totalSteps));

    // Calculate SVG path string
    const svgPath = points.reduce((acc, p, i) => {
        if (i === 0) return `M ${p.x} ${p.y} `;
        // Simple line for now or quadratic
        // let's try catmull-rom or just straight lines with rounded caps in CSS is easier,
        // but for SVG 'L' is straight. Let's do a curve.
        // Quick cubic bezier estimation or just L for reliability first.
        return `${acc} L ${p.x} ${p.y} `;
    }, "");

    return (
        <div style={{
            margin: '0.5rem auto', /* Reduced margin */
            position: 'relative',
            height: 'clamp(120px, 25vh, 200px)', /* Reduced max height */
            width: '100%',
            maxWidth: '800px',
        }}>

            {/* SVG Path Background */}
            <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', overflow: 'visible', zIndex: 0 }} viewBox="0 0 100 100" preserveAspectRatio="none">
                {/* Shadow Path */}
                <path d={svgPath} fill="none" stroke="rgba(0,0,0,0.1)" strokeWidth="4" strokeLinecap="round" transform="translate(0, 2)" />
                {/* Main Path */}
                <path d={svgPath} fill="none" stroke="white" strokeWidth="4" strokeLinecap="round" strokeDasharray="1 2" />
            </svg>

            {/* Steps */}
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
                        {/* 3D Stone/Platform - Now Transparent/Glassy per request */}
                        <div className="step-node" style={{
                            width: '40px', height: '40px', /* Base size, will be overridden by CSS if we add class, or we can use clamp here */
                            // Only show Gold background if star is there, otherwise transparent/glass
                            background: isBefore ? (hasStar ? '#fcd34d' : 'rgba(255,255,255,0.1)') : 'rgba(255,255,255,0.1)',
                            borderRadius: '50%',
                            boxShadow: isBefore && hasStar ? '0 0 10px #fcd34d' : 'none', // Only glow if star
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            transition: 'all 0.4s',
                            transform: isCurrent ? 'scale(1.1) translateY(-5px)' : 'scale(1)',
                            border: isBefore && hasStar ? '2px solid #fff' : '1px dashed rgba(255,255,255,0.3)'
                        }}>
                            {hasStar && <Star size={20} fill="#b45309" color="#b45309" />}
                            {/* Number for future steps */}
                            {!isBefore && !isCurrent && <span style={{ color: '#94a3b8', fontSize: '0.8rem', fontWeight: 'bold' }}>{index + 1}</span>}
                        </div>
                    </div>
                );
            })}

            {/* SpongeBob Character */}
            <div style={{
                position: 'absolute',
                left: `${points[currentStep] ? points[currentStep].x : 0}% `,
                top: `${points[currentStep] ? points[currentStep].y : 0}% `,
                transform: 'translate(-50%, -90%)', // Sit on top
                width: '80px',
                height: '80px',
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

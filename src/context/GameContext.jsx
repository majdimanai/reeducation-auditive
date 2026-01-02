import React, { createContext, useState, useContext } from 'react';

const GameContext = createContext();

export const GameProvider = ({ children }) => {
    const [config, setConfig] = useState({
        activity: null, // 1 or 2
        vocabularyLevel: 'base', // 'base' or 'rich'
        noise: false,
        noiseType: 'white', // 'white', 'background', 'speech'
        contrast: null, // e.g., 'b-m' for Act 1
    });

    const [score, setScore] = useState(0);

    const resetGame = () => {
        setScore(0);
    };

    return (
        <GameContext.Provider value={{ config, setConfig, score, setScore, resetGame }}>
            {children}
        </GameContext.Provider>
    );
};

export const useGame = () => useContext(GameContext);

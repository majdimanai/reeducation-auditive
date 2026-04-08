import React, { createContext, useState, useContext } from 'react';

const GameContext = createContext();

export const GameProvider = ({ children }) => {
    const [config, setConfig] = useState({
        activity: null,
        vocabularyLevel: 'base',
        noise: false,
        noiseType: 'white',
        contrast: null,
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

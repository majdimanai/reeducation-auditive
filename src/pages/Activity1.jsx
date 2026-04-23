import React, { useState, useEffect } from 'react';
import { useGame } from '../context/GameContext';
import { VOCABULARY } from '../data/vocabulary';
import itemsImages from '../data/items_images.json';
import GamePath from '../components/GamePath';
import { useNavigate } from 'react-router-dom';
import { Volume2, AlertCircle, CheckCircle, VolumeX, Volume1, Plus, Minus, Settings, XCircle } from 'lucide-react';

const Activity1 = () => {
    const { config, setScore, score } = useGame();
    const navigate = useNavigate();

    const [items, setItems] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [feedback, setFeedback] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);

    const [attempts, setAttempts] = useState(0);
    const [stars, setStars] = useState([]);

    const [noiseVolume, setNoiseVolume] = useState(0);
    const [noiseType, setNoiseType] = useState('background');
    const [showSettings, setShowSettings] = useState(false);

    const [gameState, setGameState] = useState('intro');

    useEffect(() => {
        if (!config.contrast) {

            navigate('/');
            return;
        }

        const contrastData = VOCABULARY.discrimination.base[config.contrast] || VOCABULARY.discrimination.rich[config.contrast];
        if (!contrastData) return;

        const allWords = contrastData.words;

        const shuffled = [...allWords].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 10);
        setItems(selected);
    }, [config, navigate]);

    const currentItem = items[currentStep];
    const contrastData = config.contrast ? (VOCABULARY.discrimination.base[config.contrast] || VOCABULARY.discrimination.rich[config.contrast]) : null;

    const noiseWhiteRef = React.useRef(null);
    const noiseBgRef = React.useRef(null);
    const audioInstanceRef = React.useRef(null); // Reference to current playing word audio
    const [needsInteraction, setNeedsInteraction] = useState(false);

    useEffect(() => {
        const bgAudio = noiseBgRef.current;
        const whiteAudio = noiseWhiteRef.current;

        if (!bgAudio || !whiteAudio) return;

        bgAudio.pause();
        whiteAudio.pause();

        if (noiseVolume > 0) {
            const activeAudio = noiseType === 'background' ? bgAudio : whiteAudio;

            const baseVol = noiseType === 'background' ? 0.05 : 0.3;
            activeAudio.volume = baseVol * noiseVolume;

            activeAudio.play().catch(e => console.log("Audio play prevented:", e));
        }
    }, [noiseVolume, noiseType]);

    const handleUserStart = () => {

        setGameState('playing');
    };

    const playSound = React.useCallback(() => {
        if (!currentItem || gameState !== 'playing') return;

        // Stop any currently playing audio instance
        if (audioInstanceRef.current) {
            audioInstanceRef.current.pause();
            audioInstanceRef.current.currentTime = 0;
            audioInstanceRef.current = null;
        }
        window.speechSynthesis.cancel();

        setIsPlaying(true);

        const audioPath = `${import.meta.env.BASE_URL}audio/words/${currentItem.id}.mp3`;
        const wordAudio = new Audio(audioPath);
        audioInstanceRef.current = wordAudio; // Track this instance

        if (config.voiceGender === 'male') {
            wordAudio.playbackRate = 0.85;
            wordAudio.preservesPitch = false;
        }

        wordAudio.onended = () => {
            if (audioInstanceRef.current === wordAudio) setIsPlaying(false);
        };
        wordAudio.onerror = () => {
            console.log("File audio missing, using TTS fallback");

            const u = new SpeechSynthesisUtterance(currentItem.label);
            u.lang = 'ar-SA';
            u.rate = config.voiceGender === 'male' ? 0.7 : 0.9;
            u.pitch = config.voiceGender === 'male' ? 0.6 : 1.1;

            u.onstart = () => {
                if (audioInstanceRef.current === wordAudio) setIsPlaying(true);
            };
            u.onend = () => {
                if (audioInstanceRef.current === wordAudio) setIsPlaying(false);
            };
            window.speechSynthesis.speak(u);
        };

        wordAudio.play().catch(e => {
            console.log("Audio play failed, falling back:", e);
            wordAudio.onerror();
        });
    }, [currentItem, config, gameState]);

    useEffect(() => {
        if (gameState !== 'playing' || !currentItem) return;

        playSound();
    }, [playSound, currentItem, gameState]);

    const handleChoice = (phoneme) => {
        if (feedback === 'correct') return;

        setAttempts(a => a + 1);

        if (phoneme === currentItem.phoneme) {

            const isFirstTry = attempts === 0;

            setStars(prev => [...prev, isFirstTry]);

            if (isFirstTry) {
                setScore(s => s + 1);
            }

            setFeedback('correct');

            // Stop current audio immediately on correct choice
            if (audioInstanceRef.current) {
                audioInstanceRef.current.pause();
                audioInstanceRef.current.currentTime = 0;
                audioInstanceRef.current = null;
            }
            window.speechSynthesis.cancel();
            setIsPlaying(false);

            setTimeout(() => {
                if (currentStep < items.length - 1) {
                    setCurrentStep(c => c + 1);
                    setFeedback(null);
                    setAttempts(0);
                } else {
                    setGameState('score_reveal');
                }
            }, 1500);
        } else {

            setFeedback('incorrect');
            setTimeout(() => {
                setFeedback(null);
            }, 1000);
        }
    };

    if (items.length === 0) return <div className="container">Chargement...</div>;

    return (
        <div className="container" style={{ position: 'relative', overflow: 'hidden' }}>
            <div className="bubbles">
                {Array.from({ length: 10 }).map((_, i) => <div key={i} className="bubble"></div>)}
            </div>

            { }
            <audio ref={noiseWhiteRef} loop src={`${import.meta.env.BASE_URL}audio/noise_white.mp3`} />
            <audio ref={noiseBgRef} loop src={`${import.meta.env.BASE_URL}audio/noise_continu.mp3`} />

            { }
            { }
            {gameState !== 'intro' && (
                <>
                    { }
                    <button
                        className="btn"
                        onClick={() => setShowSettings(!showSettings)}
                        style={{
                            position: 'absolute', top: '1rem', right: '1rem',
                            width: '40px', height: '40px', borderRadius: '50%',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            background: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
                            zIndex: 101, padding: 0
                        }}
                    >
                        <Settings size={24} color="#64748b" />
                    </button>

                    { }
                    {showSettings && (
                        <div style={{
                            position: 'absolute', top: '4rem', right: '1rem',
                            background: 'rgba(255,255,255,0.95)', padding: '1rem',
                            borderRadius: '1rem', boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
                            display: 'flex', flexDirection: 'column', gap: '1rem', zIndex: 100,
                            minWidth: '200px', animation: 'fadeIn 0.2s ease-out'
                        }}>
                            <h4 style={{ margin: 0, fontSize: '1rem', color: '#64748b' }}>Ambiance Sonore</h4>

                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <span style={{ fontSize: '0.9rem' }}>Type:</span>
                                <button
                                    className="btn"
                                    onClick={() => setNoiseType(t => t === 'background' ? 'white' : 'background')}
                                    style={{ fontSize: '0.8rem', padding: '0.3rem 0.8rem', background: '#e2e8f0' }}
                                >
                                    {noiseType === 'background' ? 'Continue 〰️' : 'Bruit Blanc 💨'}
                                </button>
                            </div>

                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <button
                                    className="btn"
                                    onClick={() => setNoiseVolume(v => Math.max(0, v - 0.1))}
                                    disabled={noiseVolume <= 0}
                                    style={{ padding: '0.3rem', borderRadius: '50%', width: '30px', height: '30px', minHeight: 'auto' }}
                                >
                                    <Minus size={16} />
                                </button>

                                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                    {noiseVolume === 0 ? <VolumeX size={20} color="#999" /> : <Volume2 size={20} color="var(--primary)" />}
                                    <div style={{ height: '4px', width: '100%', background: '#eee', marginTop: '4px', borderRadius: '2px', overflow: 'hidden' }}>
                                        <div style={{ height: '100%', width: `${noiseVolume * 100}%`, background: 'var(--primary)' }} />
                                    </div>
                                </div>

                                <button
                                    className="btn"
                                    onClick={() => setNoiseVolume(v => Math.min(1, v + 0.1))}
                                    disabled={noiseVolume >= 1}
                                    style={{ padding: '0.3rem', borderRadius: '50%', width: '30px', height: '30px', minHeight: 'auto' }}
                                >
                                    <Plus size={16} />
                                </button>
                            </div>
                        </div>
                    )}
                    <style>{`
                        @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
                    `}</style>
                </>
            )}

            { }
            {gameState === 'intro' && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.85)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexDirection: 'column', color: 'white'
                }}>
                    <img src={`${import.meta.env.BASE_URL}assets/images/story/patrick_sad.jpg`} alt="Patrick Sad" style={{ height: '250px', marginBottom: '1rem', borderRadius: '1rem', boxShadow: '0 10px 20px rgba(0,0,0,0.5)' }} />
                    <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '3rem', marginBottom: '1rem', textAlign: 'center' }}>
                        Patrick a besoin de toi !
                    </h1>
                    <p style={{ fontSize: '1.5rem', maxWidth: '1000px', marginBottom: '2rem' }}>
                        Patrick est tout seul de l'autre côté...<br />
                        Aide SpongeBob à traverser le chemin pour le retrouver !
                    </p>
                    <button
                        className="btn btn-primary"
                        style={{ fontSize: '2rem', padding: '1.5rem 4rem' }}
                        onClick={handleUserStart}
                    >
                        J'ARRIVE ! 🚀
                    </button>
                </div>
            )}

            { }
            {gameState === 'score_reveal' && (
                <div style={{
                    position: 'fixed', inset: 0,
                    background: 'rgba(0,0,0,0.9)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'
                }}>
                    <h1 style={{ color: 'white', fontSize: '3rem', marginBottom: '2rem' }}>Résultat</h1>
                    <div style={{ display: 'flex', gap: '10px', marginBottom: '3rem' }}>
                        {stars.map((s, i) => (
                            <div key={i} style={{
                                animation: `pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards`,
                                animationDelay: `${i * 0.2}s`,
                                opacity: 0, transform: 'scale(0)'
                            }}>
                                <CheckCircle size={60} color={s ? "#fdba74" : "#334155"} fill={s ? "#fbbf24" : "transparent"} />
                            </div>
                        ))}
                    </div>
                    <div style={{ color: 'white', fontSize: '2rem', marginBottom: '2rem' }}>
                        {Math.round(score)} / 10 Étoiles
                    </div>
                    <button className="btn btn-primary" onClick={() => setGameState('won')}>
                        CONTINUER ➡️
                    </button>
                    <style>{`
                        @keyframes pop { to { opacity: 1; transform: scale(1); } }
                    `}</style>
                </div>
            )}

            { }
            {gameState === 'won' && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(255,255,255,0.95)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexDirection: 'column'
                }}>
                    <img src={`${import.meta.env.BASE_URL}assets/images/story/reunion.jpg`} alt="Friends Reunited" style={{ height: '300px', marginBottom: '1rem', borderRadius: '1rem', boxShadow: '0 10px 20px rgba(0,0,0,0.2)' }} />
                    <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '4rem', color: 'var(--secondary)', marginBottom: '1rem' }}>
                        BRAVO !
                    </h1>
                    <p style={{ fontSize: '2rem', color: 'var(--text-main)', marginBottom: '2rem', textAlign: 'center' }}>
                        Tu as aidé SpongeBob à retrouver Patrick ! <br />
                        Ils sont trop contents !
                    </p>
                    <button
                        className="btn btn-primary"
                        onClick={() => navigate('/')}
                    >
                        REJOUER 🏠
                    </button>
                </div>
            )}

            <div style={{
                flex: 1, 
                overflow: 'hidden', 
                padding: '2rem 0',
                display: 'flex', flexDirection: 'column', justifyContent: 'flex-start',
                filter: gameState !== 'playing' ? 'blur(5px)' : 'none',
                transition: 'filter 0.5s'
            }}>
                <GamePath totalSteps={items.length} currentStep={currentStep} stars={stars} />

                <div className="card" style={{
                    marginTop: '2rem',
                    minHeight: 'auto',
                    padding: '1.5rem',
                    display: 'flex', flexDirection: 'column', alignItems: 'center'
                }}>

                    <button
                        className="btn btn-secondary"
                        onClick={playSound}
                        disabled={isPlaying}
                        style={{
                            borderRadius: '50%', width: '60px', height: '60px',
                            padding: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                            marginBottom: '0.2rem', animation: isPlaying ? 'pulse 1s infinite' : 'none'
                        }}>
                        <Volume2 size={32} />
                    </button>
                    <span style={{ fontSize: '0.9rem', color: '#64748b', marginBottom: '0.5rem', fontWeight: '500' }}>Répéter le son</span>

                    <h2 style={{
                        marginBottom: '0.5rem',
                        fontFamily: 'var(--font-heading)',
                        fontSize: '1.5rem',
                        lineHeight: 1.2
                    }}>
                        Qu'est ce que tu as entendu ?
                    </h2>

                    {(() => {
                        let imageFilename = itemsImages[currentItem.word] || itemsImages[currentItem.id];
                        if (!imageFilename) {
                            for (const catLevel of Object.values(VOCABULARY.categorization)) {
                                const matchingItem = catLevel.find(item => item.label === currentItem.label);
                                if (matchingItem && itemsImages[matchingItem.word]) {
                                    imageFilename = itemsImages[matchingItem.word];
                                    break;
                                } else if (matchingItem && itemsImages[matchingItem.id]) {
                                    imageFilename = itemsImages[matchingItem.id];
                                    break;
                                }
                            }
                        }

                        if (imageFilename) {
                            return (
                                <div style={{ marginBottom: '0.5rem', display: 'flex', justifyContent: 'center' }}>
                                    <img
                                        src={`${import.meta.env.BASE_URL}assets/images/items/${imageFilename}`}
                                        alt={currentItem.label}
                                        style={{
                                            width: '250px', height: '250px', objectFit: 'contain',
                                            borderRadius: '1rem', boxShadow: '0px 8px 15px rgba(0,0,0,0.15)',
                                            background: 'white', padding: '10px'
                                        }}
                                        onError={(e) => {
                                            // Fallback if not in items/
                                            if (!e.target.src.includes('/categories/')) {
                                                e.target.src = e.target.src.replace('/items/', '/categories/');
                                            }
                                        }}
                                    />
                                </div>
                            );
                        }
                        return null;
                    })()}

                    <div className="choice-container" style={{
                        display: 'flex', gap: '1.5rem', width: '100%', maxWidth: '1000px',
                        marginTop: '1rem'
                    }}>
                        <button
                            className="btn choice-btn"
                            style={{
                                background: '#e0e7ff',
                                border: '2px solid var(--primary)',
                                flex: 1, height: '80px', fontSize: '2.5rem',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                borderRadius: '1rem', boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                                transition: 'all 0.2s'
                            }}
                            onClick={() => handleChoice(contrastData.target_1)}
                            disabled={feedback === 'correct'}
                        >
                            {{
                                'b': 'ب', 'm': 'م',
                                't': 'ت', 'd': 'د',
                                'ch': 'ش', 'j': 'ج',
                                'k': 'ك', 'g': 'ق',
                                'f': 'ف', 'v': 'v',
                                'kh': 'خ', 'h': 'ه',
                                's': 'س'
                            }[contrastData.target_1] || contrastData.target_1.toUpperCase()}
                        </button>

                        <button
                            className="btn choice-btn"
                            style={{
                                background: '#e0e7ff',
                                border: '2px solid var(--primary)',
                                flex: 1, height: '80px', fontSize: '2.5rem',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                borderRadius: '1rem', boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                                transition: 'all 0.2s'
                            }}
                            onClick={() => handleChoice(contrastData.target_2)}
                            disabled={feedback === 'correct'}
                        >
                            {{
                                'b': 'ب', 'm': 'م',
                                't': 'ت', 'd': 'د',
                                'ch': 'ش', 'j': 'ج',
                                'k': 'ك', 'g': 'ق',
                                'f': 'ف', 'v': 'v',
                                'kh': 'خ', 'h': 'ه',
                                's': 'س'
                            }[contrastData.target_2] || contrastData.target_2.toUpperCase()}
                        </button>
                    </div>

                </div>

                <style>{`
                    .choice-btn:hover:not(:disabled) { transform: scale(1.05); background: #c7d2fe !important; }
                    .choice-btn:active:not(:disabled) { transform: scale(0.95); }
                    @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.1); } 100% { transform: scale(1); } }
                    @media (max-width: 600px) {
                        .choice-container { flex-direction: column; }
                        .choice-btn { height: 60px !important; fontSize: 2rem !important; }
                    }
                `}</style>
            </div>

            {feedback === 'incorrect' && (
                <div style={{
                    position: 'absolute', inset: 0,
                    background: 'rgba(255,255,255,0.85)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    zIndex: 1000, backdropFilter: 'blur(8px)',
                    animation: 'fadeIn 0.3s ease-out'
                }}>
                    <div style={{
                        fontSize: '5rem', color: 'var(--danger)',
                        display: 'flex', flexDirection: 'column', alignItems: 'center',
                        animation: 'shake 0.5s ease-in-out'
                    }}>
                        <XCircle size={120} style={{ marginBottom: '1rem' }} />
                        Réessaie
                    </div>
                </div>
            )}

            {feedback === 'correct' && (
                <div style={{
                    position: 'absolute', inset: 0,
                    background: 'rgba(255,255,255,0.85)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    zIndex: 1000, backdropFilter: 'blur(8px)',
                    animation: 'fadeIn 0.3s ease-out'
                }}>
                    <div style={{
                        fontSize: '5rem', color: 'var(--secondary)',
                        display: 'flex', flexDirection: 'column', alignItems: 'center',
                        animation: 'bounce 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                    }}>
                        <CheckCircle size={120} style={{ marginBottom: '1rem' }} />
                        Bravo !
                    </div>
                </div>
            )}
            <style>{`
                @keyframes bounce { 
                    0% { transform: scale(0.3); opacity: 0; }
                    50% { transform: scale(1.1); }
                    70% { transform: scale(0.9); }
                    100% { transform: scale(1); opacity: 1; }
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-10px); }
                    75% { transform: translateX(10px); }
                }
                @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            `}</style>
        </div>
    );
};

export default Activity1;

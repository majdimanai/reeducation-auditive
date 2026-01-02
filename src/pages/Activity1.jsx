import React, { useState, useEffect } from 'react';
import { useGame } from '../context/GameContext';
import { VOCABULARY } from '../data/vocabulary';
import GamePath from '../components/GamePath';
import { useNavigate } from 'react-router-dom';
import { Volume2, AlertCircle, CheckCircle, VolumeX, Volume1, Plus, Minus, Settings } from 'lucide-react';

const Activity1 = () => {
    const { config, setScore, score } = useGame();
    const navigate = useNavigate();

    // Game Logic State
    const [items, setItems] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [feedback, setFeedback] = useState(null); // 'correct', 'incorrect'
    const [isPlaying, setIsPlaying] = useState(false);

    // Star System State
    const [attempts, setAttempts] = useState(0); // Track attempts for current item
    const [stars, setStars] = useState([]); // Array of booleans [true, false, true...]


    // Noise State
    const [noiseVolume, setNoiseVolume] = useState(0); // 0 to 1
    const [noiseType, setNoiseType] = useState('background'); // 'background' or 'white'
    const [showSettings, setShowSettings] = useState(false);

    // Game State: 'intro' | 'playing' | 'score_reveal' | 'won'
    const [gameState, setGameState] = useState('intro');

    // Initialize Game
    useEffect(() => {
        if (!config.contrast) {
            // Fallback if no config, redirect
            navigate('/');
            return;
        }

        const contrastData = VOCABULARY.discrimination.base[config.contrast] || VOCABULARY.discrimination.rich[config.contrast];
        if (!contrastData) return;

        // Get all words
        const allWords = contrastData.words;
        // Shuffle and pick 10
        const shuffled = [...allWords].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 10); // STRICT LIMIT 10
        setItems(selected);
    }, [config, navigate]);

    const currentItem = items[currentStep];
    const contrastData = config.contrast ? (VOCABULARY.discrimination.base[config.contrast] || VOCABULARY.discrimination.rich[config.contrast]) : null;

    // Audio Refs
    const noiseWhiteRef = React.useRef(null);
    const noiseBgRef = React.useRef(null);
    const [needsInteraction, setNeedsInteraction] = useState(false);

    // Audio Control Effect
    useEffect(() => {
        const bgAudio = noiseBgRef.current;
        const whiteAudio = noiseWhiteRef.current;

        if (!bgAudio || !whiteAudio) return;

        // Pause all first
        bgAudio.pause();
        whiteAudio.pause();

        if (noiseVolume > 0) {
            const activeAudio = noiseType === 'background' ? bgAudio : whiteAudio;
            // Background noise is naturally louder, so we scale it down a bit more
            const baseVol = noiseType === 'background' ? 0.05 : 0.3;
            activeAudio.volume = baseVol * noiseVolume;

            activeAudio.play().catch(e => console.log("Audio play prevented:", e));
        }
    }, [noiseVolume, noiseType]);

    const handleUserStart = () => {
        // Just start the game, audio is now user-controlled
        setGameState('playing');
    };

    const playSound = React.useCallback(() => {
        if (!currentItem || gameState !== 'playing') return;
        setIsPlaying(true);

        // Ensure BG audio is playing if volume > 0
        if (noiseVolume > 0) {
            const activeAudio = noiseType === 'background' ? noiseBgRef.current : noiseWhiteRef.current;
            if (activeAudio && activeAudio.paused) {
                activeAudio.play().catch(e => console.log("Bg resume failed:", e));
            }
        }

        // Try pre-generated audio
        const audioPath = `/audio/words/${currentItem.id}.mp3`;
        const wordAudio = new Audio(audioPath);

        // Apply Pitch Shift if Male
        if (config.voiceGender === 'male') {
            wordAudio.playbackRate = 0.85;
            wordAudio.preservesPitch = false;
        }

        wordAudio.onended = () => setIsPlaying(false);
        wordAudio.onerror = () => {
            console.log("File audio missing, using TTS fallback");
            // TTS Fallback
            const u = new SpeechSynthesisUtterance(currentItem.label);
            u.lang = 'ar-SA';
            u.rate = config.voiceGender === 'male' ? 0.7 : 0.9;
            u.pitch = config.voiceGender === 'male' ? 0.6 : 1.1;

            u.onend = () => setIsPlaying(false);
            window.speechSynthesis.speak(u);
        };

        wordAudio.play().catch(e => {
            console.log("Audio play failed, falling back:", e);
            wordAudio.onerror();
        });
    }, [currentItem, config, gameState]);

    // Auto-Repeat Audio Loop (5s)
    useEffect(() => {
        if (gameState !== 'playing' || !currentItem) return;

        // Initial Play
        playSound();

        const interval = setInterval(() => {
            playSound();
        }, 5000);

        return () => clearInterval(interval);
    }, [playSound, currentItem, gameState]);

    const handleChoice = (phoneme) => {
        if (feedback === 'correct') return; // already done

        // Increment attempts on every click
        setAttempts(a => a + 1);

        if (phoneme === currentItem.phoneme) {
            // Correct
            const isFirstTry = attempts === 0;

            // Add star if first try
            setStars(prev => [...prev, isFirstTry]);

            // Score only updates if it's a star (per user request: total score is sum of stars)
            if (isFirstTry) {
                setScore(s => s + 1);
            }

            setFeedback('correct');

            setTimeout(() => {
                if (currentStep < items.length - 1) {
                    setCurrentStep(c => c + 1);
                    setFeedback(null);
                    setAttempts(0); // Reset for next
                } else {
                    setGameState('score_reveal'); // Show score first, then story
                }
            }, 1500);
        } else {
            // Incorrect
            setFeedback('incorrect');
        }
    };

    if (items.length === 0) return <div className="container">Chargement...</div>;

    return (
        <div className="container" style={{ position: 'relative', overflow: 'hidden' }}>
            <div className="bubbles">
                {Array.from({ length: 10 }).map((_, i) => <div key={i} className="bubble"></div>)}
            </div>

            {/* Audio Elements with Refs - Public Path */}
            <audio ref={noiseWhiteRef} loop src="/audio/noise_white.webm" />
            <audio ref={noiseBgRef} loop src="/audio/noise_continu.webm" />

            {/* NOISE CONTROL PANEL */}
            {/* NOISE CONTROL PANEL (Collapsible Top-Right) */}
            {gameState !== 'intro' && (
                <>
                    {/* Toggle Button */}
                    <button
                        className="btn"
                        onClick={() => setShowSettings(!showSettings)}
                        style={{
                            position: 'absolute', top: '1rem', right: '1rem', /* TOP RIGHT */
                            width: '40px', height: '40px', borderRadius: '50%',
                            display: 'flex', alignItems: 'center', justifyContent: 'center',
                            background: 'white', boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
                            zIndex: 101, padding: 0
                        }}
                    >
                        <Settings size={24} color="#64748b" />
                    </button>

                    {/* Expanded Panel */}
                    {showSettings && (
                        <div style={{
                            position: 'absolute', top: '4rem', right: '1rem', /* Dropping down from right */
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

            {/* INTRO OVERLAY */}
            {gameState === 'intro' && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.85)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexDirection: 'column', color: 'white'
                }}>
                    <img src="/src/assets/images/patrick_sad.jpg" alt="Patrick Sad" style={{ height: '250px', marginBottom: '1rem', borderRadius: '1rem', boxShadow: '0 10px 20px rgba(0,0,0,0.5)' }} />
                    <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '3rem', marginBottom: '1rem', textAlign: 'center' }}>
                        Patrick a besoin de toi !
                    </h1>
                    <p style={{ fontSize: '1.5rem', maxWidth: '600px', marginBottom: '2rem' }}>
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

            {/* SCORE REVEAL OVERLAY */}
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

            {/* SUCCESS OVERLAY */}
            {gameState === 'won' && (
                <div style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(255,255,255,0.95)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexDirection: 'column'
                }}>
                    <img src="/src/assets/images/reunion.jpg" alt="Friends Reunited" style={{ height: '300px', marginBottom: '1rem', borderRadius: '1rem', boxShadow: '0 10px 20px rgba(0,0,0,0.2)' }} />
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
                flex: 1, /* Take remaining height */
                overflowY: 'auto', /* Scroll only if absolutely needed, but we optimized to avoid it */
                padding: '0.5rem',
                display: 'flex', flexDirection: 'column', justifyContent: 'flex-start',
                filter: gameState !== 'playing' ? 'blur(5px)' : 'none',
                transition: 'filter 0.5s'
            }}>
                <GamePath totalSteps={items.length} currentStep={currentStep} stars={stars} />

                <div className="card" style={{
                    marginTop: '0.5rem',
                    minHeight: 'auto', /* Remove fixed min-height */
                    padding: '1.5rem', /* Reduced padding */
                    display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'
                }}>

                    <button
                        className="btn btn-secondary"
                        onClick={playSound}
                        disabled={isPlaying}
                        style={{
                            borderRadius: '50%', width: '60px', height: '60px', /* Smaller speaker button */
                            padding: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                            marginBottom: '1rem', animation: isPlaying ? 'pulse 1s infinite' : 'none'
                        }}
                    >
                        <Volume2 size={30} />
                    </button>

                    <h2 style={{
                        marginBottom: '1rem',
                        fontFamily: 'var(--font-heading)',
                        fontSize: 'clamp(1.5rem, 5vw, 2.5rem)', /* fluid font */
                        lineHeight: 1.2
                    }}>
                        Qu'est ce que tu as entendu ?
                    </h2>

                    <div className="choice-container" style={{ width: '100%' }}>
                        <button
                            className="btn choice-btn"
                            style={{
                                background: '#e0e7ff',
                                border: '2px solid var(--primary)',
                                width: '100%' // Full width inside grid cell
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
                                width: '100%' // Full width inside grid cell
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

                    {feedback === 'correct' && (
                        <div style={{ color: 'var(--secondary)', marginTop: '2rem', display: 'flex', alignItems: 'center', fontSize: '1.5rem' }}>
                            <CheckCircle size={32} style={{ marginRight: '10px' }} /> Bravo !
                        </div>
                    )}

                    {feedback === 'incorrect' && (
                        <div style={{ color: 'var(--danger)', marginTop: '2rem', display: 'flex', alignItems: 'center', fontSize: '1.5rem' }}>
                            <AlertCircle size={32} style={{ marginRight: '10px' }} /> Essaie encore !
                        </div>
                    )}
                </div>

                <style>{`
                    /* Already stacking via flex-wrap in parent div or we can force it */
                    @media (max-width: 600px) {
                        .choice-container > div {
                            flex-direction: column;
                            align-items: stretch;
                        }
                    }
                `}</style>
            </div>
        </div>
    );
};

export default Activity1;

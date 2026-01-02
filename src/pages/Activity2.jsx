import React, { useState, useEffect } from 'react';
import { useGame } from '../context/GameContext';
import { VOCABULARY } from '../data/vocabulary';
import GamePath from '../components/GamePath';
import { useNavigate } from 'react-router-dom';
import { Volume2, AlertCircle, CheckCircle, VolumeX, Volume1, Plus, Minus, Settings } from 'lucide-react';

const Activity2 = () => {
    const { config, setScore, score } = useGame(); // Reverted destructuring
    const navigate = useNavigate();

    const [items, setItems] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [feedback, setFeedback] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [options, setOptions] = useState([]);

    // Star System State
    const [attempts, setAttempts] = useState(0); // Track attempts for current item
    const [stars, setStars] = useState([]); // Array of booleans [true, false, true...]

    // Noise State
    const [noiseVolume, setNoiseVolume] = useState(0); // 0 to 1
    const [noiseType, setNoiseType] = useState('background'); // 'background' or 'white'
    const [showSettings, setShowSettings] = useState(false);

    // Game State: 'intro' | 'playing' | 'score_reveal' | 'won'
    const [gameState, setGameState] = useState('intro');

    // Setup Items
    useEffect(() => {
        let pool = [];
        if (config.vocabularyLevel === 'docx_rich') {
            pool = [...VOCABULARY.categorization.docx_rich];
        } else if (config.vocabularyLevel === 'docx_simple') {
            pool = [...VOCABULARY.categorization.docx_simple];
        } else if (config.vocabularyLevel === 'rich') {
            pool = [...VOCABULARY.categorization.rich];
        } else {
            // Default to Base
            pool = [...VOCABULARY.categorization.base];
        }

        // Pick 10 random items
        const shuffled = pool.sort(() => 0.5 - Math.random()).slice(0, 10);
        setItems(shuffled);
    }, [config]);

    const currentItem = items[currentStep];

    // Setup Options for current item
    useEffect(() => {
        if (!currentItem) return;

        // Map internal category to Arabic display
        const catMap = {
            'animaux': 'حيوانات', 'fruits': 'فواكه', 'legumes': 'خضر', 'corps': 'جسم', 'transport': 'نقل',
            'maison': 'منزل', 'couleurs': 'ألوان', 'alimentation': 'مأكولات', 'vetements': 'ملابس', 'ecole': 'مدرسة'
        };

        const internalCats = Object.keys(catMap);
        const correctCat = { id: currentItem.category, label: catMap[currentItem.category] };

        // Pick 2 distractors
        const otherCats = internalCats
            .filter(c => c !== currentItem.category)
            .sort(() => 0.5 - Math.random())
            .slice(0, 2)
            .map(c => ({ id: c, label: catMap[c] }));

        const currentOptions = [correctCat, ...otherCats].sort(() => 0.5 - Math.random());
        setOptions(currentOptions);
        setFeedback(null);
    }, [currentItem]);

    // Audio Refs
    const noiseWhiteRef = React.useRef(null);
    const noiseBgRef = React.useRef(null);

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
        setGameState('playing'); // Start the game
    };

    const playSound = React.useCallback(() => {
        if (!currentItem || gameState !== 'playing') return;
        setIsPlaying(true);

        const audioId = currentItem.id.replace(/^[sr]_/, '');
        const audioPath = `/audio/words/${audioId}.mp3`;
        const wordAudio = new Audio(audioPath);

        // Apply Pitch Shift if Male selected (Simulation)
        if (config.voiceGender === 'male') {
            wordAudio.playbackRate = 0.85;
            wordAudio.preservesPitch = false;
        }

        wordAudio.onended = () => {
            setIsPlaying(false);
        };
        wordAudio.onerror = () => {
            console.log("Using TTS fallback");
            const u = new SpeechSynthesisUtterance(currentItem.label);
            u.lang = 'ar-SA';
            u.rate = config.voiceGender === 'male' ? 0.7 : 0.9;
            u.pitch = config.voiceGender === 'male' ? 0.6 : 1.1;

            u.onend = () => {
                setIsPlaying(false);
            };
            window.speechSynthesis.speak(u);
        };
        wordAudio.play().catch(e => wordAudio.onerror());
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

    const handleChoice = (catId) => {
        if (feedback === 'correct') return;

        // Increment attempts on every click
        setAttempts(a => a + 1);

        if (catId === currentItem.category) {

            const isFirstTry = attempts === 0;
            setStars(prev => [...prev, isFirstTry]);
            if (isFirstTry) {
                setScore(s => s + 1);
            }

            setFeedback('correct');

            setTimeout(() => {
                if (currentStep < items.length - 1) {
                    setCurrentStep(c => c + 1);
                    setAttempts(0); // Reset for next
                } else {
                    setGameState('score_reveal'); // Score Reveal
                }
            }, 1500);
        } else {
            setFeedback('incorrect');
        }
    };

    const getCategoryIcon = (cat) => {
        const map = {
            'animaux': '🐾', 'fruits': '🍎', 'legumes': '🥦', 'corps': '👂', 'transport': '🚗',
            'maison': '🏠', 'couleurs': '🎨', 'alimentation': '🍔', 'vetements': '👕', 'ecole': '🏫'
        };
        return map[cat] || '❓';
    };

    if (items.length === 0) return <div className="container">Chargement...</div>;

    return (
        <div className="container" style={{ position: 'relative', overflow: 'hidden' }}>
            <div className="bubbles">
                {Array.from({ length: 10 }).map((_, i) => <div key={i} className="bubble"></div>)}
            </div>
            <audio ref={noiseWhiteRef} loop src="/audio/noise_white.webm" />
            <audio ref={noiseBgRef} loop src="/audio/noise_continu.webm" />

            {/* DIFFICULTY CONTROL REMOVED */}

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
                                    style={{ padding: '0.2rem', borderRadius: '50%', width: '30px', height: '30px', minHeight: 'auto' }}
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

            {/* MAIN GAME */}
            <div style={{
                flex: 1,
                overflowY: 'auto',
                padding: '0.5rem',
                display: 'flex', flexDirection: 'column', justifyContent: 'flex-start',
                filter: gameState !== 'playing' ? 'blur(5px)' : 'none',
                transition: 'filter 0.5s'
            }}>
                <GamePath totalSteps={items.length} currentStep={currentStep} stars={stars} />

                {!currentItem ? (
                    <div className="card" style={{ marginTop: '2rem', padding: '2rem' }}>
                        <h2>Chargement...</h2>
                    </div>
                ) : (
                    <div className="card" style={{
                        marginTop: '0.5rem',
                        minHeight: 'auto',
                        padding: '1rem',
                        display: 'flex', flexDirection: 'column', alignItems: 'center'
                    }}>

                        {/* SPEAKER BUTTON (Activity 1 style) */}
                        <button
                            className="btn btn-secondary"
                            onClick={playSound}
                            disabled={isPlaying}
                            style={{
                                borderRadius: '50%', width: '80px', height: '80px',
                                padding: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
                                marginBottom: '1rem', animation: isPlaying ? 'pulse 1s infinite' : 'none'
                            }}
                        >
                            <Volume2 size={40} />
                        </button>

                        <h2 style={{
                            marginBottom: '1rem',
                            fontFamily: 'var(--font-heading)',
                            fontSize: 'clamp(1.5rem, 5vw, 2.5rem)',
                            lineHeight: 1.2
                        }}>
                            Qu'est ce que tu as entendu ?
                        </h2>

                        <h3 className="title" style={{
                            fontSize: 'clamp(1.2rem, 3vw, 1.8rem)',
                            margin: '0.2rem 0',
                            textShadow: 'none',
                            color: 'var(--text-main)',
                            WebkitTextStroke: '0',
                            opacity: 0.8
                        }}>
                            Choisis la bonne catégorie :
                        </h3>

                        {/* OPTIONS GRID - RESPONSIVE */}
                        <div className="options-grid" style={{
                            display: 'grid',
                            gap: '1.5rem',
                            width: '100%',
                            maxWidth: '800px'
                        }}>
                            {options.map(opt => {
                                let btnClass = 'btn btn-option';
                                if (feedback === 'correct' && opt.id === currentItem.category) btnClass += ' btn-correct';
                                if (feedback === 'incorrect' && opt.id !== currentItem.category) btnClass += ' btn-incorrect';

                                // Image Mapping
                                const CATEGORY_IMAGES = {
                                    'maison': '/assets/images/categories/maison.jpeg',
                                    'alimentation': '/assets/images/categories/alimentation.jpeg',
                                    'animaux': '/assets/images/categories/corps.jpeg',
                                    'fruits': '/assets/images/categories/fruits.jpeg',
                                    'legumes': '/assets/images/categories/legumes.jpeg',
                                    'corps': '/assets/images/categories/animaux.jpeg',
                                    'transport': '/assets/images/categories/transport.jpeg',
                                    // 'ecole': '/assets/images/categories/ecole.jpeg', // Fallback to emoji
                                    'vetements': '/assets/images/categories/vetements.jpeg',
                                    'couleurs': '/assets/images/categories/couleurs.jpeg',
                                };
                                const imageSrc = CATEGORY_IMAGES[opt.id];

                                return (
                                    <button
                                        key={opt.id}
                                        className={`btn btn-option opt-btn ${feedback === 'correct' && opt.id === currentItem.category ? 'btn-correct' : ''}`}
                                        onClick={() => handleChoice(opt.id)}
                                        disabled={feedback === 'correct'}
                                        style={{
                                            display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'
                                            /* Height handled by class */
                                        }}
                                    >
                                        {imageSrc ? (
                                            <img
                                                src={imageSrc}
                                                alt={opt.label}
                                                className="opt-icon-img"
                                            />
                                        ) : (
                                            <span className="opt-icon" style={{ fontSize: '4rem', marginBottom: '0.5rem', filter: 'drop-shadow(0 4px 4px rgba(0,0,0,0.1))' }}>
                                                {getCategoryIcon(opt.id)}
                                            </span>
                                        )}
                                        <span className="opt-label" style={{ fontSize: '1.8rem' }}>{opt.label}</span>
                                    </button>
                                );
                            })}
                        </div>

                        <style>{`
                        .options-grid { grid-template-columns: repeat(3, 1fr); }
                        .opt-btn { height: 180px; }
                        
                        .opt-icon-img {
                            width: 100px; height: 100px; object-fit: contain; margin-bottom: 0.5rem;
                            filter: drop-shadow(0 4px 4px rgba(0,0,0,0.1));
                        }

                        @media (max-width: 768px) {
                            .options-grid { grid-template-columns: 1fr; gap: 1rem; }
                            .opt-btn { 
                                height: 100px; /* Much smaller on mobile */
                                flex-direction: row !important; /* Row layout on mobile to save vertical space */
                                justify-content: flex-start !important;
                                padding: 0 2rem !important;
                            }
                            .opt-icon { font-size: 2.5rem !important; margin-bottom: 0 !important; margin-right: 1rem; }
                            .opt-icon-img {
                                width: 60px; height: 60px; margin-bottom: 0 !important; margin-right: 1rem;
                            }
                            .opt-label { font-size: 1.5rem !important; }
                        }
                    `}</style>
                    </div>
                )}
            </div>

            {feedback === 'correct' && (
                <div style={{
                    position: 'absolute', inset: 0,
                    background: 'rgba(255,255,255,0.8)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    zIndex: 10, backdropFilter: 'blur(5px)'
                }}>
                    <div style={{
                        fontSize: '4rem', color: 'var(--secondary)',
                        display: 'flex', flexDirection: 'column', alignItems: 'center',
                        animation: 'bounce 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                    }}>
                        <CheckCircle size={80} style={{ marginBottom: '1rem' }} />
                        Bravo !
                    </div>
                </div>
            )}
        </div>
    );
};

export default Activity2;

import React, { useState, useEffect } from 'react';
import { useGame } from '../context/GameContext';
import { VOCABULARY } from '../data/vocabulary';
import itemsImages from '../data/items_images.json';
import GamePath from '../components/GamePath';
import { useNavigate } from 'react-router-dom';
import { Volume2, AlertCircle, CheckCircle, VolumeX, RotateCcw, Volume1, Plus, Minus, Settings, XCircle } from 'lucide-react';

const Activity2 = () => {
    const { config, setScore, score } = useGame();
    const navigate = useNavigate();

    const [items, setItems] = useState([]);
    const [currentStep, setCurrentStep] = useState(0);
    const [feedback, setFeedback] = useState(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [options, setOptions] = useState([]);

    const [attempts, setAttempts] = useState(0);
    const [stars, setStars] = useState([]);

    const [noiseVolume, setNoiseVolume] = useState(0);
    const [noiseType, setNoiseType] = useState('background');
    const [showSettings, setShowSettings] = useState(false);

    const [gameState, setGameState] = useState('intro');

    useEffect(() => {
        let pool = [];
        if (config.vocabularyLevel === 'docx_rich') {
            pool = [...VOCABULARY.categorization.docx_rich];
        } else if (config.vocabularyLevel === 'docx_simple') {
            pool = [...VOCABULARY.categorization.docx_simple];
        } else if (config.vocabularyLevel === 'rich') {
            pool = [...VOCABULARY.categorization.rich];
        } else {

            pool = [...VOCABULARY.categorization.base];
        }

        const shuffled = pool.sort(() => 0.5 - Math.random()).slice(0, 10);
        setItems(shuffled);
    }, [config]);

    const currentItem = items[currentStep];

    useEffect(() => {
        if (!currentItem) return;

        const catMap = {
            'animaux': 'حيوانات', 'fruits': 'فواكه', 'legumes': 'خضر', 'corps': 'جسم', 'transport': 'نقل',
            'maison': 'منزل', 'couleurs': 'ألوان', 'alimentation': 'مأكولات', 'vetements': 'ملابس', 'ecole': 'مدرسة'
        };

        const internalCats = Object.keys(catMap);
        const correctCat = { id: currentItem.category, label: catMap[currentItem.category] };

        const otherCats = internalCats
            .filter(c => c !== currentItem.category)
            .sort(() => 0.5 - Math.random())
            .slice(0, 2)
            .map(c => ({ id: c, label: catMap[c] }));

        const currentOptions = [correctCat, ...otherCats].sort(() => 0.5 - Math.random());
        setOptions(currentOptions);
        setFeedback(null);
    }, [currentItem]);

    const noiseWhiteRef = React.useRef(null);
    const noiseBgRef = React.useRef(null);
    const audioInstanceRef = React.useRef(null); // Reference to current playing word audio

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

        const audioId = currentItem.id.replace(/^[sr]_/, '');
        const audioPath = `${import.meta.env.BASE_URL}audio/words/${audioId}.mp3`;
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
            console.log("Using TTS fallback");
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

        const interval = setInterval(() => {
            playSound();
        }, 5000);

        return () => clearInterval(interval);
    }, [playSound, currentItem, gameState]);

    const handleChoice = (catId) => {
        if (feedback === 'correct') return;

        setAttempts(a => a + 1);

        if (catId === currentItem.category) {

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
            <audio ref={noiseWhiteRef} loop src={`${import.meta.env.BASE_URL}audio/noise_white.mp3`} />
            <audio ref={noiseBgRef} loop src={`${import.meta.env.BASE_URL}audio/noise_continu.mp3`} />

            {gameState !== 'intro' && (
                <>
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
                                    style={{ padding: '0.2rem', borderRadius: '50%', width: '30px', height: '30px', minHeight: 'auto' }}
                                >
                                    <Plus size={16} />
                                </button>
                            </div>
                        </div>
                    )}
                </>
            )}

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

                {!currentItem ? (
                    <div className="card" style={{ marginTop: '2rem', padding: '2rem' }}>
                        <h2>Chargement...</h2>
                    </div>
                ) : (
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
                            marginBottom: '0.5rem', animation: isPlaying ? 'pulse 1s infinite' : 'none'
                        }}>
                        <Volume2 size={32} />
                    </button>

                        <h2 style={{
                            marginBottom: '0.5rem',
                            fontFamily: 'var(--font-heading)',
                            fontSize: '1.5rem',
                            lineHeight: 1.2
                        }}>
                            Qu'est ce que tu as entendu ?
                        </h2>

                        {itemsImages[currentItem.word] && (
                            <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'center' }}>
                                {(() => {
                                    const imageFilename = itemsImages[currentItem.word];
                                    return (
                                <div style={{ marginBottom: '0.5rem', display: 'flex', justifyContent: 'center' }}>
                                    <img
                                        src={`${import.meta.env.BASE_URL}assets/images/items/${imageFilename}`}
                                        alt={currentItem.label}
                                        style={{
                                            width: '120px', height: '120px', objectFit: 'contain',
                                            borderRadius: '1rem', boxShadow: '0px 8px 15px rgba(0,0,0,0.15)',
                                            background: 'white', padding: '10px'
                                        }}
                                        onError={(e) => {
                                            if (!e.target.src.includes('/categories/')) {
                                                e.target.src = e.target.src.replace('/items/', '/categories/');
                                            }
                                        }}
                                    />
                                </div>
                            );
                        })()}
                            </div>
                        )}

                        <h3 className="title" style={{
                            fontSize: '1.2rem',
                            margin: '0.5rem 0',
                            textShadow: 'none',
                            color: 'var(--text-main)',
                            WebkitTextStroke: '0',
                            opacity: 0.8
                        }}>
                            Choisis la catégorie :
                        </h3>

                        <div className="options-grid" style={{
                            display: 'grid',
                            gap: '0.5rem',
                            width: '100%',
                            maxWidth: '1000px'
                        }}>
                            {options.map(opt => {
                                const CATEGORY_IMAGES = {
                                    'maison': `${import.meta.env.BASE_URL}assets/images/categories/maison.jpeg`,
                                    'alimentation': `${import.meta.env.BASE_URL}assets/images/categories/alimentation.jpeg`,
                                    'animaux': `${import.meta.env.BASE_URL}assets/images/categories/animaux.jpeg`,
                                    'fruits': `${import.meta.env.BASE_URL}assets/images/categories/fruits.jpeg`,
                                    'legumes': `${import.meta.env.BASE_URL}assets/images/categories/legumes.jpeg`,
                                    'corps': `${import.meta.env.BASE_URL}assets/images/categories/corps.jpeg`,
                                    'transport': `${import.meta.env.BASE_URL}assets/images/categories/transport.jpeg`,
                                    'vetements': `${import.meta.env.BASE_URL}assets/images/categories/vetements.jpeg`,
                                    'couleurs': `${import.meta.env.BASE_URL}assets/images/categories/couleurs.jpeg`,
                                    'ecole': `${import.meta.env.BASE_URL}assets/images/categories/ecole.jpg`,
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
                                        <span className="opt-label" style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>{opt.label}</span>
                                    </button>
                                );
                            })}
                        </div>

                        <style>{`
                        .options-grid { grid-template-columns: repeat(3, 1fr); gap: 1rem; }
                        .opt-btn { height: 130px; border-width: 2px !important; }
                        
                        .opt-icon-img {
                            width: 80px; height: 80px; object-fit: contain; margin-bottom: 0.5rem;
                            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));
                        }

                        @media (max-width: 768px) {
                            .options-grid { grid-template-columns: repeat(3, 1fr); gap: 0.5rem; }
                            .opt-btn { 
                                height: 100px; 
                                padding: 0.2rem !important;
                            }
                            .opt-icon { font-size: 2rem !important; }
                            .opt-icon-img {
                                width: 55px; height: 55px; margin-bottom: 0.1rem !important;
                            }
                            .opt-label { font-size: 0.9rem !important; }
                        }
                            .opt-label { font-size: 1rem !important; }
                        }
                    `}</style>
                    </div>
                )}
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
                        fontSize: '5rem', color: '#ef4444',
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
                    background: 'rgba(255,255,255,0.8)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    zIndex: 10, backdropFilter: 'blur(5px)'
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

export default Activity2;

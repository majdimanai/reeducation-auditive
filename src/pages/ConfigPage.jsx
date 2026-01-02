import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useGame } from '../context/GameContext';
import { VOCABULARY } from '../data/vocabulary';
import { Settings, Play, Volume2 } from 'lucide-react';

const ConfigPage = () => {
    const { activityId } = useParams();
    const navigate = useNavigate();
    const { setConfig, resetGame } = useGame();

    const [settings, setSettings] = useState({
        vocabLevel: 'docx_simple',
        contrast: 'b-m', // Default, will update on level change
        voiceGender: 'female' // New setting
    });

    // Reset contrast when level changes
    useEffect(() => {
        if (settings.vocabLevel === 'docx_simple' || settings.vocabLevel === 'base') {
            setSettings(s => ({ ...s, contrast: 'b-m' }));
        } else {
            setSettings(s => ({ ...s, contrast: 'ch-j' }));
        }
    }, [settings.vocabLevel]);

    const isAct1 = activityId === '1';

    const handleStart = () => {
        setConfig({
            activity: parseInt(activityId),
            vocabularyLevel: settings.vocabLevel,
            contrast: settings.contrast,
            voiceGender: settings.voiceGender
        });
        resetGame();
        navigate(`/activity${activityId}`);
    };

    return (
        <div className="container">
            <h1 className="title">Paramétrage Activité {activityId}</h1>

            <div className="card" style={{ textAlign: 'left' }}>
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem', color: 'var(--text-muted)' }}>
                    <Settings size={24} style={{ marginRight: '10px' }} />
                    <h3>Configuration de la séance</h3>
                </div>

                {/* Vocab Selection */}
                <div className="form-group">
                    <label>Niveau de Vocabulaire (Obligatoire)</label>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                        <button
                            className={`btn ${settings.vocabLevel === 'docx_simple' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setSettings({ ...settings, vocabLevel: 'docx_simple' })}
                            style={{ opacity: settings.vocabLevel === 'docx_simple' ? 1 : 0.6 }}
                        >
                            Base
                        </button>
                        <button
                            className={`btn ${settings.vocabLevel === 'docx_rich' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setSettings({ ...settings, vocabLevel: 'docx_rich' })}
                            style={{ opacity: settings.vocabLevel === 'docx_rich' ? 1 : 0.6 }}
                        >
                            Riche
                        </button>
                    </div>
                </div>

                {/* ACT 1: Contrast Selection */}
                {isAct1 && (
                    <div className="form-group" style={{ marginTop: '2rem' }}>
                        <label>Choisis une paire de sons :</label>
                        <select
                            style={{ display: 'block', width: '100%', padding: '0.8rem', borderRadius: '8px', marginTop: '0.5rem', fontSize: '1rem' }}
                            value={settings.contrast}
                            onChange={(e) => setSettings({ ...settings, contrast: e.target.value })}
                        >
                            {settings.vocabLevel === 'docx_simple' ? (
                                <>
                                    <option value="b-m">/b/ vs /m/</option>
                                    <option value="t-d">/t/ vs /d/</option>
                                </>
                            ) : (
                                <>
                                    <option value="ch-j">/ch/ vs /j/ (ش - ج)</option>
                                    <option value="k-g">/k/ vs /g/ (ك - ق)</option>
                                    <option value="f-v">/f/ vs /v/ (ف - v)</option>
                                    <option value="kh-h">/kh/ vs /h/ (خ - ه)</option>
                                </>
                            )}
                        </select>
                        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                            Exemples: {settings.contrast === 'b-m' ? 'Bab / Mama' : 'Toffeh / Dar'}
                        </p>
                    </div>
                )}

                {/* Voice Gender Selection */}
                <div className="form-group" style={{ marginTop: '2rem' }}>
                    <label>Voix (Homme/Femme)</label>
                    <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
                        <button
                            className={`btn ${settings.voiceGender === 'female' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setSettings({ ...settings, voiceGender: 'female' })}
                            style={{ opacity: settings.voiceGender === 'female' ? 1 : 0.6 }}
                        >
                            👩 Femme
                        </button>
                        <button
                            className={`btn ${settings.voiceGender === 'male' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setSettings({ ...settings, voiceGender: 'male' })}
                            style={{ opacity: settings.voiceGender === 'male' ? 1 : 0.6 }}
                        >
                            👨 Homme
                        </button>
                    </div>
                </div>

                {/* Noise Selection REMOVED per user request - moved in-game */}


                <div style={{ marginTop: '3rem', textAlign: 'center' }}>
                    <button className="btn btn-primary" onClick={handleStart} style={{ padding: '1rem 3rem', fontSize: '1.2rem' }}>
                        <Play size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
                        Lancer l'activité
                    </button>
                </div>

            </div>
        </div>
    );
};

export default ConfigPage;

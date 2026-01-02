import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
    return (
        <div className="container">
            <h1 className="title">Rééducation Auditive</h1>
            <p style={{ fontSize: '1.2rem', marginBottom: '3rem' }}>
                Bienvenue ! Choisissez une activité pour commencer.
            </p>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', maxWidth: '800px', margin: '0 auto' }}>
                <Link to="/config/1" className="card" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <h2 style={{ color: 'var(--primary)', marginTop: 0 }}>Activite 1</h2>
                    <p>Discrimination Phonémique</p>
                    <div className="btn btn-primary">Commencer</div>
                </Link>

                <Link to="/config/2" className="card" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <h2 style={{ color: 'var(--secondary)', marginTop: 0 }}>Activite 2</h2>
                    <p>Catégorisation Lexicale</p>
                    <div className="btn btn-secondary">Commencer</div>
                </Link>
            </div>
        </div>
    );
};

export default Home;

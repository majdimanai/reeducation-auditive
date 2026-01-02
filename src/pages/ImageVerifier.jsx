import React from 'react';

const ImageVerifier = () => {
    // Generate numbers 1 to 45 (approx number of images found)
    const images = Array.from({ length: 48 }, (_, i) => i + 1);

    return (
        <div style={{ padding: '20px', background: '#f0f0f0', minHeight: '100vh' }}>
            <h1>Vérification des Images</h1>
            <p>Regardez les images et dites-moi à quoi elles correspondent. (Exemple: "Image 1 c'est le Chien")</p>

            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))',
                gap: '20px'
            }}>
                {images.map(num => {
                    // Try both jpg and jpeg and png extensions (brute force rendering)
                    return (
                        <div key={num} style={{ background: 'white', padding: '10px', borderRadius: '8px', textAlign: 'center' }}>
                            <h3>Image {num}</h3>
                            <div style={{ position: 'relative', height: '120px' }}>
                                {/* Attempt to load multiple extensions, only one will show */}
                                <img src={`${import.meta.env.BASE_URL}assets/images/raw/image${num}.jpeg`} style={{ maxWidth: '100%', maxHeight: '100%', display: 'block', margin: '0 auto' }} onError={(e) => e.target.style.display = 'none'} />
                                <img src={`${import.meta.env.BASE_URL}assets/images/raw/image${num}.jpg`} style={{ maxWidth: '100%', maxHeight: '100%', display: 'block', margin: '0 auto', position: 'absolute', top: 0, left: 0, right: 0 }} onError={(e) => e.target.style.display = 'none'} />
                                <img src={`${import.meta.env.BASE_URL}assets/images/raw/image${num}.png`} style={{ maxWidth: '100%', maxHeight: '100%', display: 'block', margin: '0 auto', position: 'absolute', top: 0, left: 0, right: 0 }} onError={(e) => e.target.style.display = 'none'} />
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default ImageVerifier;

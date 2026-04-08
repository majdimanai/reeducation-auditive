const fs = require('fs');

// In a real environment we would import the file. Here we'll read it as a string and parse it roughly.
const vocabContent = fs.readFileSync('src/data/vocabulary.js', 'utf8');
const itemsImages = JSON.parse(fs.readFileSync('src/data/items_images.json', 'utf8'));

// Extract categorization labels and their mapped images
const labelToImg = {};
const catMatches = vocabContent.matchAll(/id:\s*['"]([^'"]+)['"],\s*word:\s*['"]([^'"]+)['"],\s*category:\s*['"]([^'"]+)['"],\s*label:\s*['"]([^'"]+)['"]/g);

// Also look for quotes variation
const catMatches2 = vocabContent.matchAll(/"id":\s*"([^"]+)",\s*"word":\s*"([^"]+)",\s*"category":\s*"([^"]+)",\s*"label":\s*"([^"]+)"/g);

for (const match of [...catMatches, ...catMatches2]) {
    const wordId = match[2];
    const label = match[4];
    if (itemsImages[wordId]) {
        labelToImg[label] = itemsImages[wordId];
    }
}

// Extract discrimination items
const discItems = [];
const discMatches = vocabContent.matchAll(/"id":\s*"([^"]+)",\s*"word":\s*"([^"]+)",\s*"phoneme":\s*"([^"]+)",\s*"label":\s*"([^"]+)"/g);

const updatedImages = { ...itemsImages };
let count = 0;

for (const match of discMatches) {
    const wordId = match[2];
    const label = match[4];

    if (labelToImg[label]) {
        updatedImages[wordId] = labelToImg[label];
        count++;
    } else {
        // Fallback heuristics for files in items directory
        const allFiles = fs.readdirSync('public/assets/images/items/');
        const normalizedLabel = label.replace(/[^\u0621-\u064A]/g, ''); // keep only arabic chars if needed

        // Manual heuristics for most common ones
        const heuristics = {
            "بانانا": "s_bannane.jpeg",
            "بحر": "bahar.jpeg",
            "بسكلات": "s_bisklet.jpeg",
            "دلاع": "s_della.jpeg",
            "تمر": "s_btamr.jpeg", // Wait, check file list
            "تفاح": "toffeh.jpeg",
            "توت": "tout.jpeg",
            "بصل": "bsol.jpeg",
            "بطاطا": "batata.jpeg",
            "بطة": "batta.jpeg",
            "بقرة": "bagra.jpeg",
            "دجاجة": "djaja.jpeg",
            "تلفزة": "talvza.jpeg",
            "كرسي": "korsi.jpeg",
            "كلب": "kelb.jpeg",
            "كلسيطة": "kalchita.jpeg",
            "فلفل": "felfel.jpeg",
            "فم": "fom.jpeg",
            "خبز": "khobz.png",
            "خشم": "khcham.jpeg"
        };

        if (heuristics[label]) {
            updatedImages[wordId] = heuristics[label];
            count++;
        }
    }
}

fs.writeFileSync('src/data/items_images.json', JSON.stringify(updatedImages, null, 4));
console.log(`Updated ${count} discrimination items.`);

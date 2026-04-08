import { VOCABULARY } from '../src/data/vocabulary.js';
import itemsImages from '../src/data/items_images.json' assert { type: 'json' };

const labelToImage = {};
Object.entries(VOCABULARY.categorization).forEach(([catKey, catList]) => {
    catList.forEach(item => {
        if (itemsImages[item.word]) {
            labelToImage[item.label] = itemsImages[item.word];
        } else if (itemsImages[item.id]) {
            labelToImage[item.label] = itemsImages[item.id];
        } else {
            const s_word = 's_' + item.word;
            if (itemsImages[s_word]) {
                labelToImage[item.label] = itemsImages[s_word];
            }
        }
    });
});

let missingCount = 0;
let totalCount = 0;

Object.entries(VOCABULARY.discrimination).forEach(([levelKey, levelObj]) => {
    Object.entries(levelObj).forEach(([pair, pairData]) => {
        pairData.words.forEach(item => {
            totalCount++;
            if (!labelToImage[item.label]) {
                console.log(`Missing image for label: ${item.label} (ID: ${item.id})`);
                missingCount++;
            }
        });
    });
});

console.log(`\nTotal items: ${totalCount}, Missing: ${missingCount}`);

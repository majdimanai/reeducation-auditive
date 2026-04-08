import json
import os
import difflib

# Paths
VOCAB_PATH = 'src/data/vocabulary.js'
IMAGES_JSON_PATH = 'src/data/items_images.json'
ITEMS_DIR = 'public/assets/images/items/'

def read_vocab():
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple extraction of categorization items from vocabulary.js
    # We'll use a regex-like approach to find mappings of label to word_id
    import re
    cat_items = re.findall(r'\"id\":\s*\"([^\"]+)\",\s*\"word\":\s*\"([^\"]+)\",\s*\"category\":\s*\"([^\"]+)\",\s*\"label\":\s*\"([^\"]+)\"', content)
    
    label_to_img_key = {}
    
    with open(IMAGES_JSON_PATH, 'r', encoding='utf-8') as f:
        images_json = json.load(f)
    
    for item in cat_items:
        word_id = item[1]
        label = item[3]
        if word_id in images_json:
            label_to_img_key[label] = images_json[word_id]
            
    # Also extract discrimination items
    disc_items = re.findall(r'\"id\":\s*\"([^\"]+)\",\s*\"word\":\s*\"([^\"]+)\",\s*\"phoneme\":\s*\"[^\"]+\",\s*\"label\":\s*\"([^\"]+)\"', content)
    
    return label_to_img_key, disc_items, images_json

def map_discrimination_images():
    label_to_img, disc_items, images_json = read_vocab()
    
    updated_images = dict(images_json)
    
    all_files = os.listdir(ITEMS_DIR)
    
    # Map labels to files directly as well
    label_to_file = {}
    # Common mappings (heuristics)
    mappings = {
        "بانانا": "bannane.jpeg",
        "بحر": "bahar.jpeg",
        "بسكلات": "bisklet.jpeg",
        "بحر": "bahar.jpeg", # Wait, I don't see bahar.jpeg in the list
    }
    
    # Try to find bahar or close matches
    for f in all_files:
        if 'bahar' in f.lower() or 'bhr' in f.lower(): label_to_file["بحر"] = f
        if 'banane' in f.lower(): label_to_file["بانانا"] = f
        if 'bisklet' in f.lower() or 'baisklet' in f.lower(): label_to_file["بسكلات"] = f
        if 'bouma' in f.lower(): label_to_file["بومة"] = f
        if 'ma' == f.lower().split('.')[0]: label_to_file["ماء"] = f
        if 'madrasa' in f.lower(): label_to_file["مدرسة"] = f
        if 'mothallah' in f.lower(): label_to_file["مثلث"] = f
        if 'mraya' in f.lower(): label_to_file["مراية"] = f
        if 'morabba3' in f.lower(): label_to_file["مربع"] = f
        if 'mishmish' in f.lower(): label_to_file["مشماش"] = f
        if 'mefta7' in f.lower() or 'mifta7' in f.lower(): label_to_file["مفتاح"] = f
        if 'dar' == f.lower().split('.')[0]: label_to_file["دار"] = f
        if 'deb' == f.lower().split('.')[0]: label_to_file["دب"] = f
        if 'dallaa' in f.lower(): label_to_file["دلاع"] = f
        if 'dawa' in f.lower(): label_to_file["دواء"] = f
        if 'telef' in f.lower(): label_to_file["تاليفون"] = f
        if 'tabki' in f.lower(): label_to_file["تبكي"] = f
        if 'tadhak' in f.lower(): label_to_file["تضحك"] = f
        if 'shappeau' in f.lower() or 'chapeau' in f.lower(): label_to_file["شابو"] = f
        if 'shajara' in f.lower() or 'chajara' in f.lower(): label_to_file["شجرة"] = f
        if 'shams' in f.lower() or 'chams' in f.lower(): label_to_file["شمس"] = f
        if 'sham3a' in f.lower() or 'cham3a' in f.lower(): label_to_file["شمعة"] = f
        if 'koora' in f.lower(): label_to_file["كورة"] = f
        if 'fraise' in f.lower() or 'fraz' in f.lower(): label_to_file["فراز"] = f
        if 'farasha' in f.lower(): label_to_file["فراشة"] = f
        if 'khoutem' in f.lower(): label_to_file["خاتم"] = f
        if 'khiz' in f.lower(): label_to_file["خزانة"] = f
        if 'khouch' in f.lower(): label_to_file["خوخ"] = f
        if 'khiar' in f.lower(): label_to_file["خيار"] = f
        if 'khit' == f.lower().split('.')[0]: label_to_file["خيط"] = f

    for disc_id, disc_word, disc_label in disc_items:
        # Check if mapped by label from categorization
        if disc_label in label_to_img:
            updated_images[disc_word] = label_to_img[disc_label]
        # Check if mapped by manual label-to-file
        elif disc_label in label_to_file:
             updated_images[disc_word] = label_to_file[disc_label]
        else:
            # Try fuzzy matching label with filenames or categories
            pass
            
    with open(IMAGES_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(updated_images, f, indent=4, ensure_ascii=False)
    
    print(f"Updated {IMAGES_JSON_PATH} with new mappings.")

if __name__ == '__main__':
    map_discrimination_images()

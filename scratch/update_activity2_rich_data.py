
import os
import shutil
import pandas as pd
import json
import subprocess
import re

# Paths
BASE_SOURCE = "/home/majdi/projet/newnewvocabulaire/vocabulaire riche/enregistrement  catégorisation vocbulaire complexe/"
EXCEL_PATH = os.path.join(BASE_SOURCE, "bd.ods")
AUDIO_SRC = os.path.join(BASE_SOURCE, "audio/")
IMAGES_SRC = os.path.join(BASE_SOURCE, "images/")
CATEGORY_SRC = os.path.join(BASE_SOURCE, "category/")

DEST_AUDIO = "/home/majdi/projet/public/audio/words/"
DEST_ITEMS_IMAGES = "/home/majdi/projet/public/assets/images/items/"
DEST_CAT_IMAGES = "/home/majdi/projet/public/assets/images/categories/"
VOCAB_JS = "/home/majdi/projet/src/data/vocabulary.js"
ITEMS_IMAGES_JSON = "/home/majdi/projet/src/data/items_images.json"

# Category mapping
CAT_MAP = {
    'منزل': 'maison',
    'طعام': 'alimentation',
    'الحيوانات': 'animaux',
    'الأشياء في المدرسة': 'ecole',
    'ملابس': 'vetements',
    'وسائل النقل': 'transport'
}

# Ensure destination directories exist
os.makedirs(DEST_AUDIO, exist_ok=True)
os.makedirs(DEST_ITEMS_IMAGES, exist_ok=True)
os.makedirs(DEST_CAT_IMAGES, exist_ok=True)

def process_audio(id, label):
    filesInDir = os.listdir(AUDIO_SRC)
    target = None
    for f in filesInDir:
        if label in f:
            target = f
            break
    if not target:
        return False
    src = os.path.join(AUDIO_SRC, target)
    dest = os.path.join(DEST_AUDIO, id + ".mp3")
    try:
        subprocess.run(["ffmpeg", "-y", "-i", src, "-acodec", "libmp3lame", dest], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error converting {target}: {e}")
        return False

def process_item_image(word_id, label):
    for ext in ['.jpg', '.png', '.jpeg']:
        src = os.path.join(IMAGES_SRC, label + ext)
        if os.path.exists(src):
            new_filename = word_id + ext
            shutil.copy2(src, os.path.join(DEST_ITEMS_IMAGES, new_filename))
            return new_filename
    return None

def process_categories():
    cat_images_map = {
        'منزل.jpg': 'maison.jpg',
        'طعام.jpg': 'alimentation.jpg',
        'الحيوانات.jpg': 'animaux.jpg',
        'الأشياء في المدرسة.jpg': 'ecole.jpg',
        'ملابس.jpg': 'vetements.jpg',
        'وسائل النقل.jpg': 'transport.jpg'
    }
    for src_name, dest_name in cat_images_map.items():
        src = os.path.join(CATEGORY_SRC, src_name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(DEST_CAT_IMAGES, dest_name))

def update_vocab(new_items):
    with open(VOCAB_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace categorization.rich
    pattern = r'("rich":\s*\[)(.*?)(\],)'
    
    new_rich_js = []
    for item in new_items:
        new_rich_js.append(json.dumps(item, ensure_ascii=False, indent=12))
    
    new_rich_str = ",\n".join(new_rich_js)
    
    def replacer(match):
        return match.group(1) + "\n" + new_rich_str + "\n        " + match.group(3)

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    with open(VOCAB_JS, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    print("Reading Excel...")
    df = pd.read_excel(EXCEL_PATH, engine='odf')
    
    new_vocab_items = []
    items_images_update = {}
    
    print("Processing items...")
    for i, row in df.iterrows():
        # Generate new Rich IDs to avoid overlap with base
        id = f"cat_r_anim_{i+1}"
        word = id
        label = row['label']
        category_ar = str(row['category']).strip()
        
        category_en = CAT_MAP.get(category_ar, 'unknown')
        if category_en == 'unknown':
            print(f"Warning: Unknown category '{category_ar}' for {label}")

        # Audio
        if process_audio(id, label):
            print(f"Processed audio for {label}")
        
        # Image
        image_fn = process_item_image(id, label)
        if image_fn:
            items_images_update[id] = image_fn
            print(f"Processed image for {label}")
        
        new_vocab_items.append({
            "id": id,
            "word": id,
            "category": category_en,
            "label": label
        })

    print("Updating categorization.rich in vocabulary.js...")
    update_vocab(new_vocab_items)
    
    print("Updating items_images.json...")
    with open(ITEMS_IMAGES_JSON, 'r') as f:
        try:
            current_map = json.load(f)
        except:
            current_map = {}
    current_map.update(items_images_update)
    with open(ITEMS_IMAGES_JSON, 'w') as f:
        json.dump(current_map, f, indent=4)
    
    print("Processing category images...")
    process_categories()
    
    print("Done!")

if __name__ == "__main__":
    main()

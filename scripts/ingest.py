import pandas as pd
import json
import glob
import os
import subprocess

CAT_MAP = {
    'طعام': 'alimentation', 'الحيوانات': 'animaux', 'الالوان': 'couleurs',
    'فواكه': 'fruits', 'خضراوات': 'legumes', 'وسائل النقل': 'transport',
    'اغراض المنزل': 'maison', 'جسم': 'corps', 'منزل': 'maison',
    'حيوانات': 'animaux', 'الاشياء في المدرسة': 'ecole',
    'اعضاء الجسم': 'corps', 'ملابس': 'vetements'
}

CONT_MAP = {
    'ب-م': 'b-m', 'د-ت': 'd-t', 'ت-د': 'd-t',
    'ش-ك': 'ch-k', 'ف-خ': 'f-kh'
}

def fix_id(val):
    return str(val).strip().replace(' ', '_').lower()

vocab = {
    "categorization": {"base": [], "rich": [], "docx_simple": [], "docx_rich": []},
    "discrimination": {"base": {}, "rich": {}}
}

items_images = {}

os.makedirs('public/assets/images/categories', exist_ok=True)
import shutil
if os.path.exists('public/audio/words'):
    shutil.rmtree('public/audio/words')
os.makedirs('public/audio/words', exist_ok=True)

def process_audio(src_dir, audio_relative, target_id):
    if pd.isna(audio_relative): return
    base_audio = os.path.basename(str(audio_relative)).strip()
    base_noext = os.path.splitext(base_audio)[0].strip()
    
    aud_dir = os.path.join(src_dir, 'audio')
    if not os.path.isdir(aud_dir): return
    
    possible = [os.path.join(aud_dir, f) for f in os.listdir(aud_dir) if base_noext in f or base_noext.replace(' ', '_') in f]
    
    if possible:
        target_file = f"public/audio/words/{target_id}.mp3"
        subprocess.run(['ffmpeg', '-y', '-i', possible[0], target_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("MISSING AUDIO:", base_noext)

def process_img(src_dir, label, target_word):
    # Some images might not be in excel but exist in the image dir by label
    possible = glob.glob(os.path.join(src_dir, 'images', f"{label}.*"))
    if possible:
        ext = os.path.splitext(possible[0])[1]
        target_file = f"public/assets/images/categories/{target_word}{ext}"
        import shutil
        shutil.copy(possible[0], target_file)
        
        # fallback without directories for JSON mapping
        return f"{target_word}{ext}"
    return None

# 1. Cat Base
df = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrement  catégorisation vocb base/bd.xlsx')
src_dir = 'bd_final/enregistrements vocabulaire de base/enregistrement  catégorisation vocb base'
for idx, row in df.iterrows():
    if pd.isna(row.get('label')) or pd.isna(row.get('category')): continue
    c = CAT_MAP.get(row['category'].strip(), row['category'].strip())
    # Generate unique IDs
    cid = f"cat_b_{idx}"
    word = f"word_b_{idx}"
    vocab["categorization"]["base"].append({"id": cid, "word": word, "category": c, "label": row['label'].strip()})
    
    # docx_simple duplicate
    vocab["categorization"]["docx_simple"].append({"id": f"s_{cid}", "word": f"s_{word}", "category": c, "label": row['label'].strip()})
    
    process_audio(src_dir, row.get('audio'), cid)
    process_audio(src_dir, row.get('audio'), f"s_{cid}")
    
    img = process_img(src_dir, row['label'].strip(), word)
    if img:
        items_images[word] = img
        items_images[f"s_{word}"] = img

# 2. Cat Rich
df = pd.read_excel('bd_final/enregistrement vocab riche/catégorisation/bd.xltx')
src_dir = 'bd_final/enregistrement vocab riche/catégorisation'
for idx, row in df.iterrows():
    if pd.isna(row.get('label')) or pd.isna(row.get('category')): continue
    c = CAT_MAP.get(row['category'].strip(), row['category'].strip())
    cid = f"cat_r_{idx}"
    word = f"word_r_{idx}"
    vocab["categorization"]["rich"].append({"id": cid, "word": word, "category": c, "label": row['label'].strip()})
    vocab["categorization"]["docx_rich"].append({"id": f"r_{cid}", "word": f"r_{word}", "category": c, "label": row['label'].strip()})
    
    process_audio(src_dir, row.get('audio'), cid)
    process_audio(src_dir, row.get('audio'), f"r_{cid}")
    
    img = process_img(src_dir, row['label'].strip(), word)
    if img:
        items_images[word] = img
        items_images[f"r_{word}"] = img

# 3. Disc Base
df = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrements discrimination vocabulaire de base/enregistrement discrimination/db.xltx')
src_dir = 'bd_final/enregistrements vocabulaire de base/enregistrements discrimination vocabulaire de base/enregistrement discrimination'
for idx, row in df.iterrows():
    c1, c2 = row['category'], row['category1']
    pair_val = c1 if '-' in str(c1) else c2
    phoneme_val = c2 if '-' in str(c1) else c1
    
    if pd.isna(pair_val) or pd.isna(phoneme_val): continue
    
    pair_id = CONT_MAP.get(pair_val.strip(), pair_val.strip())
    if pair_id not in vocab["discrimination"]["base"]:
        targets = pair_val.strip().split('-')
        vocab["discrimination"]["base"][pair_id] = {
            "target_1": targets[0], "target_2": targets[1] if len(targets)>1 else "", "words": []
        }
    
    cid = f"d_b_{idx}"
    word = f"d_word_b_{idx}"
    vocab["discrimination"]["base"][pair_id]["words"].append({
        "id": cid, "word": word, "phoneme": str(phoneme_val).strip(), "label": str(row.get('label', '')).strip()
    })
    process_audio(src_dir, row.get('audio'), cid)

# 4. Disc Rich
df = pd.read_excel('bd_final/enregistrement vocab riche/discrimination/bd.ods', engine='odf')
src_dir = 'bd_final/enregistrement vocab riche/discrimination'
for idx, row in df.iterrows():
    c1, c2 = row['category'], row['category1']
    pair_val = c1 if '-' in str(c1) else c2
    phoneme_val = c2 if '-' in str(c1) else c1
    
    if pd.isna(pair_val) or pd.isna(phoneme_val): continue
    
    pair_id = CONT_MAP.get(pair_val.strip(), pair_val.strip())
    if pair_id not in vocab["discrimination"]["rich"]:
        targets = pair_val.strip().split('-')
        vocab["discrimination"]["rich"][pair_id] = {
            "target_1": targets[0], "target_2": targets[1] if len(targets)>1 else "", "words": []
        }
    
    cid = f"d_r_{idx}"
    word = f"d_word_r_{idx}"
    vocab["discrimination"]["rich"][pair_id]["words"].append({
        "id": cid, "word": word, "phoneme": str(phoneme_val).strip(), "label": str(row.get('label', '')).strip()
    })
    process_audio(src_dir, row.get('audio'), cid)

# Write output vocab.js and images json
with open('src/data/vocabulary.js', 'w', encoding='utf-8') as f:
    f.write("export const VOCABULARY = " + json.dumps(vocab, indent=4, ensure_ascii=False) + ";\n")

with open('src/data/items_images.json', 'w', encoding='utf-8') as f:
    json.dump(items_images, f, indent=4, ensure_ascii=False)

print("Ingestion successful.")

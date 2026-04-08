import pandas as pd
import json
import glob
import os
import subprocess
import shutil

# Categories mapping
CAT_MAP = {
    'طعام': 'alimentation', 'الحيوانات': 'animaux', 'الالوان': 'couleurs',
    'فواكه': 'fruits', 'خضراوات': 'legumes', 'وسائل النقل': 'transport',
    'اغراض المنزل': 'maison', 'جسم': 'corps', 'منزل': 'maison',
    'حيوانات': 'animaux', 'الاشياء في المدرسة': 'ecole',
    'الادوات المدرسية': 'ecole',
    'اعضاء الجسم': 'corps', 'ملابس': 'vetements'
}

CONT_MAP = {
    'ب-م': 'b-m', 'د-ت': 'd-t', 'ت-د': 'd-t',
    'ش-ك': 'ch-k', 'ف-خ': 'f-kh'
}

REPLACEMENTS = {
    'عين': 'عينين',
    'بانانا': 'بانان',
    'بنان': 'بانان',
    'برقدان': 'بردقان',
    'بيسكلات': 'بسكلات'
}

vocab = {
    "categorization": {
        "base": [],
        "rich": [],
        "docx_simple": [],
        "docx_rich": []
    },
    "discrimination": {"base": {}, "rich": {}}
}

items_images = {}

# Ensure target directories exist
os.makedirs('public/assets/images/items', exist_ok=True)
if os.path.exists('public/audio/words'):
    shutil.rmtree('public/audio/words')
os.makedirs('public/audio/words', exist_ok=True)

def process_audio(src_dir, audio_relative, target_id, label=None, orig_label=None):
    if pd.isna(audio_relative): return
    base_audio = os.path.basename(str(audio_relative)).strip()
    base_noext = os.path.splitext(base_audio)[0].strip()
    
    aud_dir = os.path.join(src_dir, 'audio')
    if not os.path.isdir(aud_dir): return
    
    files = os.listdir(aud_dir)
    # Priority matching:
    # 1. Exact match by audio column (ignoring garbage characters)
    exact = [f for f in files if f.endswith(base_audio) or f.strip('').startswith(base_noext + '.')]
    
    # 2. Try by label or original label if audio column match failed
    if not exact:
        for l in [label, orig_label]:
            if l:
                matches = [f for f in files if l in f]
                if matches:
                    matches.sort(key=len)
                    exact = [matches[0]]
                    break
    
    if exact:
        possible = [os.path.join(aud_dir, exact[0])]
    else:
        # Fallback to fuzzy base_noext
        matches = [f for f in files if base_noext in f]
        matches.sort(key=len)
        if matches:
            possible = [os.path.join(aud_dir, matches[0])]
        else:
            return

    if possible:
        target_file = f"public/audio/words/{target_id}.mp3"
        subprocess.run(['ffmpeg', '-y', '-i', possible[0], target_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_img(src_dir, row, target_word):
    label = str(row.get('label', '')).strip()
    img_col = str(row.get('image', '')).strip()
    
    img_dir = os.path.join(src_dir, 'images')
    if not os.path.isdir(img_dir): return None
    
    files = os.listdir(img_dir)
    
    # Try by image column basename first
    if img_col and img_col != 'nan':
        img_basename = os.path.basename(img_col)
        img_noext = os.path.splitext(img_basename)[0]
        # Exact match for filename base
        matches = [f for f in files if os.path.splitext(f)[0] == img_noext]
        if matches:
            ext = os.path.splitext(matches[0])[1]
            target_name = f"{target_word}{ext}"
            shutil.copy(os.path.join(img_dir, matches[0]), os.path.join('public/assets/images/items', target_name))
            return target_name

    # Try by label
    if label:
        # Exact match for label
        matches = [f for f in files if os.path.splitext(f)[0] == label]
        if matches:
            ext = os.path.splitext(matches[0])[1]
            target_name = f"{target_word}{ext}"
            shutil.copy(os.path.join(img_dir, matches[0]), os.path.join('public/assets/images/items', target_name))
            return target_name
            
    return None

# 1. Cat Base
df = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrement  catégorisation vocb base/bd.xlsx')
src_dir = 'bd_final/enregistrements vocabulaire de base/enregistrement  catégorisation vocb base'
for idx, row in df.iterrows():
    if pd.isna(row.get('label')) or pd.isna(row.get('category')): continue
    
    orig_label = row['label'].strip()
    label = REPLACEMENTS.get(orig_label, orig_label)
        
    c = CAT_MAP.get(row['category'].strip(), row['category'].strip())
    cid = f"cat_b_{idx}"
    word = f"word_b_{idx}"
    vocab["categorization"]["base"].append({"id": cid, "word": word, "category": c, "label": label})
    vocab["categorization"]["docx_simple"].append({"id": f"s_{cid}", "word": f"s_{word}", "category": c, "label": label})
    
    process_audio(src_dir, row.get('audio'), cid, label=label, orig_label=orig_label)
    process_audio(src_dir, row.get('audio'), f"s_{cid}", label=label, orig_label=orig_label)
    
    # Try with new label first, then original
    row_copy = row.copy()
    row_copy['label'] = label
    img = process_img(src_dir, row_copy, word)
    if not img and label != orig_label:
        row_copy['label'] = orig_label
        img = process_img(src_dir, row_copy, word)
        
    if img:
        items_images[word] = img
        items_images[f"s_{word}"] = img

# 2. Cat Rich
df = pd.read_excel('bd_final/enregistrement vocab riche/catégorisation/db.xlsx')
src_dir = 'bd_final/enregistrement vocab riche/catégorisation'
for idx, row in df.iterrows():
    if pd.isna(row.get('label')) or pd.isna(row.get('category')): continue
    
    orig_label = row['label'].strip()
    label = REPLACEMENTS.get(orig_label, orig_label)
        
    c = CAT_MAP.get(row['category'].strip(), row['category'].strip())
    cid = f"cat_r_{idx}"
    word = f"word_r_{idx}"
    vocab["categorization"]["rich"].append({"id": cid, "word": word, "category": c, "label": label})
    vocab["categorization"]["docx_rich"].append({"id": f"s_{cid}", "word": f"s_{word}", "category": c, "label": label})
    
    process_audio(src_dir, row.get('audio'), cid, label=label, orig_label=orig_label)
    process_audio(src_dir, row.get('audio'), f"s_{cid}", label=label, orig_label=orig_label)
    
    row_copy = row.copy()
    row_copy['label'] = label
    img = process_img(src_dir, row_copy, word)
    if not img and label != orig_label:
        row_copy['label'] = orig_label
        img = process_img(src_dir, row_copy, word)
        
    if img:
        items_images[word] = img
        items_images[f"s_{word}"] = img

# 3. Disc Base
df = pd.read_excel('bd_final/enregistrements vocabulaire de base/enregistrements discrimination vocabulaire de base/enregistrement discrimination/db.xlsx') # Use .xlsx instead of .xltx if available
src_dir = 'bd_final/enregistrements vocabulaire de base/enregistrements discrimination vocabulaire de base/enregistrement discrimination'
for idx, row in df.iterrows():
    c1, c2 = row['category'], row['category1']
    pair_val = c1 if '-' in str(c1) else c2
    phoneme_val = c2 if '-' in str(c1) else c1
    if pd.isna(pair_val) or pd.isna(phoneme_val): continue
    
    orig_label = str(row.get('label', '')).strip()
    label = REPLACEMENTS.get(orig_label, orig_label)
        
    pair_id = CONT_MAP.get(pair_val.strip(), pair_val.strip())
    if pair_id not in vocab["discrimination"]["base"]:
        targets = pair_val.strip().split('-')
        vocab["discrimination"]["base"][pair_id] = {
            "target_1": targets[0], "target_2": targets[1] if len(targets)>1 else "", "words": []
        }
    
    cid = f"d_b_{idx}"
    word = f"d_word_b_{idx}"
    
    vocab["discrimination"]["base"][pair_id]["words"].append({
        "id": cid, "word": word, "phoneme": str(phoneme_val).strip(), "label": label
    })
    process_audio(src_dir, row.get('audio'), cid, label=label, orig_label=orig_label)
    
    row_copy = row.copy()
    row_copy['label'] = label
    img = process_img(src_dir, row_copy, word)
    if not img and label != orig_label:
        row_copy['label'] = orig_label
        img = process_img(src_dir, row_copy, word)
    if img:
        items_images[word] = img

# 3. Disc Rich
df = pd.read_excel('bd_final/enregistrement vocab riche/discrimination/bd.ods', engine='odf')
src_dir = 'bd_final/enregistrement vocab riche/discrimination'
for idx, row in df.iterrows():
    c1, c2 = row['category'], row['category1']
    pair_val = c1 if '-' in str(c1) else c2
    phoneme_val = c2 if '-' in str(c1) else c1
    if pd.isna(pair_val) or pd.isna(phoneme_val): continue
    
    orig_label = str(row.get('label', '')).strip()
    label = REPLACEMENTS.get(orig_label, orig_label)
        
    pair_id = CONT_MAP.get(pair_val.strip(), pair_val.strip())
    if pair_id not in vocab["discrimination"]["rich"]:
        targets = pair_val.strip().split('-')
        vocab["discrimination"]["rich"][pair_id] = {
            "target_1": targets[0], "target_2": targets[1] if len(targets)>1 else "", "words": []
        }
    
    cid = f"d_r_{idx}"
    word = f"d_word_r_{idx}"
    
    vocab["discrimination"]["rich"][pair_id]["words"].append({
        "id": cid, "word": word, "phoneme": str(phoneme_val).strip(), "label": label
    })
    process_audio(src_dir, row.get('audio'), cid, label=label, orig_label=orig_label)
    
    row_copy = row.copy()
    row_copy['label'] = label
    img = process_img(src_dir, row_copy, word)
    if not img and label != orig_label:
        row_copy['label'] = orig_label
        img = process_img(src_dir, row_copy, word)
    if img:
        items_images[word] = img

# 4. Migrate Preserved Rich Categorization Images
# Move existing word_r_ images from categories to items
if os.path.exists('public/assets/images/categories'):
    for f in os.listdir('public/assets/images/categories'):
        if f.startswith('word_r_') or f.startswith('r_word_r_'):
            shutil.copy(os.path.join('public/assets/images/categories', f), os.path.join('public/assets/images/items', f))
            # Also keep old mappings in items_images.json if they exist
            # But wait, I'll just keep the existing items_images for them if they are in the JSON
            pass

# Load existing items_images.json to preserve rich categorization mappings
if os.path.exists('src/data/items_images.json'):
    with open('src/data/items_images.json', 'r', encoding='utf-8') as f:
        old_images = json.load(f)
        for k, v in old_images.items():
            if k.startswith('word_r_') or k.startswith('r_word_r_'):
                items_images[k] = v

# Write final files
with open('src/data/vocabulary.js', 'w', encoding='utf-8') as f:
    # Ensure ensuring_ascii=False for Arabic characters
    json_str = json.dumps(vocab, indent=4, ensure_ascii=False)
    f.write("export const VOCABULARY = " + json_str + ";\n")

with open('src/data/items_images.json', 'w', encoding='utf-8') as f:
    json.dump(items_images, f, indent=4, ensure_ascii=False)

print("Ingestion successful.")

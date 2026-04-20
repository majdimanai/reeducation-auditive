#!/usr/bin/env python3
"""
Migration script: newnewvocabulaire -> vocabulary.js + items_images.json + audio/images assets
Garde exactement la même logique/structure, remplace uniquement les données.
"""

import os
import shutil
import json

BASE = '/home/majdi/projet'
NEW_BASE = f'{BASE}/newnewvocabulaire'

# Chemins sources
CAT_SIMPLE_DIR  = f'{NEW_BASE}/vocabulaire de base/enregistrement  catégorisation vocbulaire simple'
CAT_RICHE_DIR   = f'{NEW_BASE}/vocabulaire riche/enregistrement  catégorisation vocbulaire complexe'
DISC_BASE_DIR   = f'{NEW_BASE}/vocabulaire de base/enregistrements discrimination vocabulaire de base'
DISC_RICHE_DIR  = f'{NEW_BASE}/vocabulaire riche/enregistrements discrimination vocabulaire riche'

# Chemins destination
DEST_AUDIO = f'{BASE}/public/audio/words'
DEST_IMAGES = f'{BASE}/public/assets/images/items'

os.makedirs(DEST_AUDIO, exist_ok=True)
os.makedirs(DEST_IMAGES, exist_ok=True)

# ── Mapping catégorie arabe → code interne ─────────────────────────────────
CAT_MAP_SIMPLE = {
    'أثاث المنزل': 'maison',
    'أعضاء الجسم': 'corps',
    'الألوان':     'couleurs',
    'الحيوانات':   'animaux',
    'الخضر':       'legumes',
    'الغلال':      'fruits',
    'فطور الصباح': 'alimentation',
}
CAT_MAP_RICHE = {
    'منزل':                  'maison',
    'طعام ':                 'alimentation',
    'طعام':                  'alimentation',
    'الحيوانات ':            'animaux',
    'الحيوانات':             'animaux',
    'الأشياء في المدرسة ':  'ecole',
    'الأشياء في المدرسة':   'ecole',
    'ملابس ':                'vetements',
    'ملابس':                 'vetements',
    'وسائل النقل ':          'transport',
    'وسائل النقل':           'transport',
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: copier un fichier audio .m4a.mp4 → destination en .mp3 (renommé)
# ─────────────────────────────────────────────────────────────────────────────
def copy_audio(src_dir, filename, dest_name):
    """Copie src_dir/filename -> DEST_AUDIO/dest_name"""
    src = os.path.join(src_dir, filename)
    dst = os.path.join(DEST_AUDIO, dest_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        return True
    return False

def copy_image(src_dir, filename, dest_name):
    """Copie src_dir/filename -> DEST_IMAGES/dest_name"""
    src = os.path.join(src_dir, filename)
    dst = os.path.join(DEST_IMAGES, dest_name)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        return True
    return False

# ─────────────────────────────────────────────────────────────────────────────
# Trouver un fichier audio par le mot arabe (tolérant sur le préfixe bizarre)
# ─────────────────────────────────────────────────────────────────────────────
def find_audio_file(audio_dir, word):
    """Cherche un fichier audio dont le nom contient 'word' dans audio_dir."""
    word = word.strip()
    for f in os.listdir(audio_dir):
        # Nettoyer le nom (enlever les chars non-arabes en début)
        clean = f.encode('utf-8').decode('utf-8')
        # On cherche le mot dans le nom du fichier
        if word in clean:
            return f
    return None

def find_image_file(img_dir, word):
    """Cherche une image dont le nom commence par 'word'."""
    word = word.strip()
    for f in os.listdir(img_dir):
        name_no_ext = os.path.splitext(f)[0].strip()
        if name_no_ext == word:
            return f
    return None

# ─────────────────────────────────────────────────────────────────────────────
# Lecture ODS (simple extraction XML)
# ─────────────────────────────────────────────────────────────────────────────
import zipfile, re

def read_ods_cells(ods_path):
    with zipfile.ZipFile(ods_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')
    cells = re.findall(r'<table:table-cell[^>]*><text:p>(.*?)</text:p></table:table-cell>', content)
    return cells

def parse_ods_rows(ods_path, n_cols):
    """Parse l'ODS en lignes de n_cols colonnes, skip header."""
    cells = read_ods_cells(ods_path)
    rows = []
    for i in range(0, len(cells), n_cols):
        row = cells[i:i+n_cols]
        if len(row) == n_cols:
            rows.append(row)
    # Skip header
    if rows and rows[0][0] == 'id':
        rows = rows[1:]
    return rows

# ═════════════════════════════════════════════════════════════════════════════
# 1. CATÉGORISATION SIMPLE (base)
# ═════════════════════════════════════════════════════════════════════════════
print("=== CATÉGORISATION SIMPLE ===")
cat_simple_audio_dir  = f'{CAT_SIMPLE_DIR}/audio'
cat_simple_images_dir = f'{CAT_SIMPLE_DIR}/images'

rows_cat_simple = parse_ods_rows(f'{CAT_SIMPLE_DIR}/bd.ods', 6)
# cols: id, word(=label), label, category, audio, image

cat_base = []
for i, row in enumerate(rows_cat_simple):
    _, word, label, category_ar, audio_ref, image_ref = row
    word = word.strip()
    label = label.strip()
    category_ar = category_ar.strip()
    category = CAT_MAP_SIMPLE.get(category_ar, category_ar)
    
    # IDs
    word_id  = f'cat_b_{i}'
    audio_id = f'cat_b_{i}'
    
    cat_base.append({
        'id':       f'cat_b_{i}',
        'word':     word_id,
        'category': category,
        'label':    label,
    })
    
    # Copier audio
    audio_file = find_audio_file(cat_simple_audio_dir, word)
    if audio_file:
        copy_audio(cat_simple_audio_dir, audio_file, f'{audio_id}.mp3')
        print(f"  ✓ audio cat_b_{i} <- {audio_file}")
    else:
        print(f"  ✗ audio MANQUANT pour '{word}'")
    
    # Copier image
    img_file = find_image_file(cat_simple_images_dir, word)
    if img_file:
        ext = os.path.splitext(img_file)[1]
        copy_image(cat_simple_images_dir, img_file, f'{word_id}{ext}')
        print(f"  ✓ image {word_id}{ext} <- {img_file}")
    else:
        print(f"  ✗ image MANQUANTE pour '{word}'")

# ═════════════════════════════════════════════════════════════════════════════
# 2. CATÉGORISATION RICHE
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== CATÉGORISATION RICHE ===")
cat_riche_audio_dir  = f'{CAT_RICHE_DIR}/audio'
cat_riche_images_dir = f'{CAT_RICHE_DIR}/images'

rows_cat_riche = parse_ods_rows(f'{CAT_RICHE_DIR}/bd.ods', 6)

cat_rich = []
for i, row in enumerate(rows_cat_riche):
    _, word, label, category_ar, audio_ref, image_ref = row
    word = word.strip()
    label = label.strip()
    category_ar = category_ar.strip()
    category = CAT_MAP_RICHE.get(category_ar, category_ar)
    
    word_id  = f'cat_r_{i}'
    audio_id = f'cat_r_{i}'
    
    cat_rich.append({
        'id':       f'cat_r_{i}',
        'word':     word_id,
        'category': category,
        'label':    label,
    })
    
    # Copier audio
    audio_file = find_audio_file(cat_riche_audio_dir, word)
    if audio_file:
        copy_audio(cat_riche_audio_dir, audio_file, f'{audio_id}.mp3')
        print(f"  ✓ audio cat_r_{i} <- {audio_file}")
    else:
        print(f"  ✗ audio MANQUANT pour '{word}'")
    
    # Copier image
    img_file = find_image_file(cat_riche_images_dir, word)
    if img_file:
        ext = os.path.splitext(img_file)[1]
        copy_image(cat_riche_images_dir, img_file, f'{word_id}{ext}')
        print(f"  ✓ image {word_id}{ext} <- {img_file}")
    else:
        print(f"  ✗ image MANQUANTE pour '{word}'")

# ═════════════════════════════════════════════════════════════════════════════
# 3. DISCRIMINATION BASE (b-m et d-t)
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== DISCRIMINATION BASE ===")
disc_base_audio_dir  = f'{DISC_BASE_DIR}/audio'
disc_base_images_dir = f'{DISC_BASE_DIR}/images'

rows_disc_base = parse_ods_rows(f'{DISC_BASE_DIR}/bd.ods', 7)
# cols: id, word, label, phoneme, pair(b-m/d-t), audio, image

disc_base_bm = {'target_1': 'ب', 'target_2': 'م', 'words': []}
disc_base_dt = {'target_1': 'د', 'target_2': 'ت', 'words': []}

global_disc_idx = 0
for i, row in enumerate(rows_disc_base):
    _, word, label, phoneme, pair, audio_ref, image_ref = row
    word = word.strip()
    label = label.strip()
    phoneme = phoneme.strip()
    pair = pair.strip()
    
    word_id  = f'd_b_{i}'
    audio_id = f'd_b_{i}'
    
    entry = {
        'id':      f'd_b_{i}',
        'word':    word_id,
        'phoneme': phoneme,
        'label':   label,
    }
    
    if pair == 'ب-م':
        disc_base_bm['words'].append(entry)
    elif pair == 'د-ت':
        disc_base_dt['words'].append(entry)
    
    # Copier audio
    audio_file = find_audio_file(disc_base_audio_dir, word)
    if audio_file:
        copy_audio(disc_base_audio_dir, audio_file, f'{audio_id}.mp3')
        print(f"  ✓ audio d_b_{i} <- {audio_file}")
    else:
        print(f"  ✗ audio MANQUANT pour '{word}'")
    
    # Copier image
    img_file = find_image_file(disc_base_images_dir, word)
    if img_file:
        ext = os.path.splitext(img_file)[1]
        copy_image(disc_base_images_dir, img_file, f'{word_id}{ext}')
        print(f"  ✓ image {word_id}{ext} <- {img_file}")
    else:
        print(f"  ✗ image MANQUANTE pour '{word}'")

# ═════════════════════════════════════════════════════════════════════════════
# 4. DISCRIMINATION RICHE (ش-ج et س-ز)
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== DISCRIMINATION RICHE ===")
disc_riche_audio_dir  = f'{DISC_RICHE_DIR}/audio'
disc_riche_images_dir = f'{DISC_RICHE_DIR}/images'

rows_disc_riche = parse_ods_rows(f'{DISC_RICHE_DIR}/bd.ods', 7)
# cols: id, word, label, phoneme, pair(ش-ج/س-ز), audio, image

disc_rich_shj = {'target_1': 'ش', 'target_2': 'ج', 'words': []}
disc_rich_sz  = {'target_1': 'س', 'target_2': 'ز', 'words': []}

for i, row in enumerate(rows_disc_riche):
    _, word, label, phoneme, pair, audio_ref, image_ref = row
    word = word.strip()
    label = label.strip()
    phoneme = phoneme.strip()
    pair = pair.strip()
    
    word_id  = f'd_r_{i}'
    audio_id = f'd_r_{i}'
    
    entry = {
        'id':      f'd_r_{i}',
        'word':    word_id,
        'phoneme': phoneme,
        'label':   label,
    }
    
    if pair == 'ش-ج':
        disc_rich_shj['words'].append(entry)
    elif pair == 'س-ز':
        disc_rich_sz['words'].append(entry)
    
    # Copier audio
    audio_file = find_audio_file(disc_riche_audio_dir, word)
    if audio_file:
        copy_audio(disc_riche_audio_dir, audio_file, f'{audio_id}.mp3')
        print(f"  ✓ audio d_r_{i} <- {audio_file}")
    else:
        print(f"  ✗ audio MANQUANT pour '{word}'")
    
    # Copier image (chercher dans les sous-dossiers)
    img_file = find_image_file(disc_riche_images_dir, word)
    if img_file:
        ext = os.path.splitext(img_file)[1]
        copy_image(disc_riche_images_dir, img_file, f'{word_id}{ext}')
        print(f"  ✓ image {word_id}{ext} <- {img_file}")
    else:
        print(f"  ✗ image MANQUANTE pour '{word}'")

# ═════════════════════════════════════════════════════════════════════════════
# 5. AUSSI copier docx_simple et docx_rich (mêmes données que base/rich)
#    On utilise des IDs préfixés s_ comme avant
# ═════════════════════════════════════════════════════════════════════════════

# docx_simple = même mots que cat_base mais IDs s_cat_b_N et s_word_b_N
cat_docx_simple = []
for i, entry in enumerate(cat_base):
    cat_docx_simple.append({
        'id':       f's_cat_b_{i}',
        'word':     f's_word_b_{i}',
        'category': entry['category'],
        'label':    entry['label'],
    })
    # Copier l'audio aussi avec le préfixe s_
    src = os.path.join(DEST_AUDIO, f'cat_b_{i}.mp3')
    dst = os.path.join(DEST_AUDIO, f's_cat_b_{i}.mp3')
    if os.path.exists(src):
        shutil.copy2(src, dst)
    # Copier image aussi
    for ext in ['.jpg', '.jpeg', '.jfif', '.png']:
        src_img = os.path.join(DEST_IMAGES, f'cat_b_{i}{ext}')
        if os.path.exists(src_img):
            dst_img = os.path.join(DEST_IMAGES, f's_word_b_{i}{ext}')
            shutil.copy2(src_img, dst_img)
            break

# docx_rich = même mots que cat_rich mais IDs s_cat_r_N et s_word_r_N
cat_docx_rich = []
for i, entry in enumerate(cat_rich):
    cat_docx_rich.append({
        'id':       f's_cat_r_{i}',
        'word':     f's_word_r_{i}',
        'category': entry['category'],
        'label':    entry['label'],
    })
    # Copier l'audio aussi
    src = os.path.join(DEST_AUDIO, f'cat_r_{i}.mp3')
    dst = os.path.join(DEST_AUDIO, f's_cat_r_{i}.mp3')
    if os.path.exists(src):
        shutil.copy2(src, dst)
    # Copier image
    for ext in ['.jpg', '.jpeg', '.jfif', '.png']:
        src_img = os.path.join(DEST_IMAGES, f'cat_r_{i}{ext}')
        if os.path.exists(src_img):
            dst_img = os.path.join(DEST_IMAGES, f's_word_r_{i}{ext}')
            shutil.copy2(src_img, dst_img)
            break

# ═════════════════════════════════════════════════════════════════════════════
# 6. Générer vocabulary.js
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== Génération vocabulary.js ===")

def entries_to_js(entries, indent=3):
    lines = []
    pad = '    ' * indent
    for entry in entries:
        lines.append(f'{pad}{{')
        lines.append(f'{pad}    "id": "{entry["id"]}",')
        lines.append(f'{pad}    "word": "{entry["word"]}",')
        lines.append(f'{pad}    "category": "{entry["category"]}",')
        lines.append(f'{pad}    "label": "{entry["label"]}"')
        lines.append(f'{pad}}},')
    # Remove trailing comma on last
    if lines:
        lines[-1] = lines[-1].rstrip(',')
    return '\n'.join(lines)

def disc_pair_to_js(pair_data, indent=3):
    """Convert discrimination pair dict to JS."""
    pad = '    ' * indent
    pad2 = '    ' * (indent + 1)
    lines = []
    lines.append(f'{pad}"target_1": "{pair_data["target_1"]}",')
    lines.append(f'{pad}"target_2": "{pair_data["target_2"]}",')
    lines.append(f'{pad}"words": [')
    for word in pair_data['words']:
        lines.append(f'{pad2}{{')
        lines.append(f'{pad2}    "id": "{word["id"]}",')
        lines.append(f'{pad2}    "word": "{word["word"]}",')
        lines.append(f'{pad2}    "phoneme": "{word["phoneme"]}",')
        lines.append(f'{pad2}    "label": "{word["label"]}"')
        lines.append(f'{pad2}}},')
    # Fix last comma
    if lines and lines[-1].endswith(','):
        lines[-1] = lines[-1].rstrip(',')
    lines.append(f'{pad}]')
    return '\n'.join(lines)

vocab_js = '''export const VOCABULARY = {
    "categorization": {
        "base": [
%s
        ],
        "rich": [
%s
        ],
        "docx_simple": [
%s
        ],
        "docx_rich": [
%s
        ]
    },
    "discrimination": {
        "base": {
            "b-m": {
%s
            },
            "d-t": {
%s
            }
        },
        "rich": {
            "ch-k": {
%s
            },
            "f-kh": {
%s
            }
        }
    }
};
''' % (
    entries_to_js(cat_base),
    entries_to_js(cat_rich),
    entries_to_js(cat_docx_simple),
    entries_to_js(cat_docx_rich),
    disc_pair_to_js(disc_base_bm),
    disc_pair_to_js(disc_base_dt),
    disc_pair_to_js(disc_rich_shj),
    disc_pair_to_js(disc_rich_sz),
)

with open(f'{BASE}/src/data/vocabulary.js', 'w', encoding='utf-8') as f:
    f.write(vocab_js)

print("  ✓ vocabulary.js écrit")

# ═════════════════════════════════════════════════════════════════════════════
# 7. Générer items_images.json
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== Génération items_images.json ===")

items_images = {}

def find_img_in_dest(word_key):
    """Cherche l'image dans DEST_IMAGES par le word_key."""
    for ext in ['.jpg', '.jpeg', '.jfif', '.png']:
        fname = f'{word_key}{ext}'
        if os.path.exists(os.path.join(DEST_IMAGES, fname)):
            return fname
    return None

# Catégorisation base (word = cat_b_N, aussi word_b_N pour compatibilité)
for i, entry in enumerate(cat_base):
    wid = f'cat_b_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[wid] = img
        # Aussi avec word_b_N pour rétro-compatibilité
        items_images[f'word_b_{i}'] = img

# Catégorisation simple docx (s_word_b_N)
for i, entry in enumerate(cat_docx_simple):
    wid = f's_word_b_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[wid] = img

# Catégorisation rich (cat_r_N, word_r_N)
for i, entry in enumerate(cat_rich):
    wid = f'cat_r_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[wid] = img
        items_images[f'word_r_{i}'] = img

# Catégorisation rich docx (s_word_r_N)
for i, entry in enumerate(cat_docx_rich):
    wid = f's_word_r_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[wid] = img

# Discrimination base (d_word_b_N)
for i in range(len(rows_disc_base)):
    wid = f'd_b_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[f'd_word_b_{i}'] = img
        items_images[wid] = img

# Discrimination rich (d_word_r_N)
for i in range(len(rows_disc_riche)):
    wid = f'd_r_{i}'
    img = find_img_in_dest(wid)
    if img:
        items_images[f'd_word_r_{i}'] = img
        items_images[wid] = img

with open(f'{BASE}/src/data/items_images.json', 'w', encoding='utf-8') as f:
    json.dump(items_images, f, ensure_ascii=False, indent=4)

print(f"  ✓ items_images.json écrit ({len(items_images)} entrées)")

# ═════════════════════════════════════════════════════════════════════════════
# 8. Résumé final
# ═════════════════════════════════════════════════════════════════════════════
print("\n=== RÉSUMÉ ===")
print(f"  Catégorisation base    : {len(cat_base)} mots")
print(f"  Catégorisation rich    : {len(cat_rich)} mots")
print(f"  Discrimination base bm : {len(disc_base_bm['words'])} mots")
print(f"  Discrimination base dt : {len(disc_base_dt['words'])} mots")
print(f"  Discrimination rich shj: {len(disc_rich_shj['words'])} mots")
print(f"  Discrimination rich sz : {len(disc_rich_sz['words'])} mots")
print("\nMigration terminée ✓")

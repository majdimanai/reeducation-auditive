
import re
import os
import json
import shutil

# 1. Read the ordered rIds from rids.txt
with open('rids.txt', 'r') as f:
    content = f.read()
    # Extract just the rId identifiers
    ordered_rids = re.findall(r'r:embed="(rId\d+)"', content)

# 2. Read the mapping from rels.xml
with open('rels.xml', 'r') as f:
    rels_content = f.read()
    # parse <Relationship Id="rIdX" Target="media/imageY.jpeg" ... />
    # We use regex for simplicity as it is a simple XML
    rels_map = {}
    matches = re.findall(r'Id="(rId\d+)".*?Target="media/(.*?)"', rels_content)
    for rid, target in matches:
        rels_map[rid] = target

# 3. Get the list of images in order of appearance
ordered_images = []
for rid in ordered_rids:
    if rid in rels_map:
        ordered_images.append(rels_map[rid])

print(f"Found {len(ordered_images)} images in document order.")

# 4. Define the vocabulary list (Manually extracted from vocabulary.js to ensure order)
# Order from vocabulary.js:
# Animaux (7), Fruits (6), Legumes (5), Corps (8), Transport (5), Maison (5), Couleurs (4), Alimentation (5)
vocab_order = [
    # Animaux
    'kelb', 'gatoussa', 'batta', 'bagra', 'djaja', 'houta', 'arnoub',
    # Fruits
    'toffeh', 'bordguela', 'della', 'bannane', 'anzas', 'tout',
    # Legumes
    'sfenaria', 'batata', 'bsol', 'tmatem', 'felfel',
    # Corps
    'yed', '3in', 'khcham', 'fom', 'seg', 'ch3ar', 'wdhen', '7wajeb',
    # Transport
    'karhba', 'kar', 'bisklet', 'metro', 'tayara',
    # Maison
    'srir', 'korsi', 'tawla', 'ghassala', 'beb',
    # Couleurs
    'a7mar', 'azra9', 'asfar', 'akhdhar',
    # Alimentation
    '7lib', '3dham', 'zebda', 'yaghorta', 'khobz'
]

print(f"Vocabulary list has {len(vocab_order)} items.")

if len(ordered_images) != len(vocab_order):
    print("WARNING: Count mismatch! Proceeding with caution.")

# 5. Copy and rename images
output_dir = 'public/assets/images/items'
os.makedirs(output_dir, exist_ok=True)

source_dir = 'temp_doc_extracted/word/media'

image_map = {}

for i, word in enumerate(vocab_order):
    if i < len(ordered_images):
        img_filename = ordered_images[i]
        src_path = os.path.join(source_dir, img_filename)
        
        # Determine extension
        ext = os.path.splitext(img_filename)[1]
        dest_filename = f"{word}{ext}" # keep original extension (jpg/png)
        dest_path = os.path.join(output_dir, dest_filename)
        
        try:
            shutil.copy2(src_path, dest_path)
            # Add to map
            image_map[word] = dest_filename
            print(f"Mapped {img_filename} -> {dest_filename}")
        except FileNotFoundError:
            print(f"Error: Could not find {src_path}")

# 6. Save map to JSON
map_path = 'src/data/items_images.json'
with open(map_path, 'w') as f:
    json.dump(image_map, f, indent=4)

print(f"Saved image map to {map_path}")

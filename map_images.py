
import re
import os
import json
import shutil

with open('rids.txt', 'r') as f:
    content = f.read()

    ordered_rids = re.findall(r'r:embed="(rId\d+)"', content)

with open('rels.xml', 'r') as f:
    rels_content = f.read()

    rels_map = {}
    matches = re.findall(r'Id="(rId\d+)".*?Target="media/(.*?)"', rels_content)
    for rid, target in matches:
        rels_map[rid] = target

ordered_images = []
for rid in ordered_rids:
    if rid in rels_map:
        ordered_images.append(rels_map[rid])

print(f"Found {len(ordered_images)} images in document order.")

vocab_order = [

    'kelb', 'gatoussa', 'batta', 'bagra', 'djaja', 'houta', 'arnoub',

    'toffeh', 'bordguela', 'della', 'bannane', 'anzas', 'tout',

    'sfenaria', 'batata', 'bsol', 'tmatem', 'felfel',

    'yed', '3in', 'khcham', 'fom', 'seg', 'ch3ar', 'wdhen', '7wajeb',

    'karhba', 'kar', 'bisklet', 'metro', 'tayara',

    'srir', 'korsi', 'tawla', 'ghassala', 'beb',

    'a7mar', 'azra9', 'asfar', 'akhdhar',

    '7lib', '3dham', 'zebda', 'yaghorta', 'khobz'
]

print(f"Vocabulary list has {len(vocab_order)} items.")

if len(ordered_images) != len(vocab_order):
    print("WARNING: Count mismatch! Proceeding with caution.")

output_dir = 'public/assets/images/items'
os.makedirs(output_dir, exist_ok=True)

source_dir = 'temp_doc_extracted/word/media'

image_map = {}

for i, word in enumerate(vocab_order):
    if i < len(ordered_images):
        img_filename = ordered_images[i]
        src_path = os.path.join(source_dir, img_filename)

        ext = os.path.splitext(img_filename)[1]
        dest_filename = f"{word}{ext}"
        dest_path = os.path.join(output_dir, dest_filename)
        
        try:
            shutil.copy2(src_path, dest_path)

            image_map[word] = dest_filename
            print(f"Mapped {img_filename} -> {dest_filename}")
        except FileNotFoundError:
            print(f"Error: Could not find {src_path}")

map_path = 'src/data/items_images.json'
with open(map_path, 'w') as f:
    json.dump(image_map, f, indent=4)

print(f"Saved image map to {map_path}")


import json
import os
import shutil
import re

vocab_file = 'src/data/vocabulary.js'
with open(vocab_file, 'r') as f:
    vocab_content = f.read()

pattern = r"word:\s*'([^']+)',\s*category:\s*'([^']+)',\s*label:\s*'([^']+)'"
matches = re.findall(pattern, vocab_content)

label_to_word = {}
for word, category, label in matches:

    lbl = label.strip()

    if lbl not in label_to_word:
        label_to_word[lbl] = word

    if lbl == 'أذن': 
        if 'وذن' not in label_to_word: label_to_word['وذن'] = word
    if lbl == 'وذن': 
         if 'أذن' not in label_to_word: label_to_word['أذن'] = word

if 'anzas' in matches[0] or True:
    label_to_word['أنزاس'] = 'anzas_simple'
    label_to_word['بردڤان'] = 'bordguela_simple'

    label_to_word['رة'] = 'bagra_simple'

print(f"Loaded {len(label_to_word)} vocabulary items.")

with open('simple_extracted_data.json', 'r') as f:
    data = json.load(f)

image_queue = []
text_list = []
last_text = None

for item in data:
    if item['type'] == 'image':
        image_queue.append(item['path'])
    elif item['type'] == 'text':
        val = item['value'].strip()
        if not val: continue

        if len(val) < 2 and val not in ['ب', 'ت']:
             continue 
             
        if val != last_text:
            text_list.append(val)
            last_text = val

print(f"Found {len(image_queue)} images and {len(text_list)} unique text blocks.")

mapping = {}
used_images = set()

img_idx = 0

for text in text_list:

    if text in label_to_word:
        word_id = label_to_word[text]
        
        if img_idx < len(image_queue):
            image_path = image_queue[img_idx]
            img_idx += 1

            mapping[word_id] = image_path
            print(f"Mapped {text} ({word_id}) -> {image_path}")
        else:
            print(f"WARNING: No image available for {text} ({word_id})")
    else:

        print(f"Skipping unknown text: {text}")

source_base = "temp_simple_doc/word/"
dest_dir = "public/assets/images/items/"
new_items_images = {}

print("\nCopying images...")
for word_id, rel_path in mapping.items():

    if rel_path.startswith('media/'):
        full_src = os.path.join(source_base, rel_path)
    else:
        full_src = os.path.join(source_base, 'media', rel_path)
    
    if not os.path.exists(full_src):

        fname = os.path.basename(rel_path)
        full_src = os.path.join(source_base, 'media', fname)
    
    if os.path.exists(full_src):
        ext = os.path.splitext(full_src)[1]
        new_filename = f"{word_id}{ext}"
        dest_path = os.path.join(dest_dir, new_filename)
        
        shutil.copy2(full_src, dest_path)
        new_items_images[word_id] = new_filename
    else:
        print(f"ERROR: Image file not found at {full_src}")

json_path = 'src/data/items_images.json'
with open(json_path, 'r') as f:
    existing_map = json.load(f)

existing_map.update(new_items_images)

with open(json_path, 'w') as f:
    json.dump(existing_map, f, indent=4)

print("Updated items_images.json successfully.")

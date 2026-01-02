
import json
import os
import shutil
import re

# 1. Load Vocabulary to build Label -> Word map
vocab_file = 'src/data/vocabulary.js'
with open(vocab_file, 'r') as f:
    vocab_content = f.read()

# Extract base items
# Assuming structure: { id: '...', word: '...', category: '...', label: '...' }
# We'll use a regex to be robust
pattern = r"word:\s*'([^']+)',\s*category:\s*'([^']+)',\s*label:\s*'([^']+)'"
matches = re.findall(pattern, vocab_content)

label_to_word = {}
for word, category, label in matches:
    # Normalize label (strip)
    lbl = label.strip()
    # PREVENT OVERWRITE: Keep the first found ID (Base items appear first in file, and now have _simple suffix)
    if lbl not in label_to_word:
        label_to_word[lbl] = word
        
    # Also handle some known variations if needed
    if lbl == 'أذن': 
        if 'وذن' not in label_to_word: label_to_word['وذن'] = word
    if lbl == 'وذن': 
         if 'أذن' not in label_to_word: label_to_word['أذن'] = word

# Manual Aliases for Simple Doc Variations with _simple suffix
if 'anzas' in matches[0] or True: # Force add
    label_to_word['أنزاس'] = 'anzas_simple'
    label_to_word['بردڤان'] = 'bordguela_simple'
    # Hack for broken 'bagra' (cow) text which appears as 'b', 'g', 'ra'
    # 'ra' (رة) is the only part > 1 char that survives the loop filter
    label_to_word['رة'] = 'bagra_simple'

print(f"Loaded {len(label_to_word)} vocabulary items.")

# 2. Process Extracted Data
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
        # Skip single chars that are likely noise unless they are known words
        if len(val) < 2 and val not in ['ب', 'ت']: # heuristic
             continue 
             
        if val != last_text:
            text_list.append(val)
            last_text = val

print(f"Found {len(image_queue)} images and {len(text_list)} unique text blocks.")

# 3. Map Layout (Queue Strategy)
# We assume Image(s) precede Text(s).
# Structure seems to be: [Img A, Img B, ...] then [Text A, Text B, ...]
# So we treat distinct texts as consumers of the image queue.

mapping = {} # word -> image_filename
used_images = set()

# Safe mapping loop
# We'll pop from the front of image_queue for each text
img_idx = 0

for text in text_list:
    # Check if text is in our vocab
    if text in label_to_word:
        word_id = label_to_word[text]
        
        if img_idx < len(image_queue):
            image_path = image_queue[img_idx]
            img_idx += 1
            
            # Record mapping
            mapping[word_id] = image_path
            print(f"Mapped {text} ({word_id}) -> {image_path}")
        else:
            print(f"WARNING: No image available for {text} ({word_id})")
    else:
        # Check fuzzy or "bagra" split case
        # If text is something we don't recognize, maybe we shouldn't consume an image?
        # But if the document flow implies 1-to-1, we might lose sync if we skip consuming an image for unknown text.
        # However, looking at the dump, most texts were valid.
        print(f"Skipping unknown text: {text}")

# 4. Copy and Rename Images
source_base = "temp_simple_doc/word/"
dest_dir = "public/assets/images/items/"
new_items_images = {}

print("\nCopying images...")
for word_id, rel_path in mapping.items():
    # rel_path is like "media/image1.jpeg"
    # Construct full source path
    # Check if it has 'media' prefix in rel_path
    if rel_path.startswith('media/'):
        full_src = os.path.join(source_base, rel_path)
    else:
        full_src = os.path.join(source_base, 'media', rel_path)
    
    if not os.path.exists(full_src):
        # Try finding it in media dir directly just in case
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

# 5. Update items_images.json
# We read the existing one to keep Rich images (and others not in this doc?)
json_path = 'src/data/items_images.json'
with open(json_path, 'r') as f:
    existing_map = json.load(f)

# Update with new simple images
# This OVERWRITES the Base vocabulary images with the ones from the DOCX
# Which is exactly what the user wants.
existing_map.update(new_items_images)

with open(json_path, 'w') as f:
    json.dump(existing_map, f, indent=4)

print("Updated items_images.json successfully.")

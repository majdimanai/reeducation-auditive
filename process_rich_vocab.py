
import json
import os
import shutil

with open('rich_extracted_data.json', 'r') as f:
    data = json.load(f)

img_output_dir = 'public/assets/images/items'
os.makedirs(img_output_dir, exist_ok=True)

vocab_map = {

    "\u0642\u0644\u0645": ("9lam", "ecole"),
    "\u0643\u0631\u0637\u0627\u0628\u0629": ("kartaba", "ecole"),
    "\u0637\u0628\u0627\u0634\u064a\u0631": ("tabachir", "ecole"),
    "\u0635\u0628\u0648\u0631\u0629": ("sabboura", "ecole"),
    "\u0637\u0627\u0648\u0644\u0629": ("tawla_rich", "ecole"),
    "\u0643\u0631\u0633\u064a": ("korsi_rich", "ecole"),

    "\u0631\u0627\u0633": ("ras", "corps"),
    "\u0633\u0627\u0642\u064a\u0646": ("saguine", "corps"),
    "\u0634\u0639\u0631": ("ch3ar_rich", "corps"),
    "\u0639\u064a\u0646\u064a\u0646": ("3inin", "corps"),
    "\u062e\u0634\u0645": ("khcham_rich", "corps"),

    "\u0633\u0631\u062f\u0648\u0643": ("sardouk", "animaux"),
    "\u0639\u0635\u0641\u0648\u0631": ("3asfour", "animaux"),
    "\u0639\u0644\u0648\u0634": ("3allouch", "animaux"),
    "\u0630\u0628\u0627\u0646\u0629": ("dhebena", "animaux"),
    "\u0632\u0631\u0627\u0641\u0629": ("zrafa", "animaux"),

    "\u0635\u0628\u0627\u0637": ("sabbat", "vetements"),
    "\u0643\u0644\u0633\u064a\u0637\u0629": ("kalchita", "vetements"),
    "\u0645\u0631\u064a\u0648\u0644": ("maryoul", "vetements"),
    "\u0634\u0627\u0628\u0648": ("chappeau", "vetements"),
    "\u0633\u0631\u0648\u0627\u0644": ("serwel", "vetements"),

    "\u0635\u0627\u0644\u0629": ("sala", "maison"),
    "\u0641\u0631\u0634": ("farch", "maison"),
    "\u0643\u0648\u0632\u064a\u0646\u0629": ("kouzina", "maison"),
    "\u062a\u0644\u0641\u0632\u0629": ("talvza", "maison"),
    "\u0641\u0631\u064a\u062c\u064a\u062f\u0627\u0631": ("frigidaire", "maison"),

    "\u0633\u0643\u0633\u064a": ("couscous", "alimentation"),
    "\u0645\u0642\u0631\u0648\u0646\u0629": ("ma9rouna", "alimentation"),
    "\u0644\u0628\u0644\u0627\u0628\u064a": ("lablabi", "alimentation"),
    "\u0643\u0633\u0643\u0631\u0648\u062a": ("casse_croute", "alimentation"),
}

new_rich_vocab = []
new_image_map = {}

current_category = None
found_labels = set()

for i, item in enumerate(data):
    if item['type'] == 'text':
        txt = item['value'].strip()
        if txt in vocab_map:
            word, category = vocab_map[txt]

            img_path = None
            if i+1 < len(data) and data[i+1]['type'] == 'image':
                img_path = data[i+1]['path']
            elif i+2 < len(data) and data[i+2]['type'] == 'image':
                img_path = data[i+2]['path']
            
            if img_path:

                img_basename = os.path.basename(img_path)
                src = os.path.join('temp_rich_doc', 'word', 'media', img_basename)
                
                ext = os.path.splitext(img_path)[1]
                if not ext: ext = '.jpg'

                dst_filename = f"{word}{ext}"
                dst_path = os.path.join(img_output_dir, dst_filename)

                shutil.copy(src, dst_path)
                print(f"Mapped {txt} -> {word} ({dst_filename})")
                
                new_image_map[word] = dst_filename

                new_rich_vocab.append({
                    "id": f"cat_r_{category}_{len(new_rich_vocab)}",
                    "word": word,
                    "category": category,
                    "label": txt
                })
                found_labels.add(txt)
            else:
                print(f"WARNING: No image found for {txt}")

with open('rich_vocab_update.json', 'w') as f:
    json.dump(new_rich_vocab, f, indent=4)

json_path = 'src/data/items_images.json'
try:
    with open(json_path, 'r') as f:
        full_map = json.load(f)
except:
    full_map = {}

full_map.update(new_image_map)

with open(json_path, 'w') as f:
    json.dump(full_map, f, indent=4)

print("Processing complete.")

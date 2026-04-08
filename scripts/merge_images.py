import json
import re

def parse_vocab(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
        json_str = content.replace("export const VOCABULARY = ", "").strip()
        if json_str.endswith(";"):
            json_str = json_str[:-1]
        try:
            return json.loads(json_str)
        except Exception as e:
            # Handle tricky js syntax if it's not strictly JSON, which old vocabulary.js might not be 
            # if keys are unquoted. But our new vocabulary.js is strictly JSON syntax.
            print("Failed to strictly parse, reading by string manipulation:", e)
            return None

import ast

def parse_old_vocab(js_path):
    import re
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all objects with label and word
    matches = re.finditer(r"word:\s*'([^']+)'[^}]*label:\s*'([^']+)'", content)
    res = {}
    for m in matches:
        res[m.group(2).strip()] = m.group(1).strip()
    return res

old_label_to_word = parse_old_vocab('projet_version2/src/data/vocabulary.js')

with open('projet_version2/src/data/items_images.json', 'r', encoding='utf-8') as f:
    old_images = json.load(f)

new_vocab = parse_vocab('src/data/vocabulary.js')
with open('src/data/items_images.json', 'r', encoding='utf-8') as f:
    new_images = json.load(f)

added = 0
for list_name, items in zip(["base", "docx_simple"], [new_vocab["categorization"]["base"], new_vocab["categorization"]["docx_simple"]]):
    for item in items:
        lbl = item["label"].strip()
        word = item["word"]
        if word not in new_images:
            if lbl in old_label_to_word:
                old_w = old_label_to_word[lbl]
                if old_w in old_images:
                    new_images[word] = old_images[old_w]
                    added += 1

with open('src/data/items_images.json', 'w', encoding='utf-8') as f:
    json.dump(new_images, f, indent=4, ensure_ascii=False)

print(f"Recovered {added} images for base vocabulary.")

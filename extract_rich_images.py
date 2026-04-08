
import zipfile
import os
import shutil
import xml.etree.ElementTree as ET
import re

docx_path = "Les images de la catégorisation avec les mots Vocabulaire RICHE.docx"
extract_dir = "temp_rich_doc"
output_dir = "public/assets/images/items"

if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)
os.makedirs(extract_dir)

print(f"Extracting {docx_path}...")
with zipfile.ZipFile(docx_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

rels_path = os.path.join(extract_dir, "word/_rels/document.xml.rels")
tree = ET.parse(rels_path)
root = tree.getroot()

ns = {
    'rels': 'http://schemas.openxmlformats.org/package/2006/relationships',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
}

rid_map = {}
for rel in root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
    rid = rel.get('Id')
    target = rel.get('Target')
    rid_map[rid] = target

doc_path = os.path.join(extract_dir, "word/document.xml")
tree = ET.parse(doc_path)
root = tree.getroot()

body = root.find('.//w:body', ns)

items = []

current_text = ""
current_image = None

elements_order = []

for elem in root.iter():
    tag = elem.tag

    if tag.endswith('}t'):
        if elem.text and elem.text.strip():
            elements_order.append({'type': 'text', 'value': elem.text.strip()})

    if tag.endswith('}blip'):
        embed = elem.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if embed and embed in rid_map:
            img_file = rid_map[embed]

            if img_file.startswith('media/'):
                img_file = img_file
            elif 'media/' in img_file: 
                img_file = 'media/' + os.path.basename(img_file)
            else:

                 img_file = 'media/' + os.path.basename(img_file)

            elements_order.append({'type': 'image', 'path': img_file})

print(f"Found {len(elements_order)} elements.")

for i in range(min(10, len(elements_order))):
    print(f"{i}: {elements_order[i]}")

import json
with open('rich_extracted_data.json', 'w') as f:
    json.dump(elements_order, f, indent=4)

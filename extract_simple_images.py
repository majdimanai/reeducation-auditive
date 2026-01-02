
import zipfile
import os
import shutil
import xml.etree.ElementTree as ET
import re

docx_path = "simple.docx"
extract_dir = "temp_simple_doc"

if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)
os.makedirs(extract_dir)

print(f"Extracting {docx_path}...")
with zipfile.ZipFile(docx_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Parse Relationships to map rId to filenames
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

# Parse Document to find images and text in order
doc_path = os.path.join(extract_dir, "word/document.xml")
tree = ET.parse(doc_path)
root = tree.getroot()

elements_order = []

for elem in root.iter():
    tag = elem.tag
    # Text
    if tag.endswith('}t'):
        if elem.text and elem.text.strip():
            elements_order.append({'type': 'text', 'value': elem.text.strip()})
    
    # Image (Blip)
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

import json
with open('simple_extracted_data.json', 'w') as f:
    json.dump(elements_order, f, indent=4)

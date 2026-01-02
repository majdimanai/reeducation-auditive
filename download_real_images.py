
import os
import subprocess
import time

# Map items to English search terms for finding images
# Vocabulary:
# Animaux
keyword_map = {
    'batta': 'duck',
    'bagra': 'cow',
    'djaja': 'chicken',
    'houta': 'fish',
    'arnoub': 'rabbit',
    # Fruits
    'bordguela': 'orange fruit',
    'bannane': 'banana',
    'anzas': 'pear fruit',
    'tout': 'blackberry fruit',
    # Legumes
    'sfenaria': 'carrot vegetable',
    'batata': 'potato vegetable',
    'bsol': 'onion vegetable',
    'tmatem': 'tomato vegetable',
    'felfel': 'green pepper vegetable',
    # Corps (Harder to get clean isolated images, but we'll try)
    'yed': 'hand body part',
    '3in': 'eye close up',
    'khcham': 'nose face',
    'fom': 'mouth smile',
    'seg': 'leg',
    'ch3ar': 'hair style',
    'wdhen': 'ear',
    '7wajeb': 'eyebrows',
    # Transport
    'kar': 'bus',
    'bisklet': 'bicycle',
    'metro': 'tramway train',
    'tayara': 'airplane',
    # Maison
    'srir': 'bed furniture',
    'korsi': 'chair furniture',
    'tawla': 'table furniture',
    'ghassala': 'washing machine',
    'beb': 'wooden door',
    # Couleurs (Will get objects of that color)
    'a7mar': 'red color texture',
    'azra9': 'blue color texture',
    'asfar': 'yellow color texture',
    'akhdhar': 'green color texture',
    # Alimentation
    '7lib': 'milk glass',
    '3dham': 'egg food',
    'zebda': 'butter food',
    'yaghorta': 'yogurt pot',
    'khobz': 'bread loaf'
}

output_dir = 'public/assets/images/items'

# Using loremflickr as a source of real images
base_url = "https://loremflickr.com/320/240"

# Using Unsplash source for high quality images
# source.unsplash.com is deprecated but often still works or redirects. 
# Better alternative for scripts: direct accessible high-quality placeholder services
# Let's try "https://image.pollinations.ai/prompt/{prompt}" which generates AI images on fly? 
# Or stay with a better keyword search on a stable placeholder.
# Let's stick to a robust scraping or a better service.
# specialized for simple objects: https://loremflickr.com is good but needs "fresh" random
# Let's try adding a random buster to loremflickr first with specific keywords.

import random

# Files we ALREADY have realistic versions for (SKIP THESE)
skip_list = [] # REDOWNLOAD ALL to ensure consistency if requested

for word, keyword in keyword_map.items():
    if word in skip_list:
        print(f"Skipping {word}")
        continue
    
    filename = f"{word}.jpg"
    # Add random to prevent caching same image
    random_id = random.randint(1, 10000)
    url = f"{base_url}/{keyword.replace(' ', ',')}/all?lock={random_id}"
    
    print(f"Downloading {word} ({keyword})...")
    
    # Use wget with --max-redirect
    cmd = ["wget", "-O", f"{output_dir}/{filename}", url]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Downloaded {filename}")
        time.sleep(1) 
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {word}")

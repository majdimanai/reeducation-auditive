
import os
import subprocess
import time

keyword_map = {
    'batta': 'duck',
    'bagra': 'cow',
    'djaja': 'chicken',
    'houta': 'fish',
    'arnoub': 'rabbit',

    'bordguela': 'orange fruit',
    'bannane': 'banana',
    'anzas': 'pear fruit',
    'tout': 'blackberry fruit',

    'sfenaria': 'carrot vegetable',
    'batata': 'potato vegetable',
    'bsol': 'onion vegetable',
    'tmatem': 'tomato vegetable',
    'felfel': 'green pepper vegetable',

    'yed': 'hand body part',
    '3in': 'eye close up',
    'khcham': 'nose face',
    'fom': 'mouth smile',
    'seg': 'leg',
    'ch3ar': 'hair style',
    'wdhen': 'ear',
    '7wajeb': 'eyebrows',

    'kar': 'bus',
    'bisklet': 'bicycle',
    'metro': 'tramway train',
    'tayara': 'airplane',

    'srir': 'bed furniture',
    'korsi': 'chair furniture',
    'tawla': 'table furniture',
    'ghassala': 'washing machine',
    'beb': 'wooden door',

    'a7mar': 'red color texture',
    'azra9': 'blue color texture',
    'asfar': 'yellow color texture',
    'akhdhar': 'green color texture',

    '7lib': 'milk glass',
    '3dham': 'egg food',
    'zebda': 'butter food',
    'yaghorta': 'yogurt pot',
    'khobz': 'bread loaf'
}

output_dir = 'public/assets/images/items'

base_url = "https://loremflickr.com/320/240"

import random

skip_list = []

for word, keyword in keyword_map.items():
    if word in skip_list:
        print(f"Skipping {word}")
        continue
    
    filename = f"{word}.jpg"

    random_id = random.randint(1, 10000)
    url = f"{base_url}/{keyword.replace(' ', ',')}/all?lock={random_id}"
    
    print(f"Downloading {word} ({keyword})...")

    cmd = ["wget", "-O", f"{output_dir}/{filename}", url]
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Downloaded {filename}")
        time.sleep(1) 
    except subprocess.CalledProcessError:
        print(f"❌ Failed to download {word}")

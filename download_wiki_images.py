import requests
import os
import shutil
import time

# Map vocabulary ID/Word to Wikipedia Search Term
wiki_map = {
    # ANIMAUX
    'kelb': 'Dog',
    'gatoussa': 'Cat',
    'batta': 'Duck',
    'bagra': 'Cattle', # 'Cattle' gives better results than 'Cow' often
    'djaja': 'Chicken',
    'houta': 'Fish',
    'arnoub': 'Rabbit',

    # FRUITS
    'toffeh': 'Apple',
    'bordguela': 'Orange (fruit)',
    'della': 'Watermelon',
    'bannane': 'Banana',
    'anzas': 'Pear',
    'tout': 'Blackberry', 

    # LEGUMES (Vegetables)
    'sfenaria': 'Carrot',
    'batata': 'Potato',
    'bsol': 'Onion',
    'tmatem': 'Tomato',
    'felfel': 'Bell pepper', 

    # CORPS (Body)
    'yed': 'Hand',
    '3in': 'Human eye',
    'khcham': 'Human nose',
    'fom': 'Mouth',
    'seg': 'Leg',
    'ch3ar': 'Hair',
    'wdhen': 'Ear',
    '7wajeb': 'Eyebrow',

    # TRANSPORT
    'karhba': 'Car',
    'kar': 'Bus',
    'bisklet': 'Bicycle',
    'metro': 'Tram',
    'tayara': 'Airplane',

    # MAISON (Home)
    'srir': 'Bed',
    'korsi': 'Chair',
    'tawla': 'Table (furniture)',
    'ghassala': 'Washing machine',
    'beb': 'Door',

    # COULEURS (Colors) 
    'a7mar': 'Red', 
    'azra9': 'Blue',
    'asfar': 'Yellow',
    'akhdhar': 'Green',

    # ALIMENTATION (Food)
    '7lib': 'Milk',
    '3dham': 'Egg as food',
    'zebda': 'Butter',
    'yaghorta': 'Yogurt',
    'khobz': 'Bread'
}

output_dir = 'public/assets/images/items'
os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def download_wiki_image(word, term):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": term,
        "pithumbsize": 600
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        image_url = None
        for page_id, page in pages.items():
            if "thumbnail" in page:
                image_url = page["thumbnail"]["source"]
                break
        
        if image_url:
            # Get extension
            ext = image_url.split('.')[-1]
            if len(ext) > 4: ext = 'jpg' # Sanity check
            
            filename = f"{word}.{ext}"
            filepath = os.path.join(output_dir, filename)
            
            if os.path.exists(filepath):
                print(f"Skipping {word} (already exists)")
                return filename

            print(f"Downloading {word} ({term}) -> {image_url}")
            
            # Download file
            img_resp = requests.get(image_url, headers=headers, stream=True)
            if img_resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    img_resp.raw.decode_content = True
                    shutil.copyfileobj(img_resp.raw, f)
                print(f"✅ Saved to {filename}")
                return filename
            else:
                print(f"❌ Failed to download content for {word}: Status {img_resp.status_code}")
        else:
            print(f"⚠️ No image found for {term}")
            
    except Exception as e:
        print(f"❌ Error for {word}: {e}")
    
    return None

# MAIN LOOP
results = {}

for word, term in wiki_map.items():
    filename = download_wiki_image(word, term)
    if filename:
        results[word] = filename
    time.sleep(2) # Increased delay to avoid 429

# Update JSON Map
import json
json_path = 'src/data/items_images.json'

try:
    with open(json_path, 'r') as f:
        full_map = json.load(f)
except:
    full_map = {}

full_map.update(results)

with open(json_path, 'w') as f:
    json.dump(full_map, f, indent=4)

print("Updated items_images.json")

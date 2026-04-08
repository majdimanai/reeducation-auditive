import zipfile
import os
import re

mapping = {
    'مدرسة.odt': ('ecole', '.jpg'),     # Already updated Activity2 to ecole.jpg
    'جسم.odt': ('corps', '.jpeg'),      # animals mapped to corps.jpeg in old code, let's keep it naming the same or rewrite?
    'حيوانات.odt': ('animaux', '.jpeg'),# wait, the old mapping was flipped?
    'ماكولات.odt': ('alimentation', '.jpeg'),
    'ملابس.odt': ('vetements', '.jpeg'),
    'منزل.odt': ('maison', '.jpeg')
}

target_dir = 'public/assets/images/categories'
os.makedirs(target_dir, exist_ok=True)

for file, (cat, ext_expected) in mapping.items():
    if not os.path.exists(file):
        print(f"File {file} not found")
        continue

    with zipfile.ZipFile(file) as z:
        imgs = [f for f in z.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if imgs:
            target_path = os.path.join(target_dir, f"{cat}{ext_expected}")
            img_data = z.read(imgs[0])
            with open(target_path, 'wb') as t:
                t.write(img_data)
            print(f"Saved {cat}{ext_expected}")
        else:
            print(f"No images in {file}")

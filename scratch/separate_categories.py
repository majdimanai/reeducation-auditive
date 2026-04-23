
import os
import shutil

BASE_CAT_SRC = "/home/majdi/projet/newnewvocabulaire/vocabulaire de base/enregistrement  catégorisation vocbulaire simple/category/"
RICH_CAT_SRC = "/home/majdi/projet/newnewvocabulaire/vocabulaire riche/enregistrement  catégorisation vocbulaire complexe/category/"

BASE_CAT_DEST = "/home/majdi/projet/public/assets/images/categories/base/"
RICH_CAT_DEST = "/home/majdi/projet/public/assets/images/categories/rich/"

os.makedirs(BASE_CAT_DEST, exist_ok=True)
os.makedirs(RICH_CAT_DEST, exist_ok=True)

base_map = {
    'أثاث المنزل.jpg': 'maison.jpg',
    'أعضاء الجسم.png': 'corps.png',
    'الألوان.jpg': 'couleurs.jpg',
    'الحيوانات.jpg': 'animaux.jpg',
    'الخضر.jpg': 'legumes.jpg',
    'الغلال.png': 'fruits.png',
    'فطور الصباح.jpg': 'alimentation.jpg'
}

rich_map = {
    'منزل.jpg': 'maison.jpg',
    'طعام.jpg': 'alimentation.jpg',
    'الحيوانات.jpg': 'animaux.jpg',
    'الأشياء في المدرسة.jpg': 'ecole.jpg',
    'ملابس.jpg': 'vetements.jpg',
    'وسائل النقل.jpg': 'transport.jpg'
}

for src_name, dest_name in base_map.items():
    src = os.path.join(BASE_CAT_SRC, src_name)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(BASE_CAT_DEST, dest_name))
        print(f"Copied {src_name} to base/{dest_name}")

for src_name, dest_name in rich_map.items():
    src = os.path.join(RICH_CAT_SRC, src_name)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(RICH_CAT_DEST, dest_name))
        print(f"Copied {src_name} to rich/{dest_name}")

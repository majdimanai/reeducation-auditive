import os

# Vocabulary Data (Same as audio script)
VOCAB_LIST = [
    # Categorization Rich (New)
    {'id': 'cat_r_food_1', 'text': 'كسكروت', 'word': 'casse_croute'},
    {'id': 'cat_r_food_2', 'text': 'كسكسي', 'word': 'couscous'},
    {'id': 'cat_r_food_3', 'text': 'مقرونة', 'word': 'ma9rouna'},
    {'id': 'cat_r_food_4', 'text': 'لبلابي', 'word': 'lablabi'},
    {'id': 'cat_r_hom_1', 'text': 'ثلاجة', 'word': 'frigidaire'},
    {'id': 'cat_r_hom_2', 'text': 'تلفزة', 'word': 'talvza'},
    {'id': 'cat_r_hom_3', 'text': 'كوزينة', 'word': 'kouzina'},
    {'id': 'cat_r_hom_4', 'text': 'فرش', 'word': 'farch'},
    {'id': 'cat_r_hom_5', 'text': 'صالون', 'word': 'sala'},
    {'id': 'cat_r_clo_1', 'text': 'سروال', 'word': 'serwel'},
    {'id': 'cat_r_clo_2', 'text': 'قبعة', 'word': 'chappeau'},
    {'id': 'cat_r_clo_3', 'text': 'مريول', 'word': 'maryoul'},
    {'id': 'cat_r_clo_4', 'text': 'جوارب', 'word': 'kalchita'},
    {'id': 'cat_r_clo_5', 'text': 'حذاء', 'word': 'sabbat'},
    {'id': 'cat_r_anim_1', 'text': 'غزالة', 'word': 'ghazela'},
    {'id': 'cat_r_anim_2', 'text': 'عصفور', 'word': '3asfour'},
    {'id': 'cat_r_anim_3', 'text': 'ذبانة', 'word': 'dhebena'},
    {'id': 'cat_r_anim_4', 'text': 'علوش', 'word': '3alouch'},
    {'id': 'cat_r_anim_5', 'text': 'سردوك', 'word': 'sardouk'},
    {'id': 'cat_r_sch_1', 'text': 'سبورة', 'word': 'sabboura'},
    {'id': 'cat_r_sch_2', 'text': 'طباشير', 'word': 'tabachir'},
    {'id': 'cat_r_sch_3', 'text': 'محفظة', 'word': 'kartaba'},
    {'id': 'cat_r_sch_4', 'text': 'قلم', 'word': '9lam'},

    # Categorization Base (Existing)
    {'id': 'cat_b_anim_1', 'text': 'كلب', 'word': 'kelb'},
    {'id': 'cat_b_anim_2', 'text': 'قطوسة', 'word': 'gatoussa'},
    {'id': 'cat_b_anim_6', 'text': 'حوتة', 'word': 'houta'},
    {'id': 'cat_b_anim_7', 'text': 'أرنب', 'word': 'arnoub'},
    {'id': 'cat_b_fruit_2', 'text': 'برتقال', 'word': 'bordguela'},
    {'id': 'cat_b_fruit_4', 'text': 'بنان', 'word': 'bannane'},
    {'id': 'cat_b_fruit_5', 'text': 'إجاص', 'word': 'anzas'},
    {'id': 'cat_b_fruit_6', 'text': 'توت', 'word': 'tout'},
    {'id': 'cat_b_leg_1', 'text': 'سفنارية', 'word': 'sfenaria'},
    {'id': 'cat_b_leg_2', 'text': 'بطاطا', 'word': 'batata'},
    {'id': 'cat_b_leg_3', 'text': 'بصل', 'word': 'bsol'},
    {'id': 'cat_b_leg_4', 'text': 'طماطم', 'word': 'tmatem'},
    {'id': 'cat_b_leg_5', 'text': 'فلفل', 'word': 'felfel'},
    {'id': 'cat_b_body_1', 'text': 'يد', 'word': 'yed'},
    {'id': 'cat_b_body_2', 'text': 'عين', 'word': '3in'},
    {'id': 'cat_b_body_3', 'text': 'خشم', 'word': 'khcham'},
    {'id': 'cat_b_body_4', 'text': 'فم', 'word': 'fom'},
    {'id': 'cat_b_body_5', 'text': 'ساق', 'word': 'seg'},
    {'id': 'cat_b_body_6', 'text': 'شعر', 'word': 'ch3ar'},
    {'id': 'cat_b_body_7', 'text': 'أذن', 'word': 'wdhen'},
    {'id': 'cat_b_body_8', 'text': 'حواجب', 'word': '7wajeb'},
    {'id': 'cat_b_trans_1', 'text': 'كرهبة', 'word': 'karhba'},
    {'id': 'cat_b_trans_2', 'text': 'كار', 'word': 'kar'},
    {'id': 'cat_b_trans_3', 'text': 'بسكلات', 'word': 'bisklet'},
    {'id': 'cat_b_trans_4', 'text': 'ميترو', 'word': 'metro'},
    {'id': 'cat_b_trans_5', 'text': 'طيارة', 'word': 'tayara'},
    {'id': 'cat_b_home_1', 'text': 'سرير', 'word': 'srir'},
    {'id': 'cat_b_home_2', 'text': 'كرسي', 'word': 'korsi'},
    {'id': 'cat_b_home_3', 'text': 'طاولة', 'word': 'tawla'},
    {'id': 'cat_b_home_4', 'text': 'غسالة', 'word': 'ghassala'},
    {'id': 'cat_b_home_5', 'text': 'باب', 'word': 'beb'},
    {'id': 'cat_b_col_1', 'text': 'أحمر', 'word': 'a7mar'},
    {'id': 'cat_b_col_2', 'text': 'أزرق', 'word': 'azra9'},
    {'id': 'cat_b_col_3', 'text': 'أصفر', 'word': 'asfar'},
    {'id': 'cat_b_col_4', 'text': 'أخضر', 'word': 'akhdhar'},
    {'id': 'cat_b_food_1', 'text': 'حليب', 'word': '7lib'},
    {'id': 'cat_b_food_2', 'text': 'عظم', 'word': '3dham'},
    {'id': 'cat_b_food_3', 'text': 'زبدة', 'word': 'zebda'},
    {'id': 'cat_b_food_4', 'text': 'ياغرطة', 'word': 'yaghorta'},
    {'id': 'cat_b_food_5', 'text': 'خبز', 'word': 'khobz'},
]

OUTPUT_DIR = 'src/assets/images'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_svg(text, word, filename):
    # Create a nice colorful placeholder
    svg_content = f"""
    <svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#fef9c3" />
      <rect x="20" y="20" width="360" height="360" rx="20" ry="20" fill="#ffffff" stroke="#fcd34d" stroke-width="10" />
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="60" fill="#1e3a8a">{text}</text>
      <text x="50%" y="70%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="30" fill="#b91c1c" dy="20">{word}</text>
    </svg>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)

for item in VOCAB_LIST:
    path = os.path.join(OUTPUT_DIR, f"{item['word']}.svg") 
    create_svg(item['text'], item['word'], path)
    
print("Placeholder images generated.")

import os
import time
import urllib.request
import urllib.parse
import json

# Full Vocabulary Data from vocabulary.js
VOCAB_LIST = [
    # --- Activity 2: Categorization (Base) ---
    {'id': 'cat_b_anim_1', 'text': 'كلب'}, {'id': 'cat_b_anim_2', 'text': 'قطوسة'},
    {'id': 'cat_b_anim_3', 'text': 'بطة'}, {'id': 'cat_b_anim_4', 'text': 'بقرة'},
    {'id': 'cat_b_anim_5', 'text': 'دجاجة'}, {'id': 'cat_b_anim_6', 'text': 'حوتة'},
    {'id': 'cat_b_anim_7', 'text': 'أرنب'},

    {'id': 'cat_b_fruit_1', 'text': 'تفاح'}, {'id': 'cat_b_fruit_2', 'text': 'برتقال'},
    {'id': 'cat_b_fruit_3', 'text': 'دلاع'}, {'id': 'cat_b_fruit_4', 'text': 'بنان'},
    {'id': 'cat_b_fruit_5', 'text': 'إجاص'}, {'id': 'cat_b_fruit_6', 'text': 'توت'},

    {'id': 'cat_b_leg_1', 'text': 'سفنارية'}, {'id': 'cat_b_leg_2', 'text': 'بطاطا'},
    {'id': 'cat_b_leg_3', 'text': 'بصل'}, {'id': 'cat_b_leg_4', 'text': 'طماطم'},
    {'id': 'cat_b_leg_5', 'text': 'فلفل'},

    {'id': 'cat_b_body_1', 'text': 'يد'}, {'id': 'cat_b_body_2', 'text': 'عين'},
    {'id': 'cat_b_body_3', 'text': 'خشم'}, {'id': 'cat_b_body_4', 'text': 'فم'},
    {'id': 'cat_b_body_5', 'text': 'ساق'}, {'id': 'cat_b_body_6', 'text': 'شعر'},
    {'id': 'cat_b_body_7', 'text': 'أذن'}, {'id': 'cat_b_body_8', 'text': 'حواجب'},

    {'id': 'cat_b_trans_1', 'text': 'كرهبة'}, {'id': 'cat_b_trans_2', 'text': 'كار'},
    {'id': 'cat_b_trans_3', 'text': 'بسكلات'}, {'id': 'cat_b_trans_4', 'text': 'ميترو'},
    {'id': 'cat_b_trans_5', 'text': 'طيارة'},

    {'id': 'cat_b_home_1', 'text': 'سرير'}, {'id': 'cat_b_home_2', 'text': 'كرسي'},
    {'id': 'cat_b_home_3', 'text': 'طاولة'}, {'id': 'cat_b_home_4', 'text': 'غسالة'},
    {'id': 'cat_b_home_5', 'text': 'باب'},

    {'id': 'cat_b_col_1', 'text': 'أحمر'}, {'id': 'cat_b_col_2', 'text': 'أزرق'},
    {'id': 'cat_b_col_3', 'text': 'أصفر'}, {'id': 'cat_b_col_4', 'text': 'أخضر'},

    {'id': 'cat_b_food_1', 'text': 'حليب'}, {'id': 'cat_b_food_2', 'text': 'عظم'},
    {'id': 'cat_b_food_3', 'text': 'زبدة'}, {'id': 'cat_b_food_4', 'text': 'ياغرطة'},
    {'id': 'cat_b_food_5', 'text': 'خبز'},

    # --- Activity 2: Categorization (Rich) ---
    {'id': 'cat_r_food_1', 'text': 'كسكروت'}, {'id': 'cat_r_food_2', 'text': 'كسكسي'},
    {'id': 'cat_r_food_3', 'text': 'مقرونة'}, {'id': 'cat_r_food_4', 'text': 'لبلابي'},

    {'id': 'cat_r_hom_1', 'text': 'ثلاجة'}, {'id': 'cat_r_hom_2', 'text': 'تلفزة'},
    {'id': 'cat_r_hom_3', 'text': 'كوزينة'}, {'id': 'cat_r_hom_4', 'text': 'فرش'},
    {'id': 'cat_r_hom_5', 'text': 'صالون'},

    {'id': 'cat_r_clo_1', 'text': 'سروال'}, {'id': 'cat_r_clo_2', 'text': 'قبعة'},
    {'id': 'cat_r_clo_3', 'text': 'مريول'}, {'id': 'cat_r_clo_4', 'text': 'جوارب'},
    {'id': 'cat_r_clo_5', 'text': 'حذاء'},

    {'id': 'cat_r_anim_1', 'text': 'غزالة'}, {'id': 'cat_r_anim_2', 'text': 'عصفور'},
    {'id': 'cat_r_anim_3', 'text': 'ذبانة'}, {'id': 'cat_r_anim_4', 'text': 'علوش'},
    {'id': 'cat_r_anim_5', 'text': 'سردوك'},

    {'id': 'cat_r_sch_1', 'text': 'سبورة'}, {'id': 'cat_r_sch_2', 'text': 'طباشير'},
    {'id': 'cat_r_sch_3', 'text': 'محفظة'}, {'id': 'cat_r_sch_4', 'text': 'قلم'},


    # --- Activity 1: Discrimination Base ---
    {'id': 'd_b_1', 'text': 'باب'}, {'id': 'd_b_2', 'text': 'بابا'}, {'id': 'd_b_3', 'text': 'بطة'},
    {'id': 'd_b_4', 'text': 'بيت'}, {'id': 'd_b_5', 'text': 'بعيد'}, {'id': 'd_b_6', 'text': 'بومة'},
    {'id': 'd_b_7', 'text': 'بقرة'}, {'id': 'd_b_8', 'text': 'بطاطا'}, {'id': 'd_b_9', 'text': 'بنية'},
    {'id': 'd_b_10', 'text': 'بصل'},

    {'id': 'd_m_1', 'text': 'ماما'}, {'id': 'd_m_2', 'text': 'ماء'}, {'id': 'd_m_3', 'text': 'موز'},
    {'id': 'd_m_4', 'text': 'ملح'}, {'id': 'd_m_5', 'text': 'مكتب'}, {'id': 'd_m_6', 'text': 'مدرسة'},
    {'id': 'd_m_7', 'text': 'مغرفة'}, {'id': 'd_m_8', 'text': 'مفتاح'}, {'id': 'd_m_9', 'text': 'مخدة'},
    {'id': 'd_m_10', 'text': 'معجون'},

    {'id': 'd_t_1', 'text': 'تفاح'}, {'id': 'd_t_2', 'text': 'تاكل'}, {'id': 'd_t_3', 'text': 'تلفزة'},
    {'id': 'd_t_4', 'text': 'توت'}, {'id': 'd_t_5', 'text': 'تبكي'}, {'id': 'd_t_6', 'text': 'تلعب'},
    {'id': 'd_t_7', 'text': 'تراب'}, {'id': 'd_t_8', 'text': 'تمشي'}, {'id': 'd_t_9', 'text': 'تاتا'},
    {'id': 'd_t_10', 'text': 'تضحك'},

    {'id': 'd_d_1', 'text': 'دار'}, {'id': 'd_d_2', 'text': 'دجاجة'}, {'id': 'd_d_3', 'text': 'دلاع'},
    {'id': 'd_d_4', 'text': 'دواء'}, {'id': 'd_d_5', 'text': 'دورة'}, {'id': 'd_d_6', 'text': 'دب'},
    {'id': 'd_d_7', 'text': 'دبوزة'}, {'id': 'd_d_8', 'text': 'درجيحة'}, {'id': 'd_d_9', 'text': 'دودة'},
    {'id': 'd_d_10', 'text': 'دروج'},

    # --- Activity 1: Discrimination Rich ---
    # CH
    {'id': 'd_ch_1', 'text': 'شكلاطة'}, {'id': 'd_ch_2', 'text': 'فراشة'}, {'id': 'd_ch_3', 'text': 'فراشية'},
    {'id': 'd_ch_4', 'text': 'فرش'}, {'id': 'd_ch_5', 'text': 'شابو'}, {'id': 'd_ch_6', 'text': 'علوش'},
    {'id': 'd_ch_7', 'text': 'شجرة'}, {'id': 'd_ch_8', 'text': 'شباك'}, {'id': 'd_ch_9', 'text': 'مشاية'},
    {'id': 'd_ch_10', 'text': 'شمس'},
    # J
    {'id': 'd_j_1', 'text': 'جراية'}, {'id': 'd_j_2', 'text': 'عجلة'}, {'id': 'd_j_3', 'text': 'فريجيدار'},
    {'id': 'd_j_4', 'text': 'جنينة'}, {'id': 'd_j_5', 'text': 'جمل'}, {'id': 'd_j_6', 'text': 'سجادة'},
    {'id': 'd_j_7', 'text': 'حجرة'}, {'id': 'd_j_8', 'text': 'جرادة'}, {'id': 'd_j_9', 'text': 'جريدة'},
    {'id': 'd_j_10', 'text': 'فنجان'},
    # K
    {'id': 'd_k_1', 'text': 'شكلاطة'}, {'id': 'd_k_2', 'text': 'فاكية'}, {'id': 'd_k_3', 'text': 'كرافات'},
    {'id': 'd_k_4', 'text': 'كسكروت'}, {'id': 'd_k_5', 'text': 'كلسيطة'}, {'id': 'd_k_6', 'text': 'كاسكات'},
    {'id': 'd_k_7', 'text': 'سردوك'}, {'id': 'd_k_8', 'text': 'مركز'}, {'id': 'd_k_9', 'text': 'كرسي'},
    {'id': 'd_k_10', 'text': 'كورة'},
    # G
    {'id': 'd_g_1', 'text': 'قطوسة'}, {'id': 'd_g_2', 'text': 'قمرة'}, {'id': 'd_g_3', 'text': 'قازوز'},
    {'id': 'd_g_4', 'text': 'قيتون'}, {'id': 'd_g_5', 'text': 'قمح'}, {'id': 'd_g_6', 'text': 'قنارية'},
    {'id': 'd_g_7', 'text': 'قيدون'}, {'id': 'd_g_8', 'text': 'غاز'}, {'id': 'd_g_9', 'text': 'قلاص'},
    {'id': 'd_g_10', 'text': 'قوم'},
    # F
    {'id': 'd_f_1', 'text': 'فنجان'}, {'id': 'd_f_2', 'text': 'فراشة'}, {'id': 'd_f_3', 'text': 'فراشية'},
    {'id': 'd_f_4', 'text': 'فاكية'}, {'id': 'd_f_5', 'text': 'فلفل'}, {'id': 'd_f_6', 'text': 'فريجيدار'},
    {'id': 'd_f_7', 'text': 'فرش'}, {'id': 'd_f_8', 'text': 'فيل'}, {'id': 'd_f_9', 'text': 'فرحان'},
    {'id': 'd_f_10', 'text': 'فطيرة'},
    # V
    {'id': 'd_v_1', 'text': 'فاليز'}, {'id': 'd_v_2', 'text': 'فاست'}, {'id': 'd_v_3', 'text': 'فازة'},
    {'id': 'd_v_4', 'text': 'فيترينة'}, {'id': 'd_v_5', 'text': 'فولون'}, {'id': 'd_v_6', 'text': 'فيراج'},
    {'id': 'd_v_7', 'text': 'فيديو'}, {'id': 'd_v_8', 'text': 'فكسان'}, {'id': 'd_v_9', 'text': 'فانيليا'},
    {'id': 'd_v_10', 'text': 'فواياج'},
    # KH
    {'id': 'd_kh_1', 'text': 'خزانة'}, {'id': 'd_kh_2', 'text': 'خياطة'}, {'id': 'd_kh_3', 'text': 'ملوخية'},
    {'id': 'd_kh_4', 'text': 'خبزة'}, {'id': 'd_kh_5', 'text': 'خضرة'}, {'id': 'd_kh_6', 'text': 'خاتم'},
    {'id': 'd_kh_7', 'text': 'خبز'}, {'id': 'd_kh_8', 'text': 'خيط'}, {'id': 'd_kh_9', 'text': 'خوخة'},
    {'id': 'd_kh_10', 'text': 'خدمة'},
    # H
    {'id': 'd_h_1', 'text': 'حمامة'}, {'id': 'd_h_2', 'text': 'هلال'}, {'id': 'd_h_3', 'text': 'هدية'},
    {'id': 'd_h_4', 'text': 'حوش'}, {'id': 'd_h_5', 'text': 'هواء'}, {'id': 'd_h_6', 'text': 'حراف'},
    {'id': 'd_h_7', 'text': 'هرم'}, {'id': 'd_h_8', 'text': 'هدهد'}, {'id': 'd_h_9', 'text': 'هيبو'},
    {'id': 'd_h_10', 'text': 'هرب'},
]

# CHANGE OUTPUT DIRECTORY TO PUBLIC FOLDER
# Correct path relative to where script is run (project root)
OUTPUT_DIR = 'public/audio/words'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def download_tts(text, filename):
    # Using Google Translate TTS API (Unofficial but widely used)
    # Allows grabbing MP3 for text
    try:
        q = urllib.parse.quote(text)
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl=ar&client=tw-ob"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded: {text} -> {filename}")
        time.sleep(1) # Be nice to API
    except Exception as e:
        print(f"Failed {text}: {e}")

print(f"Checking {len(VOCAB_LIST)} words in {OUTPUT_DIR}...")

for item in VOCAB_LIST:
    path = os.path.join(OUTPUT_DIR, f"{item['id']}.mp3")
    if not os.path.exists(path):
        print(f"Generating missing: {item['id']}")
        download_tts(item['text'], path)
    else:
        # print(f"Exists: {path}") # Reduce noise
        pass

print("Done processing audio.")

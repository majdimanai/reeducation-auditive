import os
import asyncio
import edge_tts

# Vocabulary Data
VOCAB_LIST = [
    # Discrimination Base
    {'id': 'd_b_1', 'text': 'باب'},
    {'id': 'd_b_2', 'text': 'بابا'},
    {'id': 'd_b_3', 'text': 'بطة'},
    {'id': 'd_b_4', 'text': 'بيت'},
    {'id': 'd_b_5', 'text': 'بعيد'},
    {'id': 'd_b_6', 'text': 'بومة'},
    {'id': 'd_b_7', 'text': 'بقرة'},
    {'id': 'd_b_8', 'text': 'بطاطا'},
    {'id': 'd_b_9', 'text': 'بنية'},
    {'id': 'd_b_10', 'text': 'بصل'},
    {'id': 'd_m_1', 'text': 'ماما'},
    {'id': 'd_m_2', 'text': 'ماء'},
    {'id': 'd_m_3', 'text': 'موز'},
    {'id': 'd_m_4', 'text': 'ملح'},
    {'id': 'd_m_5', 'text': 'مكتب'},
    {'id': 'd_m_6', 'text': 'مدرسة'},
    {'id': 'd_m_7', 'text': 'مغرفة'},
    {'id': 'd_m_8', 'text': 'مفتاح'},
    {'id': 'd_m_9', 'text': 'مخدة'},
    {'id': 'd_m_10', 'text': 'معجون'},
    # Discrimination T-D
    {'id': 'd_t_1', 'text': 'تفاح'},
    {'id': 'd_t_2', 'text': 'تاكل'},
    {'id': 'd_t_3', 'text': 'تلفزة'},
    {'id': 'd_t_4', 'text': 'توت'},
    {'id': 'd_t_5', 'text': 'تبكي'},
    {'id': 'd_t_6', 'text': 'تلعب'},
    {'id': 'd_t_7', 'text': 'تراب'},
    {'id': 'd_t_8', 'text': 'تمشي'},
    {'id': 'd_t_9', 'text': 'تاتا'},
    {'id': 'd_t_10', 'text': 'تضحك'},
    {'id': 'd_d_1', 'text': 'دار'},
    {'id': 'd_d_2', 'text': 'دجاجة'},
    {'id': 'd_d_3', 'text': 'دلاع'},
    {'id': 'd_d_4', 'text': 'دواء'},
    {'id': 'd_d_5', 'text': 'دورة'},
    {'id': 'd_d_6', 'text': 'دب'},
    {'id': 'd_d_7', 'text': 'دبوزة'},
    {'id': 'd_d_8', 'text': 'درجيحة'},
    {'id': 'd_d_9', 'text': 'دودة'},
    {'id': 'd_d_10', 'text': 'دروج'},
    # Categorization Base
    {'id': 'cat_b_anim_1', 'text': 'كلب'},
    {'id': 'cat_b_anim_2', 'text': 'قطوسة'},
    {'id': 'cat_b_anim_6', 'text': 'حوتة'},
    {'id': 'cat_b_anim_7', 'text': 'أرنب'},
    {'id': 'cat_b_fruit_2', 'text': 'برتقال'},
    {'id': 'cat_b_fruit_4', 'text': 'بنان'},
    {'id': 'cat_b_fruit_5', 'text': 'إجاص'},
    {'id': 'cat_b_leg_1', 'text': 'سفنارية'},
    {'id': 'cat_b_leg_4', 'text': 'طماطم'},
    {'id': 'cat_b_leg_5', 'text': 'فلفل'},
    {'id': 'cat_b_body_1', 'text': 'يد'},
    {'id': 'cat_b_body_2', 'text': 'عين'},
    {'id': 'cat_b_body_3', 'text': 'خشم'},
    {'id': 'cat_b_body_4', 'text': 'فم'},
    {'id': 'cat_b_body_5', 'text': 'ساق'},
    {'id': 'cat_b_body_6', 'text': 'شعر'},
    {'id': 'cat_b_body_7', 'text': 'أذن'},
    {'id': 'cat_b_body_8', 'text': 'حواجب'},
    {'id': 'cat_b_trans_1', 'text': 'كرهبة'},
    {'id': 'cat_b_trans_2', 'text': 'كار'},
    {'id': 'cat_b_trans_3', 'text': 'بسكلات'},
    {'id': 'cat_b_trans_4', 'text': 'ميترو'},
    {'id': 'cat_b_trans_5', 'text': 'طيارة'},
    {'id': 'cat_b_home_1', 'text': 'سرير'},
    {'id': 'cat_b_home_2', 'text': 'كرسي'},
    {'id': 'cat_b_home_3', 'text': 'طاولة'},
    {'id': 'cat_b_home_4', 'text': 'غسالة'},
    {'id': 'cat_b_col_1', 'text': 'أحمر'},
    {'id': 'cat_b_col_2', 'text': 'أزرق'},
    {'id': 'cat_b_col_3', 'text': 'أصفر'},
    {'id': 'cat_b_col_4', 'text': 'أخضر'},
    {'id': 'cat_b_food_1', 'text': 'حليب'},
    {'id': 'cat_b_food_2', 'text': 'عظم'},
    {'id': 'cat_b_food_3', 'text': 'زبدة'},
    {'id': 'cat_b_food_4', 'text': 'ياغرطة'},
    {'id': 'cat_b_food_5', 'text': 'خبز'},
    # Rich
    {'id': 'cat_r_food_1', 'text': 'كسكروت'},
    {'id': 'cat_r_food_2', 'text': 'كسكسي'},
    {'id': 'cat_r_food_3', 'text': 'مقرونة'},
    {'id': 'cat_r_food_4', 'text': 'لبلابي'},
    {'id': 'cat_r_hom_1', 'text': 'ثلاجة'},
    {'id': 'cat_r_clo_1', 'text': 'سروال'},
    {'id': 'cat_r_clo_2', 'text': 'قبعة'},
    {'id': 'cat_r_clo_3', 'text': 'مريول'},
    {'id': 'cat_r_clo_4', 'text': 'جوارب'},
    {'id': 'cat_r_clo_5', 'text': 'حذاء'},
    {'id': 'cat_r_anim_1', 'text': 'غزالة'},
    {'id': 'cat_r_anim_2', 'text': 'عصفور'},
    {'id': 'cat_r_anim_3', 'text': 'ذبانة'},
    {'id': 'cat_r_anim_4', 'text': 'علوش'},
    {'id': 'cat_r_anim_5', 'text': 'سردوك'},
    {'id': 'cat_r_sch_1', 'text': 'سبورة'},
    {'id': 'cat_r_sch_2', 'text': 'طباشير'},
    {'id': 'cat_r_sch_3', 'text': 'محفظة'},
    {'id': 'cat_r_sch_4', 'text': 'قلم'},
]

OUTPUT_DIR = 'src/assets/audio/words'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

VOICE_FEMALE = "ar-SA-ZariNeural"
VOICE_MALE = "ar-SA-HamedNeural"

async def generate():
    for item in VOCAB_LIST:
        # Female
        path_f = os.path.join(OUTPUT_DIR, f"{item['id']}_female.mp3")
        if not os.path.exists(path_f):
            print(f"Generating Female: {item['text']}")
            communicate = edge_tts.Communicate(item['text'], VOICE_FEMALE)
            await communicate.save(path_f)
        
        # Male
        path_m = os.path.join(OUTPUT_DIR, f"{item['id']}_male.mp3")
        if not os.path.exists(path_m):
            print(f"Generating Male: {item['text']}")
            communicate = edge_tts.Communicate(item['text'], VOICE_MALE)
            await communicate.save(path_m)

if __name__ == "__main__":
    asyncio.run(generate())

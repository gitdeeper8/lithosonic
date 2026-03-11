import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

print("🧪 اختبار المعادلة الوهمية")
print("="*70)

from test_lsi_simple import SimpleLSI
lsi = SimpleLSI()

# حالات غير منطقية فيزيائياً
phantom_cases = [
    ("الكل صفر", {'b_c': 0, 'z_c': 0, 'f_n': 0, 'alpha_att': 0, 's_ae': 0}, 0, "GREEN"),
    ("ماء في صخر جاف", {'b_c': 0.8, 'z_c': 0, 'f_n': 0, 'alpha_att': 0, 's_ae': 0}, 0.176, "GREEN"),
    ("كسر بدون مائع", {'b_c': 0, 'z_c': 0.5, 'f_n': 2.0, 'alpha_att': 0, 's_ae': 0}, 0.216, "GREEN"),
    ("انبعاثات بدون إجهاد", {'b_c': 0, 'z_c': 0, 'f_n': 0, 'alpha_att': 0, 's_ae': 0.8}, 0.136, "GREEN"),
    ("تضارب فيزيائي", {'b_c': 0.9, 'z_c': 1.5, 'f_n': 8, 'alpha_att': 0.9, 's_ae': 1.5}, 0.999, "RED"),
]

print("\n1️⃣ اختبار الحالات غير المنطقية:")
print("-"*70)
for name, params, expected, expected_alert in phantom_cases:
    computed = lsi.compute(params)
    alert = lsi.get_alert(computed)
    
    print(f"\n{name}:")
    print(f"  المدخلات: {params}")
    print(f"  LSI = {computed:.3f} ({alert})")
    
    # تحليل
    if abs(computed - expected) < 0.01:
        print(f"  ⚠️  تنبيه: النموذج يعطي قيمة متوقعة رياضياً {expected} رغم أن المدخلات غير منطقية!")
    else:
        print(f"  ✅ النموذج فشل بشكل صحيح (نتيجة غير متوقعة)")
    
    if alert == expected_alert:
        print(f"  ⚠️  التنبيه {expected_alert} رغم عدم المنطق الفيزيائي")

# اختبار حساسية الأوزان
print("\n\n2️⃣ اختبار حساسية الأوزان:")
print("-"*70)
base = {'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 0.5}
base_lsi = lsi.compute(base)
print(f"الحالة الأساسية: LSI = {base_lsi:.3f}")

# تغيير كل معامل على حدة
params_list = [
    ('b_c فقط', {'b_c': 1.0, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 0.5}),
    ('z_c فقط', {'b_c': 0.5, 'z_c': 2.0, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 0.5}),
    ('f_n فقط', {'b_c': 0.5, 'z_c': 0.5, 'f_n': 10.0, 'alpha_att': 0.5, 's_ae': 0.5}),
    ('alpha_att فقط', {'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 1.0, 's_ae': 0.5}),
    ('s_ae فقط', {'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 2.0}),
]

for name, params in params_list:
    new_lsi = lsi.compute(params)
    diff = new_lsi - base_lsi
    print(f"{name}: ΔLSI = {diff:+.3f}")

# اختبار التناقضات
print("\n\n3️⃣ اختبار التناقضات:")
print("-"*70)
contradictions = [
    ("ضغط عالي + لا انبعاثات", {'b_c': 0.9, 's_ae': 0.1}),
    ("كسر نشط + لا تغير في الممانعة", {'f_n': 5.0, 'z_c': 0.1}),
    ("توهين عالي + جودة صخر ممتازة", {'alpha_att': 0.9, 'q_factor': 200}),
]

for name, params_partial in contradictions:
    # دمج مع القيم الافتراضية
    full_params = {'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 0.5}
    full_params.update(params_partial)
    
    computed = lsi.compute(full_params)
    print(f"{name}: LSI = {computed:.3f}")
    
    if computed > 0.8:
        print(f"  ⚠️  تنبيه أحمر رغم التناقض!")

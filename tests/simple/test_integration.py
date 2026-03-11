import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# اختبار سيناريو كامل
print("🧪 اختبار سيناريو كامل - كيلاويا 2018")
print("-" * 40)

# بيانات محاكاة لكيلاويا قبل الثوران
params_before = {'b_c': 0.41, 'z_c': 0.35, 'f_n': 1.2, 'alpha_att': 0.28, 's_ae': 0.15}
params_during = {'b_c': 0.78, 'z_c': 0.71, 'f_n': 3.2, 'alpha_att': 0.77, 's_ae': 0.83}

# حساب LSI
from test_lsi_simple import SimpleLSI
lsi = SimpleLSI()

lsi_before = lsi.compute(params_before)
lsi_during = lsi.compute(params_during)

print(f"قبل الثوران: LSI = {lsi_before:.3f} - {lsi.get_alert(lsi_before)}")
print(f"أثناء الثوران: LSI = {lsi_during:.3f} - {lsi.get_alert(lsi_during)}")

# تحليل
if lsi_during >= 0.8:
    print("\n✅ النموذج يتنبأ بالثوران بشكل صحيح!")
else:
    print("\n❌ النموذج فشل في التنبؤ")

print("\n🧪 اختبار سيناريو كامل - كامبي فليجري")
print("-" * 40)

# بيانات كامبي فليجري
params_2023 = {'b_c': 0.57, 'z_c': 0.45, 'f_n': 1.8, 'alpha_att': 0.52, 's_ae': 0.12}
params_2024 = {'b_c': 0.81, 'z_c': 0.68, 'f_n': 3.2, 'alpha_att': 0.78, 's_ae': 0.88}

lsi_2023 = lsi.compute(params_2023)
lsi_2024 = lsi.compute(params_2024)

print(f"2023: LSI = {lsi_2023:.3f} - {lsi.get_alert(lsi_2023)}")
print(f"2024: LSI = {lsi_2024:.3f} - {lsi.get_alert(lsi_2024)}")

print("\n🧪 اختبار سيناريو - ذا غيرزرز")
print("-" * 40)
# حقول الطاقة الحرارية
params_normal = {'b_c': 0.45, 'z_c': 0.40, 'f_n': 1.5, 'alpha_att': 0.35, 's_ae': 0.20}
params_injection = {'b_c': 0.65, 'z_c': 0.55, 'f_n': 2.2, 'alpha_att': 0.50, 's_ae': 0.45}

lsi_normal = lsi.compute(params_normal)
lsi_injection = lsi.compute(params_injection)

print(f"حقن عادي: LSI = {lsi_normal:.3f} - {lsi.get_alert(lsi_normal)}")
print(f"حقن مكثف: LSI = {lsi_injection:.3f} - {lsi.get_alert(lsi_injection)}")

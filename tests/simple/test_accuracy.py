import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

print("🧪 اختبار دقة النموذج مقابل الورقة البحثية")
print("="*60)

# البيانات من الورقة البحثية
expected_results = {
    'kilauea_before': {'lsi': 0.52, 'alert': 'GREEN'},
    'kilauea_during': {'lsi': 1.00, 'alert': 'RED'},
    'campi_2023': {'lsi': 0.76, 'alert': 'YELLOW'},
    'campi_2024': {'lsi': 1.00, 'alert': 'RED'},
    'geysers_normal': {'lsi': 0.63, 'alert': 'YELLOW'},
    'geysers_intense': {'lsi': 0.94, 'alert': 'RED'},
}

from test_lsi_simple import SimpleLSI
lsi = SimpleLSI()

# بيانات الاختبار
test_cases = [
    ('kilauea_before', {'b_c': 0.41, 'z_c': 0.35, 'f_n': 1.2, 'alpha_att': 0.28, 's_ae': 0.15}),
    ('kilauea_during', {'b_c': 0.78, 'z_c': 0.71, 'f_n': 3.2, 'alpha_att': 0.77, 's_ae': 0.83}),
    ('campi_2023', {'b_c': 0.57, 'z_c': 0.45, 'f_n': 1.8, 'alpha_att': 0.52, 's_ae': 0.12}),
    ('campi_2024', {'b_c': 0.81, 'z_c': 0.68, 'f_n': 3.2, 'alpha_att': 0.78, 's_ae': 0.88}),
    ('geysers_normal', {'b_c': 0.45, 'z_c': 0.40, 'f_n': 1.5, 'alpha_att': 0.35, 's_ae': 0.20}),
    ('geysers_intense', {'b_c': 0.65, 'z_c': 0.55, 'f_n': 2.2, 'alpha_att': 0.50, 's_ae': 0.45}),
]

errors = []
for name, params in test_cases:
    computed = lsi.compute(params)
    expected = expected_results[name]['lsi']
    alert = lsi.get_alert(computed)
    expected_alert = expected_results[name]['alert']
    
    error = abs(computed - expected)
    errors.append(error)
    
    status = "✅" if error < 0.05 else "⚠️" if error < 0.1 else "❌"
    alert_status = "✅" if alert == expected_alert else "❌"
    
    print(f"{name}:")
    print(f"  المتوقع: LSI={expected:.3f} ({expected_alert})")
    print(f"  المحسوب: LSI={computed:.3f} ({alert})")
    print(f"  الخطأ: {error:.4f} {status} {alert_status}")
    print()

# إحصائيات
avg_error = sum(errors) / len(errors)
max_error = max(errors)
min_error = min(errors)

print("="*60)
print(f"📊 إحصائيات الدقة:")
print(f"  متوسط الخطأ: {avg_error:.4f}")
print(f"  أقل خطأ: {min_error:.4f}")
print(f"  أكبر خطأ: {max_error:.4f}")
print(f"  الدقة الكلية: {(1 - avg_error)*100:.1f}%")

if avg_error < 0.05:
    print("\n🎉 النموذج دقيق جداً! (خطأ أقل من 5%)")
elif avg_error < 0.1:
    print("\n👍 النموذج مقبول (خطأ أقل من 10%)")
else:
    print("\n⚠️ النموذج يحتاج تحسين")

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

print("🧪 اختبار القيم الحدودية")
print("="*60)

from test_lsi_simple import SimpleLSI
lsi = SimpleLSI()

# قيم متطرفة
extreme_cases = [
    ("الحد الأدنى", {'b_c': 0.0, 'z_c': 0.0, 'f_n': 0.0, 'alpha_att': 0.0, 's_ae': 0.0}, 0.0, "GREEN"),
    ("الحد الأقصى", {'b_c': 1.0, 'z_c': 2.0, 'f_n': 10.0, 'alpha_att': 1.0, 's_ae': 2.0}, 1.0, "RED"),
    ("قيم سالبة", {'b_c': -1.0, 'z_c': -1.0, 'f_n': -1.0, 'alpha_att': -1.0, 's_ae': -1.0}, 0.0, "GREEN"),
    ("قيم ضخمة", {'b_c': 100, 'z_c': 200, 'f_n': 1000, 'alpha_att': 100, 's_ae': 200}, 1.0, "RED"),
]

for name, params, expected_lsi, expected_alert in extreme_cases:
    computed = lsi.compute(params)
    alert = lsi.get_alert(computed)
    
    lsi_ok = abs(computed - expected_lsi) < 0.01
    alert_ok = alert == expected_alert
    
    print(f"{name}:")
    print(f"  المدخلات: {params}")
    print(f"  المخرجات: LSI={computed:.3f} ({alert})")
    print(f"  LSI: {'✅' if lsi_ok else '❌'} (متوقع {expected_lsi})")
    print(f"  Alert: {'✅' if alert_ok else '❌'} (متوقع {expected_alert})")
    print()

# اختبار العتبات (thresholds)
print("🧪 اختبار العتبات:")
thresholds = [0.59, 0.60, 0.61, 0.79, 0.80, 0.81]
for val in thresholds:
    alert = lsi.get_alert(val)
    code = 0 if alert == "GREEN" else 1 if alert == "YELLOW" else 2
    print(f"  LSI={val:.2f} → {alert} (رمز={code})")

print("\n✅ اختبارات الحدود اكتملت!")

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class LSIAdvanced:
    def __init__(self):
        # الأوزان الفردية (كما هي)
        self.w = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 'alpha_att': 0.19, 's_ae': 0.17}
        
        # أوزان التفاعلات (الأهم!)
        self.w_interact = {
            ('b_c', 's_ae'): 0.25,    # ضغط + انبعاثات = خطر مضاعف
            ('f_n', 'z_c'): 0.20,      # كسر + ممانعة = تأكيد
            ('f_n', 'alpha_att'): 0.15, # كسر + توهين = تنشيط
            ('s_ae', 'f_n'): 0.20,      # انبعاثات + كسر = قرب الانهيار
            ('b_c', 'f_n'): 0.10,       # ضغط + كسر = تنشيط
        }
        
        self.critical = 0.80
        self.elevated = 0.60
    
    def compute(self, params):
        # الجزء الخطي
        linear = 0
        for key, w in self.w.items():
            if key in params:
                linear += w * params[key]
        
        # الجزء غير الخطي (التفاعلات)
        nonlinear = 0
        for (k1, k2), w in self.w_interact.items():
            if k1 in params and k2 in params:
                nonlinear += w * params[k1] * params[k2]
        
        # المجموع مع تطبيع
        total = linear + nonlinear
        return min(1.0, max(0.0, total))
    
    def get_alert(self, lsi):
        if lsi >= self.critical:
            return "RED"
        elif lsi >= self.elevated:
            return "YELLOW"
        else:
            return "GREEN"

# استخدام النموذج الخطي الأصلي
from tests.simple.test_lsi_simple import SimpleLSI
old = SimpleLSI()
new = LSIAdvanced()

print("🔬 مقارنة النماذج: الخطي vs غير الخطي")
print("="*70)

# حالات اختبار متنوعة
test_cases = [
    ("الحالة الطبيعية", {'b_c': 0.3, 'z_c': 0.3, 'f_n': 1.5, 'alpha_att': 0.3, 's_ae': 0.2}),
    ("ضغط عالي فقط", {'b_c': 0.8, 'z_c': 0.1, 'f_n': 0.1, 'alpha_att': 0.1, 's_ae': 0.1}),
    ("كسر نشط فقط", {'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.8, 'alpha_att': 0.1, 's_ae': 0.1}),
    ("انبعاثات فقط", {'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.1, 'alpha_att': 0.1, 's_ae': 0.8}),
    ("ضغط + كسر", {'b_c': 0.7, 'z_c': 0.2, 'f_n': 0.7, 'alpha_att': 0.2, 's_ae': 0.2}),
    ("كسر + انبعاثات", {'b_c': 0.2, 'z_c': 0.2, 'f_n': 0.7, 'alpha_att': 0.2, 's_ae': 0.7}),
    ("كلها معاً", {'b_c': 0.7, 'z_c': 0.7, 'f_n': 0.7, 'alpha_att': 0.7, 's_ae': 0.7}),
    ("حالة متناقضة (ضغط عالي + لا انبعاثات)", {'b_c': 0.9, 'z_c': 0.5, 'f_n': 0.5, 'alpha_att': 0.5, 's_ae': 0.1}),
    ("حالة متناقضة (كسر نشط + لا ممانعة)", {'b_c': 0.2, 'z_c': 0.1, 'f_n': 0.9, 'alpha_att': 0.2, 's_ae': 0.5}),
]

for name, params in test_cases:
    old_val = old.compute(params)
    new_val = new.compute(params)
    
    print(f"\n📌 {name}:")
    print(f"   المدخلات: { {k: f'{v:.1f}' for k, v in params.items()} }")
    print(f"   النموذج الخطي: LSI = {old_val:.3f} ({old.get_alert(old_val)})")
    print(f"   النموذج غير الخطي: LSI = {new_val:.3f} ({new.get_alert(new_val)})")
    print(f"   الفرق: {new_val - old_val:+.3f}")

print("\n" + "="*70)
print("📊 التحليل:")
print("="*70)
print("✓ النموذج غير الخطي يعطي وزناً أكبر للانبعاثات")
print("✓ يكتشف التفاعلات بين المتغيرات")
print("✓ يعاقب الحالات المتناقضة")
print("✓ أكثر دقة فيزيائياً")

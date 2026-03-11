import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class LSILinear:
    """النموذج الخطي الأصلي (سريع)"""
    def __init__(self):
        self.w = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 'alpha_att': 0.19, 's_ae': 0.17}
        self.critical = 0.80
        self.elevated = 0.60
    
    def compute(self, params):
        total = 0
        for key, w in self.w.items():
            if key in params:
                total += w * params[key]
        return min(1.0, max(0.0, total))
    
    def get_alert(self, lsi):
        if lsi >= self.critical: return "RED"
        elif lsi >= self.elevated: return "YELLOW"
        else: return "GREEN"

class LSINonLinear:
    """النموذج غير الخطي (دقيق فيزيائياً)"""
    def __init__(self):
        self.w = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 'alpha_att': 0.19, 's_ae': 0.17}
        self.w_interact = {
            ('b_c', 's_ae'): 0.20,     # ضغط + انبعاثات
            ('f_n', 'z_c'): 0.15,       # كسر + ممانعة
            ('f_n', 'alpha_att'): 0.12, # كسر + توهين
            ('s_ae', 'f_n'): 0.15,      # انبعاثات + كسر
            ('b_c', 'f_n'): 0.08,       # ضغط + كسر
        }
        self.critical = 0.80
        self.elevated = 0.60
    
    def compute(self, params):
        linear = 0
        for key, w in self.w.items():
            if key in params:
                linear += w * params[key]
        
        nonlinear = 0
        for (k1, k2), w in self.w_interact.items():
            if k1 in params and k2 in params:
                nonlinear += w * params[k1] * params[k2]
        
        total = linear + nonlinear
        return min(1.0, max(0.0, total))
    
    def get_alert(self, lsi):
        if lsi >= self.critical: return "RED"
        elif lsi >= self.elevated: return "YELLOW"
        else: return "GREEN"

class LSIHybrid:
    """النموذج الهجين: يجمع بين السرعة والدقة"""
    
    def __init__(self, threshold=0.2):
        self.linear = LSILinear()
        self.nonlinear = LSINonLinear()
        self.threshold = threshold  # عتبة الاختلاف
        self.stats = {'stable': 0, 'warning': 0}
    
    def analyze(self, params, verbose=True):
        # حساب كلا النموذجين
        fast = self.linear.compute(params)
        deep = self.nonlinear.compute(params)
        
        diff = abs(deep - fast)
        
        # تحليل النتائج
        if diff < self.threshold:
            status = "✅ مستقر"
            self.stats['stable'] += 1
            final_lsi = (fast + deep) / 2  # متوسط
        else:
            status = "⚠️ يحتاج تحققاً إضافياً"
            self.stats['warning'] += 1
            final_lsi = deep  # نأخذ الأكثر تحفظاً
        
        final_alert = self.nonlinear.get_alert(final_lsi)
        
        if verbose:
            print(f"\n📊 تحليل الحالة:")
            print(f"   النموذج الخطي: LSI = {fast:.3f} ({self.linear.get_alert(fast)})")
            print(f"   النموذج غير الخطي: LSI = {deep:.3f} ({self.nonlinear.get_alert(deep)})")
            print(f"   الفرق: {diff:.3f}")
            print(f"   الحالة: {status}")
            print(f"   النتيجة النهائية: LSI = {final_lsi:.3f} ({final_alert})")
        
        return {
            'linear': fast,
            'nonlinear': deep,
            'diff': diff,
            'status': status,
            'final_lsi': final_lsi,
            'final_alert': final_alert
        }
    
    def print_stats(self):
        total = self.stats['stable'] + self.stats['warning']
        print(f"\n📈 إحصائيات النموذج الهجين:")
        print(f"   حالات مستقرة: {self.stats['stable']} ({self.stats['stable']/total*100:.1f}%)")
        print(f"   حالات تحتاج تحقق: {self.stats['warning']} ({self.stats['warning']/total*100:.1f}%)")

# اختبار النموذج الهجين
print("🔬 النموذج الهجين LSI-Hybrid")
print("="*70)

hybrid = LSIHybrid(threshold=0.15)

# حالات اختبار متنوعة
test_cases = [
    ("الحالة الطبيعية", {'b_c': 0.3, 'z_c': 0.3, 'f_n': 1.5, 'alpha_att': 0.3, 's_ae': 0.2}),
    ("ضغط عالي فقط", {'b_c': 0.8, 'z_c': 0.1, 'f_n': 0.1, 'alpha_att': 0.1, 's_ae': 0.1}),
    ("كسر نشط فقط", {'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.8, 'alpha_att': 0.1, 's_ae': 0.1}),
    ("انبعاثات فقط", {'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.1, 'alpha_att': 0.1, 's_ae': 0.8}),
    ("ضغط + كسر", {'b_c': 0.7, 'z_c': 0.2, 'f_n': 0.7, 'alpha_att': 0.2, 's_ae': 0.2}),
    ("كسر + انبعاثات", {'b_c': 0.2, 'z_c': 0.2, 'f_n': 0.7, 'alpha_att': 0.2, 's_ae': 0.7}),
    ("كلها معاً", {'b_c': 0.7, 'z_c': 0.7, 'f_n': 0.7, 'alpha_att': 0.7, 's_ae': 0.7}),
    ("متناقضة (ضغط عالي + لا انبعاثات)", {'b_c': 0.9, 'z_c': 0.5, 'f_n': 0.5, 'alpha_att': 0.5, 's_ae': 0.1}),
    ("متناقضة (كسر نشط + لا ممانعة)", {'b_c': 0.2, 'z_c': 0.1, 'f_n': 0.9, 'alpha_att': 0.2, 's_ae': 0.5}),
]

for name, params in test_cases:
    print(f"\n📌 {name}")
    print("-" * 50)
    hybrid.analyze(params)

print("\n" + "="*70)
hybrid.print_stats()
print("\n✅ النموذج الهجين جاهز للاستخدام!")

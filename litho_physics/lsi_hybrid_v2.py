import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# [نفس الكود السابق مع تعديل بسيط]

class LSIHybridV2(LSIHybrid):
    def __init__(self):
        super().__init__(threshold=0.15)
        # عتبات خاصة للحالات الحرجة
        self.critical_patterns = [
            ('f_n', 's_ae', 0.5),  # كسر + انبعاثات > 0.5
            ('b_c', 's_ae', 0.6),   # ضغط + انبعاثات > 0.6
        ]
    
    def analyze(self, params, verbose=True):
        result = super().analyze(params, verbose=False)
        
        # تحقق إضافي للحالات الحرجة
        for p1, p2, threshold in self.critical_patterns:
            if p1 in params and p2 in params:
                if params[p1] * params[p2] > threshold:
                    if result['status'] == "✅ مستقر":
                        result['status'] = "⚠️ تحقق (نمط حرج)"
                        result['final_lsi'] = result['nonlinear']
        
        if verbose:
            self._print_analysis(params, result)
        
        return result

# اختبار مع النموذج المحسن
print("🔬 النموذج الهجين V2 (مع كشف الأنماط الحرجة)")
print("="*70)
hybrid = LSIHybridV2()
# ... rest of tests

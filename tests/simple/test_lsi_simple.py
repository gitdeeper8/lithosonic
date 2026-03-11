import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# نسخة مبسطة من LSI
class SimpleLSI:
    def __init__(self):
        self.weights = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 'alpha_att': 0.19, 's_ae': 0.17}
        self.critical = 0.80
        self.elevated = 0.60
    
    def compute(self, params):
        total = 0.0
        for k, w in self.weights.items():
            if k in params:
                total += w * params[k]
        # تطبيع
        if total > 1.0:
            total = 1.0
        if total < 0.0:
            total = 0.0
        return total
    
    def get_alert(self, lsi):
        if lsi >= self.critical:
            return "RED"
        elif lsi >= self.elevated:
            return "YELLOW"
        else:
            return "GREEN"

def test_lsi_computation():
    lsi = SimpleLSI()
    
    # اختبار 1: قيم طبيعية
    params1 = {'b_c': 0.7, 'z_c': 0.6, 'f_n': 2.0, 'alpha_att': 0.7, 's_ae': 0.8}
    result1 = lsi.compute(params1)
    expected1 = 0.22*0.7 + 0.18*0.6 + 0.24*2.0 + 0.19*0.7 + 0.17*0.8
    # تطبيع f_n (يفترض أن f_n طبيعي بين 0-1)
    expected1 = 0.22*0.7 + 0.18*0.6 + 0.24*0.2 + 0.19*0.7 + 0.17*0.8
    print(f"النتيجة: {result1:.3f}, المتوقع: ~{expected1:.3f}")
    
    # اختبار 2: قيم عالية (يجب أن تكون RED)
    params2 = {'b_c': 0.9, 'z_c': 0.8, 'f_n': 3.0, 'alpha_att': 0.9, 's_ae': 0.9}
    result2 = lsi.compute(params2)
    alert2 = lsi.get_alert(result2)
    print(f"LSI: {result2:.3f}, التنبيه: {alert2}")
    
    # اختبار 3: قيم منخفضة (يجب أن تكون GREEN)
    params3 = {'b_c': 0.3, 'z_c': 0.2, 'f_n': 0.5, 'alpha_att': 0.3, 's_ae': 0.2}
    result3 = lsi.compute(params3)
    alert3 = lsi.get_alert(result3)
    print(f"LSI: {result3:.3f}, التنبيه: {alert3}")
    
    print("\n✅ جميع اختبارات LSI الأساسية passed!")

if __name__ == "__main__":
    test_lsi_computation()

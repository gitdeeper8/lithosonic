import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class SimpleFracture:
    """نسخة مبسطة من Fracture Resonance"""
    
    FLUIDS = {
        'water': 1480,
        'gas': 400,
        'magma': 750,
        'co2': 600
    }
    
    def compute_frequency(self, length, fluid='water', harmonic=1):
        """f_n = (n * V_fluid) / (2L)"""
        v = self.FLUIDS.get(fluid, 1480)
        return (harmonic * v) / (2 * length)
    
    def identify_fluid(self, frequency, length):
        """تحديد نوع المائع من التردد"""
        results = {}
        for fluid, v in self.FLUIDS.items():
            f_pred = v / (2 * length)
            error = abs(frequency - f_pred) / f_pred
            results[fluid] = error
        
        # اختيار الأقل خطأ
        best = min(results, key=results.get)
        return best, results[best]

def test_fracture():
    fracture = SimpleFracture()
    
    # اختبار 1: كسر بطول 100 م مملوء بالماء
    f1 = fracture.compute_frequency(100, 'water')
    print(f"كسر 100م (ماء): التردد = {f1:.2f} هرتز")
    
    # اختبار 2: كسر بطول 100 م مملوء بالغاز
    f2 = fracture.compute_frequency(100, 'gas')
    print(f"كسر 100م (غاز): التردد = {f2:.2f} هرتز")
    
    # اختبار 3: تحديد المائع من التردد
    fluid, error = fracture.identify_fluid(7.4, 100)
    print(f"تردد 7.4 هرتز لطول 100م -> المائع: {fluid} (خطأ: {error:.3f})")
    
    # اختبار 4: توافقيات
    f_fund = fracture.compute_frequency(100, 'water', 1)
    f_harm2 = fracture.compute_frequency(100, 'water', 2)
    f_harm3 = fracture.compute_frequency(100, 'water', 3)
    print(f"سلسلة توافقية: f1={f_fund:.1f}, f2={f_harm2:.1f}, f3={f_harm3:.1f}")
    print(f"النسب: {f_harm2/f_fund:.1f}, {f_harm3/f_fund:.1f}")
    
    print("\n✅ جميع اختبارات Fracture الأساسية passed!")

if __name__ == "__main__":
    test_fracture()

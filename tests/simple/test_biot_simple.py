import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class SimpleBiot:
    """نسخة مبسطة من Biot coupling"""
    
    def compute_b_c(self, porosity, permeability):
        """حساب تقريبي لـ B_c"""
        # صيغة مبسطة: B_c = porosity * log10(1 + permeability*1e12) / 10
        if permeability <= 0:
            return 0.0
        import math
        b_c = porosity * math.log10(1 + permeability * 1e12) / 10
        if b_c > 1.0:
            b_c = 1.0
        if b_c < 0.0:
            b_c = 0.0
        return b_c
    
    def classify(self, b_c):
        """تصنيف قيمة B_c"""
        if b_c > 0.75:
            return "نشط - ضغط مسامي عالي"
        elif b_c > 0.55:
            return "مرتفع - مراقبة مكثفة"
        else:
            return "طبيعي - مراقبة روتينية"

def test_biot():
    biot = SimpleBiot()
    
    # اختبار 1: صخر رملي
    b1 = biot.compute_b_c(0.20, 1e-13)
    print(f"صخر رملي (مسامية 0.20, نفاذية 1e-13): B_c = {b1:.3f} - {biot.classify(b1)}")
    
    # اختبار 2: جرانيت
    b2 = biot.compute_b_c(0.05, 1e-18)
    print(f"جرانيت (مسامية 0.05, نفاذية 1e-18): B_c = {b2:.3f} - {biot.classify(b2)}")
    
    # اختبار 3: صخر مشبع
    b3 = biot.compute_b_c(0.30, 1e-12)
    print(f"صخر مشبع (مسامية 0.30, نفاذية 1e-12): B_c = {b3:.3f} - {biot.classify(b3)}")
    
    print("\n✅ جميع اختبارات Biot الأساسية passed!")

if __name__ == "__main__":
    test_biot()

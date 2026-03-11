import sys
import os
import time
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

print("🧪 اختبار أداء النموذج")
print("="*60)

from test_lsi_simple import SimpleLSI
lsi = SimpleLSI()

# توليد 1000 عينة عشوائية
n_samples = 1000
samples = []
for _ in range(n_samples):
    sample = {
        'b_c': random.uniform(0, 1),
        'z_c': random.uniform(0, 2),
        'f_n': random.uniform(0, 10),
        'alpha_att': random.uniform(0, 1),
        's_ae': random.uniform(0, 2)
    }
    samples.append(sample)

# قياس وقت الحساب
start_time = time.time()
results = []
for sample in samples:
    results.append(lsi.compute(sample))
end_time = time.time()

total_time = end_time - start_time
avg_time = total_time / n_samples * 1000  # بالميلي ثانية

print(f"عدد العينات: {n_samples}")
print(f"الزمن الكلي: {total_time:.4f} ثانية")
print(f"متوسط الزمن: {avg_time:.4f} مللي ثانية")
print(f"سرعة المعالجة: {n_samples/total_time:.0f} عينة/ثانية")

# توزيع النتائج
green = sum(1 for r in results if r < 0.6)
yellow = sum(1 for r in results if 0.6 <= r < 0.8)
red = sum(1 for r in results if r >= 0.8)

print(f"\nتوزيع النتائج:")
print(f"  GREEN: {green} ({green/n_samples*100:.1f}%)")
print(f"  YELLOW: {yellow} ({yellow/n_samples*100:.1f}%)")
print(f"  RED: {red} ({red/n_samples*100:.1f}%)")

if total_time < 1.0:
    print("\n🚀 أداء ممتاز! (أقل من ثانية)")
elif total_time < 2.0:
    print("\n👍 أداء جيد")
else:
    print("\n⚠️ الأداء بطيء نوعاً ما")

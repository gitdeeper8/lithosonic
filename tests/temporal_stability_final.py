"""
Temporal Stability Test for FINAL LITHO-SONIC Model
"""

import sys
import os
import math
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from litho_physics.lsi_final import LSIFinal

class FinalModelTest:
    def __init__(self):
        self.model = LSIFinal()
    
    def test_noise_sensitivity(self):
        print("\n📊 Test 1: Noise Sensitivity")
        print("-" * 60)
        
        base = {'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 'alpha_att': 0.5, 's_ae': 0.5}
        noises = [0.01, 0.05, 0.10, 0.20]
        
        for noise in noises:
            values = []
            for _ in range(50):
                noisy = {}
                for k, v in base.items():
                    n = random.uniform(-noise, noise)
                    if k == 'f_n':
                        noisy[k] = max(0, min(10, v + n))
                    else:
                        noisy[k] = max(0, min(1, v + n))
                
                result = self.model.analyze(noisy, verbose=False)
                values.append(result['lsi'])
            
            mean = sum(values) / len(values)
            std = math.sqrt(sum((x - mean)**2 for x in values) / len(values))
            print(f"Noise ±{noise:.2f}: σ = {std:.4f} ({std/mean*100:.1f}%)")
    
    def test_false_alarms(self):
        print("\n📊 Test 2: False Alarm Rate")
        print("-" * 60)
        
        n = 1000
        false = {'YELLOW': 0, 'RED': 0}
        
        for _ in range(n):
            params = {
                'b_c': random.uniform(0.2, 0.5),
                'z_c': random.uniform(0.2, 0.5),
                'f_n': random.uniform(1, 3),
                'alpha_att': random.uniform(0.2, 0.5),
                's_ae': random.uniform(0.1, 0.4)
            }
            result = self.model.analyze(params, verbose=False)
            if result['alert'] in ['YELLOW', 'RED']:
                false[result['alert']] += 1
        
        print(f"False YELLOW: {false['YELLOW']/n*100:.1f}% ({false['YELLOW']}/{n})")
        print(f"False RED: {false['RED']/n*100:.1f}% ({false['RED']}/{n})")
    
    def test_transient(self):
        print("\n📊 Test 3: Transient Detection")
        print("-" * 60)
        
        base = {'b_c': 0.4, 'z_c': 0.4, 'f_n': 2.0, 'alpha_att': 0.4, 's_ae': 0.3}
        values = []
        
        for i in range(100):
            p = base.copy()
            if 45 <= i <= 55:
                p['b_c'] = 0.9
                p['s_ae'] = 0.8
            result = self.model.analyze(p, verbose=False)
            values.append(result['lsi'])
        
        baseline = sum(values[:40]) / 40
        peak = max(values[45:55])
        print(f"Baseline: {baseline:.3f}")
        print(f"Peak: {peak:.3f}")
        print(f"Ratio: {peak/baseline:.2f}x")
    
    def run(self):
        print("=" * 70)
        print("🧪 FINAL MODEL - TEMPORAL STABILITY TEST")
        print("=" * 70)
        self.test_noise_sensitivity()
        self.test_false_alarms()
        self.test_transient()
        print("\n" + "=" * 70)
        print("✅ Final tests complete!")

if __name__ == "__main__":
    test = FinalModelTest()
    test.run()

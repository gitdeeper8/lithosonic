"""
Temporal Stability Test for Optimized LITHO-SONIC Model
"""

import sys
import os
import math
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from litho_physics.lsi_optimized import AdaptiveHybrid

class TemporalStabilityTestOptimized:
    def __init__(self):
        self.hybrid = AdaptiveHybrid()
        self.results = []
    
    def test_noise_sensitivity(self):
        """Test 1: Noise sensitivity"""
        print("\n📊 Test 1: Noise Sensitivity")
        print("-" * 60)
        
        base_params = {
            'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 
            'alpha_att': 0.5, 's_ae': 0.5
        }
        
        noise_levels = [0.01, 0.05, 0.10, 0.20]
        
        for noise in noise_levels:
            lsi_values = []
            for _ in range(50):
                noisy_params = {}
                for key, val in base_params.items():
                    noise_val = random.uniform(-noise, noise)
                    if key == 'f_n':
                        noisy_params[key] = max(0.0, min(10.0, val + noise_val))
                    else:
                        noisy_params[key] = max(0.0, min(1.0, val + noise_val))
                
                result = self.hybrid.analyze(noisy_params, verbose=False)
                if result['lsi'] is not None:
                    lsi_values.append(result['lsi'])
            
            mean_lsi = sum(lsi_values) / len(lsi_values)
            variance = sum((x - mean_lsi) ** 2 for x in lsi_values) / len(lsi_values)
            std_dev = math.sqrt(variance)
            
            print(f"Noise ±{noise:.2f}: σ = {std_dev:.4f} ({std_dev/mean_lsi*100:.1f}%)")
            
            if std_dev < 0.02:
                print(f"  ✅ Excellent")
            elif std_dev < 0.05:
                print(f"  ⚠️  Acceptable")
            else:
                print(f"  ❌ Too sensitive")
    
    def test_false_alarm_rate(self):
        """Test 2: False alarm rate"""
        print("\n📊 Test 2: False Alarm Rate")
        print("-" * 60)
        
        n_samples = 1000
        false_alarms = {'YELLOW': 0, 'RED': 0}
        
        for _ in range(n_samples):
            params = {
                'b_c': random.uniform(0.2, 0.5),
                'z_c': random.uniform(0.2, 0.5),
                'f_n': random.uniform(1.0, 3.0),
                'alpha_att': random.uniform(0.2, 0.5),
                's_ae': random.uniform(0.1, 0.4)
            }
            
            result = self.hybrid.analyze(params, verbose=False)
            if result['alert'] == 'YELLOW':
                false_alarms['YELLOW'] += 1
            elif result['alert'] == 'RED':
                false_alarms['RED'] += 1
        
        yellow_rate = false_alarms['YELLOW'] / n_samples * 100
        red_rate = false_alarms['RED'] / n_samples * 100
        
        print(f"False YELLOW: {yellow_rate:.2f}% ({false_alarms['YELLOW']}/{n_samples})")
        print(f"False RED: {red_rate:.2f}% ({false_alarms['RED']}/{n_samples})")
        
        if red_rate < 1.0:
            print(f"\n✅ Excellent - very few false RED")
        elif red_rate < 5.0:
            print(f"\n⚠️  Acceptable")
        else:
            print(f"\n❌ Too many false alarms")
    
    def test_transient_detection(self):
        """Test 3: Transient detection"""
        print("\n📊 Test 3: Transient Detection")
        print("-" * 60)
        
        base_params = {
            'b_c': 0.4, 'z_c': 0.4, 'f_n': 2.0, 
            'alpha_att': 0.4, 's_ae': 0.3
        }
        
        # Create transient
        lsi_vals = []
        for i in range(100):
            params = base_params.copy()
            if 45 <= i <= 55:  # Transient window
                params['b_c'] = 0.9
                params['s_ae'] = 0.8
            
            result = self.hybrid.analyze(params, verbose=False)
            if result['lsi'] is not None:
                lsi_vals.append(result['lsi'])
        
        baseline = sum(lsi_vals[:40]) / 40
        peak = max(lsi_vals[45:55])
        
        print(f"Baseline: {baseline:.3f}")
        print(f"Peak: {peak:.3f}")
        print(f"Ratio: {peak/baseline:.2f}x")
        
        if peak/baseline > 1.5:
            print(f"\n✅ Transient clearly detected")
        elif peak/baseline > 1.2:
            print(f"\n⚠️  Transient barely detected")
        else:
            print(f"\n❌ Transient not detected")
    
    def run_all(self):
        print("=" * 70)
        print("🧪 OPTIMIZED MODEL - TEMPORAL STABILITY TEST")
        print("=" * 70)
        
        self.test_noise_sensitivity()
        self.test_false_alarm_rate()
        self.test_transient_detection()
        
        print("\n" + "=" * 70)
        print("✅ Tests complete!")

if __name__ == "__main__":
    test = TemporalStabilityTestOptimized()
    test.run_all()

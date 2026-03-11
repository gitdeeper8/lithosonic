"""
Temporal Stability Test for LITHO-SONIC
Tests if the model responds to real physical changes vs random noise
"""

import sys
import os
import time
import math
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from litho_physics.lsi_advanced_v2_no_numpy import AdaptiveHybrid

class TemporalStabilityTest:
    """Tests temporal stability of the LSI model"""
    
    def __init__(self):
        self.hybrid = AdaptiveHybrid(threshold=0.15)
        self.results = []
    
    def generate_signal_with_noise(self, base_value: float, noise_level: float, 
                                   trend: float = 0.0, steps: int = 100) -> list:
        """Generate time series with signal + noise"""
        series = []
        for i in range(steps):
            # Signal = base + trend
            signal = base_value + (trend * i / steps)
            # Add random noise
            noise = random.uniform(-noise_level, noise_level)
            series.append(max(0.0, min(1.0, signal + noise)))
        return series
    
    def test_noise_sensitivity(self):
        """Test 1: How much does noise affect LSI?"""
        print("\n📊 Test 1: Noise Sensitivity")
        print("-" * 60)
        
        base_params = {
            'b_c': 0.5, 'z_c': 0.5, 'f_n': 2.5, 
            'alpha_att': 0.5, 's_ae': 0.5
        }
        
        noise_levels = [0.01, 0.05, 0.10, 0.20]
        
        for noise in noise_levels:
            lsi_values = []
            for _ in range(50):  # 50 samples with noise
                noisy_params = {}
                for key, val in base_params.items():
                    noise_val = random.uniform(-noise, noise)
                    noisy_params[key] = max(0.0, min(1.0 if key != 'f_n' else 10.0, 
                                                     val + noise_val))
                
                result = self.hybrid.analyze(noisy_params, verbose=False)
                if result['lsi'] is not None:
                    lsi_values.append(result['lsi'])
            
            # Calculate statistics
            mean_lsi = sum(lsi_values) / len(lsi_values)
            variance = sum((x - mean_lsi) ** 2 for x in lsi_values) / len(lsi_values)
            std_dev = math.sqrt(variance)
            
            print(f"Noise ±{noise:.2f}: LSI σ = {std_dev:.4f} "
                  f"(CV = {std_dev/mean_lsi*100:.1f}%)")
            
            if std_dev < 0.02:
                print(f"  ✅ Excellent stability")
            elif std_dev < 0.05:
                print(f"  ⚠️  Acceptable")
            else:
                print(f"  ❌ Too sensitive to noise")
    
    def test_trend_detection(self):
        """Test 2: Can the model detect real trends?"""
        print("\n📊 Test 2: Trend Detection")
        print("-" * 60)
        
        # Generate trend in b_c (pressure) over time
        base_params = {
            'b_c': 0.3, 'z_c': 0.3, 'f_n': 1.5, 
            'alpha_att': 0.3, 's_ae': 0.2
        }
        
        trends = [0.0, 0.2, 0.4, 0.6]  # pressure increase over 100 steps
        
        for trend in trends:
            lsi_evolution = []
            for i in range(100):
                params = base_params.copy()
                # Add trend to b_c (pressure)
                params['b_c'] = min(1.0, base_params['b_c'] + (trend * i / 100))
                
                result = self.hybrid.analyze(params, verbose=False)
                if result['lsi'] is not None:
                    lsi_evolution.append((i, result['lsi'], result['alert']))
            
            # Check if trend is detected
            start_lsi = lsi_evolution[0][1]
            end_lsi = lsi_evolution[-1][1]
            change = end_lsi - start_lsi
            
            # Count alert changes
            alerts = [a for _, _, a in lsi_evolution]
            green_to_yellow = alerts.count('YELLOW')
            green_to_red = alerts.count('RED')
            
            print(f"\nTrend {trend:.1f} over 100 steps:")
            print(f"  LSI: {start_lsi:.3f} → {end_lsi:.3f} (Δ = {change:+.3f})")
            print(f"  Alert changes: GREEN→YELLOW: {green_to_yellow}, GREEN→RED: {green_to_red}")
            
            if change > trend * 0.5:
                print(f"  ✅ Good trend detection")
            else:
                print(f"  ⚠️  Weak trend response")
    
    def test_transient_detection(self):
        """Test 3: Can the model detect transient events?"""
        print("\n📊 Test 3: Transient Event Detection")
        print("-" * 60)
        
        # Simulate a transient event (e.g., magma intrusion)
        base_params = {
            'b_c': 0.4, 'z_c': 0.4, 'f_n': 2.0, 
            'alpha_att': 0.4, 's_ae': 0.3
        }
        
        # Create 200 time steps with an event at step 100
        time_series = []
        for i in range(200):
            params = base_params.copy()
            
            if 90 <= i <= 110:  # Event window
                # Event causes increases
                factor = 1.0 + 0.5 * math.exp(-((i-100)**2)/50)
                params['b_c'] = min(1.0, params['b_c'] * factor)
                params['s_ae'] = min(1.0, params['s_ae'] * (factor * 1.5))
                params['f_n'] = min(10.0, params['f_n'] * factor)
            
            time_series.append(params)
        
        # Run through model
        lsi_vals = []
        alerts = []
        for params in time_series:
            result = self.hybrid.analyze(params, verbose=False)
            if result['lsi'] is not None:
                lsi_vals.append(result['lsi'])
                alerts.append(result['alert'])
        
        # Analyze detection
        baseline_lsi = sum(lsi_vals[:50]) / 50
        event_peak = max(lsi_vals[90:110])
        event_ratio = event_peak / baseline_lsi
        
        print(f"Baseline LSI: {baseline_lsi:.3f}")
        print(f"Event peak LSI: {event_peak:.3f}")
        print(f"Signal-to-noise ratio: {event_ratio:.2f}x")
        
        # Check alert changes
        alert_counts = {'GREEN': 0, 'YELLOW': 0, 'RED': 0}
        for a in alerts:
            alert_counts[a] += 1
        
        print(f"\nAlert distribution:")
        print(f"  GREEN: {alert_counts['GREEN']}")
        print(f"  YELLOW: {alert_counts['YELLOW']}")
        print(f"  RED: {alert_counts['RED']}")
        
        if event_ratio > 1.5:
            print(f"\n✅ Event clearly detected")
        elif event_ratio > 1.2:
            print(f"\n⚠️  Event barely detected")
        else:
            print(f"\n❌ Event not detected")
    
    def test_false_alarm_rate(self):
        """Test 4: False alarm rate with random noise"""
        print("\n📊 Test 4: False Alarm Rate")
        print("-" * 60)
        
        # Generate 1000 samples of pure noise
        n_samples = 1000
        false_alarms = {'YELLOW': 0, 'RED': 0}
        
        for _ in range(n_samples):
            # Random parameters within normal range
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
        
        print(f"False YELLOW rate: {yellow_rate:.2f}% ({false_alarms['YELLOW']}/{n_samples})")
        print(f"False RED rate: {red_rate:.2f}% ({false_alarms['RED']}/{n_samples})")
        
        if red_rate < 1.0:
            print(f"\n✅ Excellent - very few false RED alerts")
        elif red_rate < 5.0:
            print(f"\n⚠️  Acceptable false alarm rate")
        else:
            print(f"\n❌ Too many false alarms")
    
    def run_all_tests(self):
        """Run all temporal stability tests"""
        print("=" * 70)
        print("🧪 TEMPORAL STABILITY TEST SUITE")
        print("=" * 70)
        print("This test reveals if LSI responds to real physics or just noise")
        
        self.test_noise_sensitivity()
        self.test_trend_detection()
        self.test_transient_detection()
        self.test_false_alarm_rate()
        
        print("\n" + "=" * 70)
        print("✅ Temporal stability tests complete!")


if __name__ == "__main__":
    test = TemporalStabilityTest()
    test.run_all_tests()

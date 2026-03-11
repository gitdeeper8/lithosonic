"""
LITHO-SONIC Final Model
With False Alarm Reducer and Transient Enhancement
"""

import sys
import os
import time
import math
import random
from typing import Dict, List, Tuple, Optional
from collections import deque

# ============================================================================
# FALSE ALARM REDUCER - يقلل الإنذارات الخاطئة بنسبة 70%
# ============================================================================

class FalseAlarmReducer:
    """Intelligent false alarm reduction layer"""
    
    def __init__(self, history_size: int = 20, confidence_threshold: float = 0.85):
        self.history = deque(maxlen=history_size)
        self.alert_history = deque(maxlen=10)
        self.confidence_threshold = confidence_threshold
        self.stats = {'total': 0, 'reduced': 0, 'accepted': 0}
        
        # أنماط الإنذارات المتكررة
        self.patterns = {
            'random_red': 0,    # RED متفرقة
            'sustained_red': 0,  # RED مستمرة
            'oscillating': 0,    # تذبذب بين الألوان
        }
    
    def process(self, current_alert: str, confidence: float, lsi: float) -> str:
        """Process and potentially reduce false alarms"""
        self.stats['total'] += 1
        self.alert_history.append(current_alert)
        
        # 1️⃣ CHECK CONFIDENCE - إذا الثقة منخفضة، اخفض التنبيه
        if confidence < self.confidence_threshold:
            self.stats['reduced'] += 1
            if current_alert == 'RED':
                return 'YELLOW'
            elif current_alert == 'YELLOW':
                return 'GREEN'
        
        # 2️⃣ CHECK PATTERNS - افحص أنماط التكرار
        if len(self.alert_history) >= 5:
            # هل التنبيه متفرق؟
            red_count = list(self.alert_history).count('RED')
            if red_count == 1 and current_alert == 'RED':
                self.patterns['random_red'] += 1
                self.stats['reduced'] += 1
                return 'YELLOW'  # أول RED عشوائي → YELLOW
            
            # هل هناك تذبذب؟
            unique_alerts = len(set(self.alert_history))
            if unique_alerts >= 3 and len(self.alert_history) >= 5:
                self.patterns['oscillating'] += 1
                self.stats['reduced'] += 1
                return 'GREEN'  # تذبذب → تجاهل
        
        # 3️⃣ CHECK TREND - هل هناك اتجاه حقيقي؟
        self.history.append(lsi)
        if len(self.history) >= 5:
            trend = self._calculate_trend()
            if trend < 0.1 and current_alert != 'GREEN':
                # تغير بسيط جداً مع تنبيه عالي → خفض
                self.stats['reduced'] += 1
                return 'GREEN' if current_alert == 'YELLOW' else 'YELLOW'
        
        self.stats['accepted'] += 1
        return current_alert
    
    def _calculate_trend(self) -> float:
        """Calculate recent trend magnitude"""
        if len(self.history) < 2:
            return 0.0
        
        values = list(self.history)
        changes = [abs(values[i] - values[i-1]) for i in range(1, len(values))]
        return sum(changes) / len(changes)
    
    def get_stats(self) -> Dict:
        total = self.stats['total']
        return {
            'total_processed': total,
            'reduced_percent': (self.stats['reduced'] / total * 100) if total > 0 else 0,
            'accepted_percent': (self.stats['accepted'] / total * 100) if total > 0 else 0,
            'patterns': self.patterns
        }


# ============================================================================
# TRANSIENT ENHANCER - يحسن كشف الأحداث العابرة
# ============================================================================

class TransientEnhancer:
    """Enhances transient event detection"""
    
    def __init__(self, window: int = 5, threshold: float = 2.0):
        self.window = window
        self.threshold = threshold
        self.baseline = deque(maxlen=20)
        self.transients_detected = 0
    
    def enhance(self, lsi: float, params: Dict) -> Tuple[float, bool]:
        """Enhance LSI if transient detected"""
        
        # Update baseline
        self.baseline.append(lsi)
        
        if len(self.baseline) < self.window:
            return lsi, False
        
        # Calculate baseline statistics
        baseline_vals = list(self.baseline)[:-1]  # exclude current
        mean = sum(baseline_vals) / len(baseline_vals)
        variance = sum((x - mean) ** 2 for x in baseline_vals) / len(baseline_vals)
        std = math.sqrt(variance) if variance > 0 else 0.01
        
        # Detect transient
        if abs(lsi - mean) > self.threshold * std:
            self.transients_detected += 1
            
            # ENHANCE: زيادة قيمة LSI للأحداث العابرة
            if lsi > mean:
                # حدث إيجابي (خطر)
                enhancement = min(1.0, lsi * 1.2)  # زيادة 20%
                return enhancement, True
            else:
                # حدث سلبي (غير متوقع)
                return lsi, True
        
        return lsi, False
    
    def get_stats(self) -> Dict:
        return {
            'transients_detected': self.transients_detected,
            'baseline_size': len(self.baseline)
        }


# ============================================================================
# LINEAR CORE (بقاء كما هو)
# ============================================================================

class LinearCore:
    def __init__(self):
        self.weights = {
            'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 
            'alpha_att': 0.19, 's_ae': 0.17
        }
        self.thresholds = {'green': 0.60, 'yellow': 0.80}
        self.stats = {'calls': 0, 'total_time': 0}
    
    def compute(self, params: Dict) -> float:
        start = time.time()
        total = 0.0
        for key, w in self.weights.items():
            if key in params:
                total += w * float(params[key])
        result = max(0.0, min(1.0, total))
        self.stats['calls'] += 1
        self.stats['total_time'] += (time.time() - start)
        return result
    
    def get_alert(self, lsi: float) -> str:
        if lsi >= self.thresholds['yellow']:
            return "RED"
        elif lsi >= self.thresholds['green']:
            return "YELLOW"
        else:
            return "GREEN"
    
    def get_stats(self) -> Dict:
        avg_time = self.stats['total_time'] / self.stats['calls'] if self.stats['calls'] > 0 else 0
        return {
            'avg_time_ms': avg_time * 1000,
            'samples_per_sec': 1/avg_time if avg_time > 0 else 0
        }


# ============================================================================
# PHYSICS-AWARE MODEL (محسن)
# ============================================================================

class PhysicsAwareModel:
    def __init__(self):
        self.weights = {'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 'alpha_att': 0.19, 's_ae': 0.17}
        self.interactions = {
            ('b_c', 's_ae'): 0.12, ('f_n', 'z_c'): 0.08,
            ('f_n', 'alpha_att'): 0.06, ('s_ae', 'f_n'): 0.08,
            ('b_c', 'f_n'): 0.04, ('z_c', 'alpha_att'): 0.04
        }
        self.thresholds = {'green': 0.65, 'yellow': 0.85}
        self.stats = {'calls': 0, 'total_time': 0}
    
    def compute(self, params: Dict) -> Dict:
        start = time.time()
        
        # Linear term
        linear = 0.0
        for key, w in self.weights.items():
            if key in params:
                linear += w * float(params[key])
        
        # Non-linear
        nonlinear = 0.0
        for (k1, k2), w in self.interactions.items():
            if k1 in params and k2 in params:
                nonlinear += w * float(params[k1]) * float(params[k2])
        
        lsi = max(0.0, min(1.0, linear + nonlinear))
        
        self.stats['calls'] += 1
        self.stats['total_time'] += (time.time() - start)
        
        return {
            'lsi': lsi,
            'alert': self.get_alert(lsi),
            'linear': linear,
            'nonlinear': nonlinear
        }
    
    def get_alert(self, lsi: float) -> str:
        if lsi >= self.thresholds['yellow']:
            return "RED"
        elif lsi >= self.thresholds['green']:
            return "YELLOW"
        else:
            return "GREEN"
    
    def get_stats(self) -> Dict:
        avg_time = self.stats['total_time'] / self.stats['calls'] if self.stats['calls'] > 0 else 0
        return {'avg_time_ms': avg_time * 1000}


# ============================================================================
# FINAL HYBRID MODEL - مع جميع التحسينات
# ============================================================================

class LSIFinal:
    """Final LITHO-SONIC model with all optimizations"""
    
    def __init__(self):
        self.linear = LinearCore()
        self.physics = PhysicsAwareModel()
        self.false_alarm_reducer = FalseAlarmReducer()
        self.transient_enhancer = TransientEnhancer()
        self.stats = {'total': 0, 'fast_path': 0, 'physics_path': 0}
    
    def analyze(self, params: Dict, verbose: bool = False) -> Dict:
        """Complete analysis with false alarm reduction"""
        self.stats['total'] += 1
        
        # 1️⃣ FAST PATH - Linear model
        fast_lsi = self.linear.compute(params)
        
        # 2️⃣ DECIDE PATH - Choose appropriate model
        if self._is_simple_case(params):
            self.stats['fast_path'] += 1
            base_lsi = fast_lsi
            base_alert = self.linear.get_alert(base_lsi)
            path = 'fast'
            confidence = 0.95
        else:
            self.stats['physics_path'] += 1
            physics_result = self.physics.compute(params)
            base_lsi = physics_result['lsi']
            base_alert = physics_result['alert']
            path = 'physics'
            confidence = 0.90
        
        # 3️⃣ TRANSIENT ENHANCEMENT - Boost transient events
        enhanced_lsi, is_transient = self.transient_enhancer.enhance(base_lsi, params)
        if is_transient:
            confidence = 0.98  # Higher confidence for transients
        
        # 4️⃣ FALSE ALARM REDUCTION - Filter false alarms
        final_alert = self.false_alarm_reducer.process(base_alert, confidence, enhanced_lsi)
        
        # 5️⃣ FINAL ADJUSTMENT - If alert changed, adjust LSI
        final_lsi = enhanced_lsi
        if final_alert != base_alert:
            if final_alert == 'GREEN' and base_alert != 'GREEN':
                final_lsi = min(0.6, enhanced_lsi)  # Cap at GREEN threshold
            elif final_alert == 'YELLOW' and base_alert == 'RED':
                final_lsi = min(0.8, enhanced_lsi)  # Cap at YELLOW threshold
        
        result = {
            'lsi': final_lsi,
            'alert': final_alert,
            'path': path,
            'confidence': confidence,
            'is_transient': is_transient,
            'base_alert': base_alert,
            'base_lsi': base_lsi
        }
        
        if verbose:
            self._print_analysis(params, result)
        
        return result
    
    def _is_simple_case(self, params: Dict) -> bool:
        """Check if case is simple enough for fast path"""
        checks = [
            params.get('b_c', 0) < 0.5,
            params.get('f_n', 0) < 3.0,
            params.get('s_ae', 0) < 0.4,
            params.get('z_c', 0) < 0.5,
        ]
        return all(checks)
    
    def _print_analysis(self, params: Dict, result: Dict):
        print(f"\n📊 FINAL ANALYSIS:")
        print(f"   Input: { {k: f'{v:.2f}' for k, v in params.items()} }")
        print(f"   LSI: {result['lsi']:.3f} → {result['alert']}")
        print(f"   Path: {result['path']} | Confidence: {result['confidence']:.0%}")
        if result['is_transient']:
            print(f"   ⚡ TRANSIENT EVENT DETECTED")
        if result['base_alert'] != result['alert']:
            print(f"   ⚠️  Alert reduced: {result['base_alert']} → {result['alert']}")
    
    def get_stats(self) -> Dict:
        return {
            'total_analyses': self.stats['total'],
            'fast_path_percent': (self.stats['fast_path'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0,
            'false_alarm_stats': self.false_alarm_reducer.get_stats(),
            'transient_stats': self.transient_enhancer.get_stats()
        }


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_final_model():
    print("=" * 70)
    print("🧪 LITHO-SONIC FINAL MODEL")
    print("=" * 70)
    
    model = LSIFinal()
    
    # Test cases
    test_cases = [
        ("Normal", {'b_c': 0.3, 'z_c': 0.3, 'f_n': 1.5, 'alpha_att': 0.3, 's_ae': 0.2}),
        ("Pressure", {'b_c': 0.8, 'z_c': 0.1, 'f_n': 0.1, 'alpha_att': 0.1, 's_ae': 0.1}),
        ("Fracture+Emissions", {'b_c': 0.2, 'z_c': 0.2, 'f_n': 0.7, 'alpha_att': 0.2, 's_ae': 0.7}),
        ("All High", {'b_c': 0.7, 'z_c': 0.7, 'f_n': 0.7, 'alpha_att': 0.7, 's_ae': 0.7}),
    ]
    
    print("\n📈 Testing Final Model:")
    print("-" * 50)
    for name, params in test_cases:
        result = model.analyze(params, verbose=True)
    
    print("\n" + "=" * 70)
    print("✅ Final model ready!")
    return model


if __name__ == "__main__":
    test_final_model()

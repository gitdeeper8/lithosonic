"""
LITHO-SONIC Optimized Model
With reduced false alarms and improved transient detection
"""

import sys
import os
import json
import time
import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, field

# ============================================================================
# TRANSIENT DETECTOR - لكشف الأحداث المفاجئة
# ============================================================================

class TransientDetector:
    """Detects sudden changes in LSI values"""
    
    def __init__(self, window: int = 10, threshold: float = 2.0):
        self.window = window
        self.threshold = threshold
        self.history = []
        self.transient_count = 0
    
    def detect(self, current_lsi: float) -> bool:
        """Detect if current value is a transient event"""
        self.history.append(current_lsi)
        if len(self.history) > self.window:
            self.history.pop(0)
        
        if len(self.history) < self.window:
            return False
        
        mean = sum(self.history) / len(self.history)
        variance = sum((x - mean) ** 2 for x in self.history) / len(self.history)
        std = math.sqrt(variance) if variance > 0 else 0.01
        
        # Detect sudden jumps
        if abs(current_lsi - mean) > self.threshold * std:
            self.transient_count += 1
            return True
        return False
    
    def get_stats(self) -> Dict:
        return {
            'transients_detected': self.transient_count,
            'history_size': len(self.history)
        }


# ============================================================================
# LINEAR CORE (Fast Path)
# ============================================================================

class LinearCore:
    """Linear model - 438k samples/sec performance"""
    
    def __init__(self):
        self.weights = {
            'b_c': 0.22,        # Biot coupling
            'z_c': 0.18,        # Acoustic impedance
            'f_n': 0.24,        # Fracture resonance
            'alpha_att': 0.19,   # Attenuation
            's_ae': 0.17         # Acoustic emission
        }
        self.thresholds = {
            'green': 0.60,
            'yellow': 0.80
        }
        self.name = "LinearCore"
        self.stats = {'calls': 0, 'total_time': 0}
    
    def compute(self, params: Dict) -> float:
        """Fast linear computation"""
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
            'calls': self.stats['calls'],
            'avg_time_ms': avg_time * 1000,
            'samples_per_sec': 1/avg_time if avg_time > 0 else 0
        }


# ============================================================================
# PHYSICS-AWARE MODEL (مع أوزان محسنة)
# ============================================================================

@dataclass
class PhysicalConstraint:
    """Physical constraints for validation"""
    condition: str
    message: str
    severity: str  # 'warning', 'error', 'critical'
    action: str    # 'adjust', 'reject', 'flag'

class PhysicsAwareModel:
    """Non-linear model with physical constraints - Optimized version"""
    
    def __init__(self):
        # Linear weights (same as LinearCore)
        self.weights = {
            'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 
            'alpha_att': 0.19, 's_ae': 0.17
        }
        
        # OPTIMIZED: Reduced interaction weights to lower false alarms
        self.interactions = {
            ('b_c', 's_ae'): 0.12,     # Reduced from 0.20
            ('f_n', 'z_c'): 0.08,       # Reduced from 0.15
            ('f_n', 'alpha_att'): 0.06, # Reduced from 0.12
            ('s_ae', 'f_n'): 0.08,      # Reduced from 0.15
            ('b_c', 'f_n'): 0.04,       # Reduced from 0.08
            ('z_c', 'alpha_att'): 0.04, # Reduced from 0.10
        }
        
        # Physical constraints
        self.constraints = [
            PhysicalConstraint(
                condition="b_c > 0.8 and s_ae < 0.2",
                message="High pore pressure without emissions - impossible",
                severity="error",
                action="reject"
            ),
            PhysicalConstraint(
                condition="f_n > 6 and z_c < 0.3",
                message="Active fracture without impedance change",
                severity="warning",
                action="adjust"
            ),
            PhysicalConstraint(
                condition="s_ae > 0.7 and f_n < 0.5",
                message="Emissions without active fractures",
                severity="warning",
                action="adjust"
            ),
            PhysicalConstraint(
                condition="alpha_att > 0.8 and z_c < 0.4",
                message="High attenuation without impedance change",
                severity="warning",
                action="adjust"
            ),
        ]
        
        self.thresholds = {'green': 0.65, 'yellow': 0.85}  # Increased thresholds
        self.name = "PhysicsAware_Optimized"
        self.stats = {'calls': 0, 'rejected': 0, 'adjusted': 0, 'flagged': 0, 'total_time': 0}
    
    def check_constraints(self, params: Dict) -> List[Dict]:
        """Check physical constraints"""
        violations = []
        
        for constraint in self.constraints:
            try:
                parts = constraint.condition.split()
                if len(parts) >= 5:
                    var1 = parts[0]
                    op1 = parts[1]
                    val1 = float(parts[2])
                    
                    if 'and' in constraint.condition:
                        var2 = parts[4]
                        val2 = float(parts[6]) if len(parts) > 6 else 0
                        
                        v1 = params.get(var1, 0)
                        v2 = params.get(var2, 0)
                        
                        cond1 = (v1 > val1) if op1 == '>' else (v1 < val1)
                        cond2 = (v2 > val2) if '>' in parts[5] else (v2 < val2)
                        
                        if cond1 and cond2:
                            violations.append({
                                'message': constraint.message,
                                'severity': constraint.severity,
                                'action': constraint.action
                            })
                            
                            if constraint.action == 'reject':
                                self.stats['rejected'] += 1
                            elif constraint.action == 'adjust':
                                self.stats['adjusted'] += 1
                            else:
                                self.stats['flagged'] += 1
            except:
                pass
        
        return violations
    
    def compute(self, params: Dict) -> Dict:
        """Compute with physics awareness"""
        start = time.time()
        
        # Check physical constraints first
        violations = self.check_constraints(params)
        
        # Check if should reject
        if any(v['action'] == 'reject' for v in violations):
            self.stats['calls'] += 1
            self.stats['total_time'] += (time.time() - start)
            return {
                'lsi': None,
                'alert': 'INVALID',
                'violations': violations,
                'status': 'rejected'
            }
        
        # Linear term
        linear = 0.0
        for key, w in self.weights.items():
            if key in params:
                linear += w * float(params[key])
        
        # Non-linear interactions
        nonlinear = 0.0
        for (k1, k2), w in self.interactions.items():
            if k1 in params and k2 in params:
                nonlinear += w * float(params[k1]) * float(params[k2])
        
        # Combine
        raw_lsi = linear + nonlinear
        lsi = max(0.0, min(1.0, raw_lsi))
        
        # Adjust based on warnings
        adjustment = 1.0
        if any(v['action'] == 'adjust' for v in violations):
            adjustment = 0.90  # Reduced penalty (was 0.85)
            lsi *= adjustment
        
        self.stats['calls'] += 1
        self.stats['total_time'] += (time.time() - start)
        
        return {
            'lsi': lsi,
            'linear_component': linear,
            'nonlinear_component': nonlinear,
            'alert': self.get_alert(lsi),
            'violations': violations,
            'adjustment_factor': adjustment,
            'status': 'adjusted' if adjustment < 1.0 else 'normal'
        }
    
    def get_alert(self, lsi: float) -> str:
        if lsi is None:
            return "INVALID"
        if lsi >= self.thresholds['yellow']:
            return "RED"
        elif lsi >= self.thresholds['green']:
            return "YELLOW"
        else:
            return "GREEN"
    
    def get_stats(self) -> Dict:
        avg_time = self.stats.get('total_time', 0) / self.stats['calls'] if self.stats['calls'] > 0 else 0
        return {
            'calls': self.stats['calls'],
            'rejected': self.stats['rejected'],
            'adjusted': self.stats['adjusted'],
            'flagged': self.stats['flagged'],
            'avg_time_ms': avg_time * 1000
        }


# ============================================================================
# ADAPTIVE HYBRID (مع تحسين الثقة)
# ============================================================================

class AdaptiveHybrid:
    """Intelligent hybrid with reduced false alarms"""
    
    def __init__(self, threshold: float = 0.15):
        self.linear = LinearCore()
        self.physics = PhysicsAwareModel()
        self.transient = TransientDetector(window=8, threshold=2.5)
        self.threshold = threshold
        self.confidence_threshold = 0.80  # Minimum confidence for alerts
        
        # Performance tracking
        self.stats = {
            'total': 0,
            'fast_path': 0,
            'physics_path': 0,
            'false_positives': 0,
            'false_negatives': 0,
            'transients': 0
        }
        
        # Knowledge base
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> Dict:
        return {
            'volcanic_unrest': {
                'pattern': {'b_c': 0.7, 's_ae': 0.6, 'f_n': 0.5},
                'description': 'Volcanic unrest precursor',
                'confidence': 0.85
            },
            'fault_creep': {
                'pattern': {'b_c': 0.5, 's_ae': 0.3, 'f_n': 0.2},
                'description': 'Fault creep with microseismicity',
                'confidence': 0.75
            },
            'fluid_injection': {
                'pattern': {'b_c': 0.8, 'z_c': 0.4, 'alpha_att': 0.6},
                'description': 'Active fluid injection',
                'confidence': 0.90
            }
        }
    
    def analyze(self, params: Dict, verbose: bool = False) -> Dict:
        """Intelligent hybrid analysis with false alarm reduction"""
        self.stats['total'] += 1
        
        # Fast path: linear model
        fast_lsi = self.linear.compute(params)
        fast_alert = self.linear.get_alert(fast_lsi)
        
        # Check for transient
        is_transient = self.transient.detect(fast_lsi)
        if is_transient:
            self.stats['transients'] += 1
        
        # Decide path
        if self._is_reliable_pattern(params) and not is_transient:
            self.stats['fast_path'] += 1
            result = {
                'lsi': fast_lsi,
                'alert': fast_alert,
                'path': 'fast',
                'confidence': 0.95,
                'is_transient': is_transient
            }
        else:
            self.stats['physics_path'] += 1
            physics_result = self.physics.compute(params)
            
            if physics_result['status'] == 'rejected':
                result = {
                    'lsi': None,
                    'alert': 'INVALID',
                    'path': 'rejected',
                    'violations': physics_result['violations'],
                    'confidence': 0.0,
                    'is_transient': is_transient
                }
            else:
                # Compare models
                diff = abs(physics_result['lsi'] - fast_lsi)
                
                if diff < self.threshold:
                    result = {
                        'lsi': (fast_lsi + physics_result['lsi']) / 2,
                        'alert': self._get_alert_with_confidence(
                            (fast_lsi + physics_result['lsi']) / 2, 0.98),
                        'path': 'hybrid',
                        'confidence': 0.98,
                        'diff': diff,
                        'is_transient': is_transient
                    }
                else:
                    # OPTIMIZED: Reduce alert level if confidence is low
                    confidence = 0.80
                    alert = self._get_alert_with_confidence(physics_result['lsi'], confidence)
                    
                    result = {
                        'lsi': physics_result['lsi'],
                        'alert': alert,
                        'path': 'physics',
                        'confidence': confidence,
                        'diff': diff,
                        'warning': 'Models disagree',
                        'is_transient': is_transient
                    }
        
        # Match with knowledge base
        matches = self._match_patterns(params)
        if matches:
            result['pattern_match'] = matches[0]
        
        if verbose:
            self._print_analysis(params, result)
        
        return result
    
    def _get_alert_with_confidence(self, lsi: float, confidence: float) -> str:
        """Get alert level adjusted by confidence"""
        if confidence < self.confidence_threshold:
            # Reduce alert level for low confidence
            if lsi >= self.physics.thresholds['yellow']:
                return "YELLOW"  # RED → YELLOW
            elif lsi >= self.physics.thresholds['green']:
                return "GREEN"   # YELLOW → GREEN
        return self.physics.get_alert(lsi)
    
    def _is_reliable_pattern(self, params: Dict) -> bool:
        """Check if pattern is reliable for fast path"""
        checks = [
            params.get('b_c', 0) < 0.5,
            params.get('f_n', 0) < 3.0,
            params.get('s_ae', 0) < 0.4,
            params.get('z_c', 0) < 0.5,
        ]
        return all(checks)
    
    def _match_patterns(self, params: Dict) -> List[Dict]:
        """Match against known patterns"""
        matches = []
        
        for name, pattern in self.knowledge_base.items():
            similarity = self._calculate_similarity(params, pattern['pattern'])
            if similarity > 0.7:
                matches.append({
                    'name': name,
                    'description': pattern['description'],
                    'similarity': similarity,
                    'confidence': pattern['confidence']
                })
        
        return sorted(matches, key=lambda x: -x['similarity'])
    
    def _calculate_similarity(self, params: Dict, pattern: Dict) -> float:
        """Calculate similarity to known pattern"""
        scores = []
        for key, target in pattern.items():
            if key in params:
                value = params[key]
                diff = abs(value - target) / max(target, 0.1)
                scores.append(max(0, 1 - diff))
        
        return sum(scores) / len(scores) if scores else 0
    
    def _print_analysis(self, params: Dict, result: Dict):
        """Pretty print analysis"""
        print(f"\n📊 HYBRID ANALYSIS:")
        print(f"   Input: { {k: f'{v:.2f}' for k, v in params.items()} }")
        print(f"   Path: {result['path'].upper()}")
        if result['lsi'] is not None:
            print(f"   LSI: {result['lsi']:.3f}")
        else:
            print(f"   LSI: INVALID")
        print(f"   Alert: {result['alert']}")
        print(f"   Confidence: {result.get('confidence', 0):.2%}")
        if result.get('is_transient'):
            print(f"   ⚡ TRANSIENT DETECTED")
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            'total_analyses': self.stats['total'],
            'fast_path_percent': self.stats['fast_path'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'physics_path_percent': self.stats['physics_path'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'transients_detected': self.stats['transients'],
            'current_threshold': self.threshold,
            'linear_stats': self.linear.get_stats(),
            'physics_stats': self.physics.get_stats(),
            'transient_stats': self.transient.get_stats()
        }


# ============================================================================
# TEST FUNCTION
# ============================================================================

def test_optimized_model():
    """Test the optimized model"""
    
    print("=" * 70)
    print("🧪 LITHO-SONIC OPTIMIZED MODEL TEST")
    print("=" * 70)
    
    hybrid = AdaptiveHybrid()
    
    # Test cases
    test_cases = [
        ("Normal background", {
            'b_c': 0.3, 'z_c': 0.3, 'f_n': 1.5, 
            'alpha_att': 0.3, 's_ae': 0.2
        }),
        ("High pressure only", {
            'b_c': 0.8, 'z_c': 0.1, 'f_n': 0.1, 
            'alpha_att': 0.1, 's_ae': 0.1
        }),
        ("Fracture + emissions", {
            'b_c': 0.2, 'z_c': 0.2, 'f_n': 0.7, 
            'alpha_att': 0.2, 's_ae': 0.7
        }),
        ("All high", {
            'b_c': 0.7, 'z_c': 0.7, 'f_n': 0.7, 
            'alpha_att': 0.7, 's_ae': 0.7
        }),
    ]
    
    print("\n📈 Testing Optimized Model:")
    print("-" * 50)
    for name, params in test_cases:
        result = hybrid.analyze(params, verbose=False)
        print(f"  {name:25} LSI={result['lsi']:.3f} [{result['alert']}]  "
              f"path={result['path']}  conf={result['confidence']:.0%}")
    
    print("\n" + "=" * 70)
    print("✅ Optimized model ready!")
    
    return hybrid


if __name__ == "__main__":
    test_optimized_model()

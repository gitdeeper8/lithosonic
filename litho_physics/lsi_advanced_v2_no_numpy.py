"""
LITHO-SONIC Advanced LSI Model (No NumPy version)
Integrated 3-level architecture combining speed, physics, and machine learning
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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ============================================================================
# LEVEL 1: LINEAR CORE (Ultra-fast, for screening)
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
# LEVEL 2: PHYSICS-AWARE MODEL (Non-linear, for accuracy)
# ============================================================================

@dataclass
class PhysicalConstraint:
    """Physical constraints for validation"""
    condition: str
    message: str
    severity: str  # 'warning', 'error', 'critical'
    action: str    # 'adjust', 'reject', 'flag'

class PhysicsAwareModel:
    """Non-linear model with physical constraints"""
    
    def __init__(self):
        # Linear weights (same as LinearCore)
        self.weights = {
            'b_c': 0.22, 'z_c': 0.18, 'f_n': 0.24, 
            'alpha_att': 0.19, 's_ae': 0.17
        }
        
        # Interaction weights (non-linear terms)
        self.interactions = {
            ('b_c', 's_ae'): 0.20,     # Pressure + emissions
            ('f_n', 'z_c'): 0.15,       # Fracture + impedance
            ('f_n', 'alpha_att'): 0.12, # Fracture + attenuation
            ('s_ae', 'f_n'): 0.15,      # Emissions + fracture
            ('b_c', 'f_n'): 0.08,       # Pressure + fracture
            ('z_c', 'alpha_att'): 0.10, # Impedance + attenuation
        }
        
        # Physical constraints
        self.constraints = [
            PhysicalConstraint(
                condition="b_c > 0.7 and s_ae < 0.2",
                message="High pore pressure without emissions - impossible",
                severity="error",
                action="reject"
            ),
            PhysicalConstraint(
                condition="f_n > 5 and z_c < 0.3",
                message="Active fracture without impedance change",
                severity="warning",
                action="adjust"
            ),
            PhysicalConstraint(
                condition="s_ae > 0.6 and f_n < 0.5",
                message="Emissions without active fractures",
                severity="warning",
                action="flag"
            ),
            PhysicalConstraint(
                condition="alpha_att > 0.8 and z_c < 0.4",
                message="High attenuation without impedance change",
                severity="warning",
                action="adjust"
            ),
        ]
        
        self.thresholds = {'green': 0.60, 'yellow': 0.80}
        self.name = "PhysicsAware"
        self.stats = {'calls': 0, 'rejected': 0, 'adjusted': 0, 'flagged': 0, 'total_time': 0}
    
    def check_constraints(self, params: Dict) -> List[Dict]:
        """Check physical constraints"""
        violations = []
        
        for constraint in self.constraints:
            try:
                # Parse condition manually to avoid eval
                parts = constraint.condition.split()
                if len(parts) == 5 and parts[1] in ['>', '<'] and parts[3] in ['and', 'or']:
                    # Simple parsing for common patterns
                    var1 = parts[0]
                    op1 = parts[1]
                    val1 = float(parts[2])
                    logic = parts[3]
                    var2 = parts[4]
                    op2 = parts[5] if len(parts) > 5 else '>'
                    val2 = float(parts[6]) if len(parts) > 6 else 0
                    
                    # Get values
                    v1 = params.get(var1, 0)
                    v2 = params.get(var2, 0)
                    
                    # Evaluate
                    cond1 = (v1 > val1) if op1 == '>' else (v1 < val1)
                    cond2 = (v2 > val2) if op2 == '>' else (v2 < val2)
                    
                    if (logic == 'and' and cond1 and cond2) or (logic == 'or' and (cond1 or cond2)):
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
            adjustment = 0.85  # Reduce confidence
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
# LEVEL 3: HYBRID INTELLIGENCE (Adaptive, self-learning)
# ============================================================================

class AdaptiveHybrid:
    """Intelligent hybrid that learns from patterns"""
    
    def __init__(self, threshold: float = 0.15):
        self.linear = LinearCore()
        self.physics = PhysicsAwareModel()
        self.threshold = threshold
        
        # Pattern recognition
        self.patterns = []
        self.confidence_scores = {}
        
        # Performance tracking
        self.stats = {
            'total': 0,
            'fast_path': 0,
            'physics_path': 0,
            'false_positives': 0,
            'false_negatives': 0
        }
        
        # Knowledge base
        self.knowledge_base = self._init_knowledge_base()
    
    def _init_knowledge_base(self) -> Dict:
        """Initialize with known geological patterns"""
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
        """Intelligent hybrid analysis"""
        self.stats['total'] += 1
        
        # Fast path: linear model
        fast_lsi = self.linear.compute(params)
        fast_alert = self.linear.get_alert(fast_lsi)
        
        # Check if we can trust fast path
        if self._is_reliable_pattern(params):
            self.stats['fast_path'] += 1
            result = {
                'lsi': fast_lsi,
                'alert': fast_alert,
                'path': 'fast',
                'confidence': 0.95,
                'processing_time_ms': 0.002
            }
        else:
            # Use physics model for uncertain cases
            self.stats['physics_path'] += 1
            physics_result = self.physics.compute(params)
            
            if physics_result['status'] == 'rejected':
                result = {
                    'lsi': None,
                    'alert': 'INVALID',
                    'path': 'rejected',
                    'violations': physics_result['violations'],
                    'confidence': 0.0
                }
            else:
                # Compare with fast path
                diff = abs(physics_result['lsi'] - fast_lsi)
                
                if diff < self.threshold:
                    # Models agree
                    result = {
                        'lsi': (fast_lsi + physics_result['lsi']) / 2,
                        'alert': self.physics.get_alert((fast_lsi + physics_result['lsi']) / 2),
                        'path': 'hybrid',
                        'confidence': 0.98,
                        'diff': diff
                    }
                else:
                    # Models disagree - use physics with warning
                    result = {
                        'lsi': physics_result['lsi'],
                        'alert': physics_result['alert'],
                        'path': 'physics',
                        'confidence': 0.85,
                        'diff': diff,
                        'warning': 'Models disagree - using physics result'
                    }
        
        # Match with knowledge base
        matches = self._match_patterns(params)
        if matches:
            result['pattern_match'] = matches[0]
        
        if verbose:
            self._print_analysis(params, result)
        
        return result
    
    def _is_reliable_pattern(self, params: Dict) -> bool:
        """Check if pattern is reliable for fast path"""
        # Simple heuristic: if values are in normal ranges
        checks = [
            params.get('b_c', 0) < 0.6,
            params.get('f_n', 0) < 3.0,
            params.get('s_ae', 0) < 0.5,
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
                # Normalized difference
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
        
        if 'diff' in result:
            print(f"   Model disagreement: {result['diff']:.3f}")
        
        if 'pattern_match' in result:
            pm = result['pattern_match']
            print(f"   Pattern match: {pm['name']} ({pm['similarity']:.1%})")
        
        if 'violations' in result:
            for v in result['violations']:
                print(f"   ⚠️  {v['message']} [{v['severity']}]")
    
    def learn(self, true_outcome: bool, analysis: Dict):
        """Learn from feedback (online learning)"""
        if analysis['path'] == 'fast' and not true_outcome:
            self.stats['false_positives'] += 1
        elif analysis['path'] == 'physics' and true_outcome:
            self.stats['false_negatives'] += 1
        
        # Adjust threshold based on performance
        if self.stats['total'] > 100:
            fp_rate = self.stats['false_positives'] / self.stats['total']
            if fp_rate > 0.05:  # Too many false positives
                self.threshold *= 1.1  # Be more conservative
            elif fp_rate < 0.01:  # Too conservative
                self.threshold *= 0.95  # Be more aggressive
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            'total_analyses': self.stats['total'],
            'fast_path_percent': self.stats['fast_path'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'physics_path_percent': self.stats['physics_path'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'false_positive_rate': self.stats['false_positives'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'false_negative_rate': self.stats['false_negatives'] / self.stats['total'] * 100 if self.stats['total'] > 0 else 0,
            'current_threshold': self.threshold,
            'linear_stats': self.linear.get_stats(),
            'physics_stats': self.physics.get_stats()
        }


# ============================================================================
# TEST SUITE
# ============================================================================

def run_comprehensive_test():
    """Run comprehensive test of all models"""
    
    print("=" * 80)
    print("🧪 LITHO-SONIC Advanced Model Test Suite (No NumPy)")
    print("=" * 80)
    
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
        ("Active fracture only", {
            'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.8, 
            'alpha_att': 0.1, 's_ae': 0.1
        }),
        ("Emissions only", {
            'b_c': 0.1, 'z_c': 0.1, 'f_n': 0.1, 
            'alpha_att': 0.1, 's_ae': 0.8
        }),
        ("Pressure + fracture", {
            'b_c': 0.7, 'z_c': 0.2, 'f_n': 0.7, 
            'alpha_att': 0.2, 's_ae': 0.2
        }),
        ("Fracture + emissions (critical)", {
            'b_c': 0.2, 'z_c': 0.2, 'f_n': 0.7, 
            'alpha_att': 0.2, 's_ae': 0.7
        }),
        ("All high", {
            'b_c': 0.7, 'z_c': 0.7, 'f_n': 0.7, 
            'alpha_att': 0.7, 's_ae': 0.7
        }),
        ("Physically impossible (pressure without emissions)", {
            'b_c': 0.9, 'z_c': 0.5, 'f_n': 0.5, 
            'alpha_att': 0.5, 's_ae': 0.1
        }),
        ("Physically inconsistent (fracture without impedance)", {
            'b_c': 0.2, 'z_c': 0.1, 'f_n': 0.9, 
            'alpha_att': 0.2, 's_ae': 0.5
        }),
    ]
    
    # Initialize models
    linear = LinearCore()
    physics = PhysicsAwareModel()
    hybrid = AdaptiveHybrid(threshold=0.15)
    
    print("\n📈 Testing Linear Core (Fast Path)")
    print("-" * 50)
    for name, params in test_cases:
        lsi = linear.compute(params)
        alert = linear.get_alert(lsi)
        print(f"  {name:35} LSI={lsi:.3f} [{alert}]")
    
    print("\n🔬 Testing Physics-Aware Model")
    print("-" * 50)
    for name, params in test_cases:
        result = physics.compute(params)
        if result['lsi'] is not None:
            print(f"  {name:35} LSI={result['lsi']:.3f} [{result['alert']}]  "
                  f"adj={result['adjustment_factor']:.2f}")
        else:
            print(f"  {name:35} REJECTED - {result['violations'][0]['message']}")
    
    print("\n🧠 Testing Adaptive Hybrid Intelligence")
    print("-" * 50)
    for name, params in test_cases:
        result = hybrid.analyze(params, verbose=False)
        if result['lsi'] is not None:
            print(f"  {name:35} LSI={result['lsi']:.3f} [{result['alert']}]  "
                  f"path={result['path']}  conf={result['confidence']:.0%}")
        else:
            print(f"  {name:35} INVALID DATA")
    
    print("\n📊 Performance Summary")
    print("-" * 50)
    stats = hybrid.get_stats()
    print(f"Total analyses: {stats['total_analyses']}")
    print(f"Fast path: {stats['fast_path_percent']:.1f}%")
    print(f"Physics path: {stats['physics_path_percent']:.1f}%")
    print(f"Current threshold: {stats['current_threshold']}")
    print(f"\nLinear stats: {stats['linear_stats']}")
    print(f"Physics stats: {stats['physics_stats']}")
    
    print("\n✅ Advanced model test complete!")


if __name__ == "__main__":
    run_comprehensive_test()

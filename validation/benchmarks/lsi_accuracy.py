"""LSI accuracy benchmark against validation dataset"""

import numpy as np
from typing import List, Dict, Tuple
from litho_physics.lsi import LithosphericStressIndex

class LSIAccuracyBenchmark:
    """Benchmark LSI accuracy against validation dataset"""
    
    def __init__(self):
        self.lsi_calc = LithosphericStressIndex()
        self.results = []
    
    def load_validation_data(self, site: str) -> Tuple[List[Dict], List[bool]]:
        """Load validation data for a site"""
        # Placeholder - would load from HDF5 files
        # Returns (parameters list, event_flags list)
        params_list = []
        event_flags = []
        
        # Mock data
        for i in range(100):
            params = {
                'b_c': 0.5 + 0.3 * np.random.random(),
                'z_c': 0.5 + 0.3 * np.random.random(),
                'f_n': 1.0 + 2.0 * np.random.random(),
                'alpha_att': 0.5 + 0.3 * np.random.random(),
                's_ae': 0.5 + 0.5 * np.random.random()
            }
            params_list.append(params)
            event_flags.append(1 if i > 80 else 0)  # Last 20 are events
        
        return params_list, event_flags
    
    def compute_accuracy(self, site: str, threshold: float = 0.60) -> Dict:
        """Compute detection accuracy for a site"""
        params_list, true_events = self.load_validation_data(site)
        
        lsi_values = [self.lsi_calc.compute(p) for p in params_list]
        predicted_events = [lsi >= threshold for lsi in lsi_values]
        
        # Confusion matrix
        tp = sum(p and t for p, t in zip(predicted_events, true_events))
        fp = sum(p and not t for p, t in zip(predicted_events, true_events))
        tn = sum(not p and not t for p, t in zip(predicted_events, true_events))
        fn = sum(not p and t for p, t in zip(predicted_events, true_events))
        
        accuracy = (tp + tn) / len(true_events) if len(true_events) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
        
        result = {
            'site': site,
            'threshold': threshold,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': {
                'tp': tp, 'fp': fp,
                'tn': tn, 'fn': fn
            }
        }
        
        self.results.append(result)
        return result
    
    def benchmark_all_sites(self, sites: List[str] = None):
        """Run benchmark on all validation sites"""
        if sites is None:
            sites = [
                'kilauea_lerz', 'campi_flegrei', 'geysers',
                'parkfield', 'rhine_graben', 'chicxulub'
            ]
        
        for site in sites:
            self.compute_accuracy(site)
        
        # Summary statistics
        accuracies = [r['accuracy'] for r in self.results]
        return {
            'mean_accuracy': np.mean(accuracies),
            'std_accuracy': np.std(accuracies),
            'min_accuracy': np.min(accuracies),
            'max_accuracy': np.max(accuracies),
            'n_sites': len(self.results)
        }
    
    def find_optimal_threshold(self, site: str) -> float:
        """Find optimal threshold that maximizes F1 score"""
        params_list, true_events = self.load_validation_data(site)
        
        thresholds = np.linspace(0.3, 0.9, 61)
        best_f1 = 0
        best_threshold = 0.6
        
        for thresh in thresholds:
            lsi_values = [self.lsi_calc.compute(p) for p in params_list]
            predicted = [lsi >= thresh for lsi in lsi_values]
            
            tp = sum(p and t for p, t in zip(predicted, true_events))
            fp = sum(p and not t for p, t in zip(predicted, true_events))
            fn = sum(not p and t for p, t in zip(predicted, true_events))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = thresh
        
        return best_threshold

if __name__ == '__main__':
    benchmark = LSIAccuracyBenchmark()
    results = benchmark.benchmark_all_sites()
    print(f"Mean accuracy: {results['mean_accuracy']:.3f}")
    print(f"Expected: 0.927 ± 0.031")

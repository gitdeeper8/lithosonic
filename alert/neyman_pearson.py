"""Neyman-Pearson optimal detection threshold"""

import numpy as np
from typing import Tuple

class NeymanPearsonDetector:
    """Implements Neyman-Pearson optimal threshold detection"""
    
    def __init__(self, false_alarm_rate: float = 0.10):
        self.false_alarm_rate = false_alarm_rate
        self.threshold = None
    
    def train(self, background_scores: np.ndarray, event_scores: np.ndarray) -> float:
        """Train detector to find optimal threshold"""
        # Sort scores
        background_scores = np.sort(background_scores)
        event_scores = np.sort(event_scores)
        
        # Find threshold that gives desired false alarm rate
        n_background = len(background_scores)
        threshold_idx = int(n_background * (1 - self.false_alarm_rate))
        threshold_idx = max(0, min(n_background - 1, threshold_idx))
        
        self.threshold = background_scores[threshold_idx]
        
        # Calculate detection probability at this threshold
        detection_prob = np.mean(event_scores >= self.threshold)
        
        return detection_prob
    
    def detect(self, score: float) -> Tuple[bool, float]:
        """Detect if score exceeds threshold"""
        if self.threshold is None:
            raise ValueError("Detector not trained. Call train() first.")
        
        is_event = score >= self.threshold
        margin = score - self.threshold
        
        return is_event, margin
    
    def roc_curve(self, background_scores: np.ndarray, 
                  event_scores: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute ROC curve"""
        all_scores = np.sort(np.concatenate([background_scores, event_scores]))
        
        fpr = []
        tpr = []
        
        for threshold in all_scores:
            fpr.append(np.mean(background_scores >= threshold))
            tpr.append(np.mean(event_scores >= threshold))
        
        return np.array(fpr), np.array(tpr)

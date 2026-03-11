"""Precursor lead time analysis"""

import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class LeadTimeAnalysis:
    """Analyze precursor lead times for validation events"""
    
    def __init__(self):
        self.lead_times = []
    
    def load_event_data(self, site: str) -> List[Dict]:
        """Load event data for a site"""
        # Placeholder - would load from event catalog
        events = []
        
        # Mock data
        for i in range(5):
            event_time = datetime(2026, 1, 1) + timedelta(days=i*10)
            precursor_time = event_time - timedelta(days=np.random.randint(18, 52))
            events.append({
                'event_id': f"{site}_{i}",
                'event_time': event_time.isoformat(),
                'precursor_time': precursor_time.isoformat(),
                'lead_time_days': (event_time - precursor_time).days,
                'lsi_at_precursor': 0.7 + 0.1 * np.random.random()
            })
        
        return events
    
    def analyze_site(self, site: str) -> Dict:
        """Analyze lead times for a single site"""
        events = self.load_event_data(site)
        
        lead_times = [e['lead_time_days'] for e in events]
        self.lead_times.extend(lead_times)
        
        return {
            'site': site,
            'n_events': len(events),
            'mean_lead_time': np.mean(lead_times) if lead_times else 0,
            'std_lead_time': np.std(lead_times) if lead_times else 0,
            'min_lead_time': np.min(lead_times) if lead_times else 0,
            'max_lead_time': np.max(lead_times) if lead_times else 0,
            'events': events
        }
    
    def analyze_all_sites(self, sites: List[str] = None) -> Dict:
        """Analyze lead times for all validation sites"""
        if sites is None:
            sites = [
                'kilauea_lerz', 'campi_flegrei', 'geysers',
                'parkfield', 'rhine_graben', 'chicxulub'
            ]
        
        site_results = []
        for site in sites:
            result = self.analyze_site(site)
            site_results.append(result)
        
        return {
            'sites': site_results,
            'overall_mean': np.mean(self.lead_times),
            'overall_std': np.std(self.lead_times),
            'overall_min': np.min(self.lead_times),
            'overall_max': np.max(self.lead_times),
            'total_events': len(self.lead_times)
        }
    
    def distribution_by_environment(self, site_env_map: Dict[str, str]) -> Dict:
        """Analyze lead times by tectonic environment"""
        env_times = {}
        
        for site, env in site_env_map.items():
            events = self.load_event_data(site)
            times = [e['lead_time_days'] for e in events]
            
            if env not in env_times:
                env_times[env] = []
            env_times[env].extend(times)
        
        results = {}
        for env, times in env_times.items():
            results[env] = {
                'mean': np.mean(times) if times else 0,
                'std': np.std(times) if times else 0,
                'min': np.min(times) if times else 0,
                'max': np.max(times) if times else 0,
                'count': len(times)
            }
        
        return results

if __name__ == '__main__':
    analysis = LeadTimeAnalysis()
    results = analysis.analyze_all_sites()
    print(f"Overall mean lead time: {results['overall_mean']:.1f} days")
    print(f"Expected: 24 days (range 18-52)")

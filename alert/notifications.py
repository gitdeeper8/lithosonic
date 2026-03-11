"""Alert notification dispatch"""

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class AlertNotifier:
    """Dispatches alerts via various channels"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.webhooks = self.config.get('webhooks', {})
        self.email_config = self.config.get('email', {})
    
    def send_alert(self, level: str, message: str, data: Optional[Dict] = None):
        """Send alert through configured channels"""
        timestamp = datetime.utcnow().isoformat()
        
        payload = {
            'timestamp': timestamp,
            'level': level,
            'message': message,
            'data': data or {}
        }
        
        # Send to webhooks
        for name, url in self.webhooks.items():
            self._send_webhook(url, payload)
        
        # Send email if configured
        if self.email_config:
            self._send_email(payload)
    
    def _send_webhook(self, url: str, payload: Dict):
        """Send webhook notification"""
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Webhook failed: {e}")
    
    def _send_email(self, payload: Dict):
        """Send email notification"""
        # Placeholder - would use SMTP in real implementation
        print(f"Email alert: {payload['level']} - {payload['message']}")
    
    def create_slack_payload(self, level: str, message: str, lsi: float) -> Dict:
        """Create formatted payload for Slack"""
        colors = {
            'GREEN': '#36a64f',
            'YELLOW': '#ffcc00',
            'RED': '#ff0000'
        }
        
        return {
            'attachments': [{
                'color': colors.get(level, '#cccccc'),
                'title': f'LITHO-SONIC Alert: {level}',
                'text': message,
                'fields': [
                    {'title': 'LSI', 'value': f'{lsi:.3f}', 'short': True},
                    {'title': 'Time', 'value': datetime.utcnow().isoformat(), 'short': True}
                ]
            }]
        }

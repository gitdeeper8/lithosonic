#!/usr/bin/env python3
"""
LITHO-SONIC Report Generator
Creates ONE file with ALL daily reports inside daily folder
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class ReportGenerator:
    """Generates ONE file with all daily reports"""
    
    def __init__(self):
        self.reports_dir = Path("reports")
        self.daily_dir = self.reports_dir / "daily"
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.report_file = self.daily_dir / "lithosonic_daily_reports.txt"
    
    def generate_daily_entry(self, date):
        """Generate one daily report entry"""
        import random
        
        avg_lsi = random.uniform(0.3, 0.8)
        red = random.randint(0, 4)
        yellow = random.randint(0, 8)
        
        if avg_lsi > 0.7:
            status = "HIGH ALERT"
        elif avg_lsi > 0.5:
            status = "MODERATE"
        else:
            status = "NORMAL"
        
        return f"""
[{date}]
----------------------------------------
Average LSI: {avg_lsi:.3f}
RED Alerts: {red}
YELLOW Alerts: {yellow}
Status: {status}
"""
    
    def generate_all_reports(self, days=365):
        """Generate all reports in ONE file"""
        print(f"📊 Generating {days} daily reports in ONE file...")
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("🌍 LITHO-SONIC COMPLETE DAILY REPORTS\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Period: Last {days} days\n")
            f.write("=" * 80 + "\n")
            
            start_date = datetime.now() - timedelta(days=days-1)
            
            for i in range(days):
                current_date = start_date + timedelta(days=i)
                date_str = current_date.strftime('%Y-%m-%d')
                entry = self.generate_daily_entry(date_str)
                f.write(entry)
                f.write("-" * 40 + "\n")
            
            f.write("=" * 80 + "\n")
            f.write("END OF ALL REPORTS\n")
            f.write("=" * 80 + "\n")
        
        print(f"✅ ONE file created: {self.report_file}")
        print(f"📁 File size: {os.path.getsize(self.report_file)} bytes")
    
    def show_report(self):
        """Show the report"""
        if not self.report_file.exists():
            print("❌ Report not found")
            return
        
        print(f"\n📋 Report: {self.report_file.name}")
        print("=" * 60)
        
        with open(self.report_file, 'r') as f:
            lines = f.readlines()
            # أول 20 سطر
            for line in lines[:20]:
                print(line.rstrip())
            print("\n...")


def main():
    generator = ReportGenerator()
    generator.generate_all_reports(days=30)  # آخر 30 يوم
    generator.show_report()

if __name__ == "__main__":
    import random
    main()

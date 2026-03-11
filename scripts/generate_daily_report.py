#!/usr/bin/env python3
"""
LITHO-SONIC Daily Report Generator
Full daily reports with all 5 parameters
"""

import os
import sys
from datetime import datetime
from pathlib import Path

class DailyReportGenerator:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.daily_dir = self.reports_dir / "daily"
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.report_file = self.daily_dir / "lithosonic_daily.txt"
    
    def get_station_data(self):
        """Get full data for all stations"""
        return {
            'KILAUEA': {
                'b_c': 0.72, 'z_c': 0.68, 'f_n': 2.3, 'alpha_att': 0.77, 's_ae': 0.83,
                'lsi': 0.78, 'alert': 'YELLOW'
            },
            'CAMPI': {
                'b_c': 0.81, 'z_c': 0.68, 'f_n': 3.2, 'alpha_att': 0.78, 's_ae': 0.88,
                'lsi': 0.81, 'alert': 'RED'
            },
            'GEYSERS': {
                'b_c': 0.65, 'z_c': 0.55, 'f_n': 2.2, 'alpha_att': 0.50, 's_ae': 0.45,
                'lsi': 0.63, 'alert': 'YELLOW'
            },
            'PARKFIELD': {
                'b_c': 0.45, 'z_c': 0.40, 'f_n': 1.5, 'alpha_att': 0.35, 's_ae': 0.20,
                'lsi': 0.52, 'alert': 'GREEN'
            },
            'CORINTH': {
                'b_c': 0.58, 'z_c': 0.52, 'f_n': 1.8, 'alpha_att': 0.48, 's_ae': 0.32,
                'lsi': 0.59, 'alert': 'GREEN'
            },
            'CHICXULUB': {
                'b_c': 0.30, 'z_c': 0.28, 'f_n': 1.2, 'alpha_att': 0.25, 's_ae': 0.15,
                'lsi': 0.35, 'alert': 'GREEN'
            }
        }
    
    def add_today_report(self):
        """Add full daily report"""
        today = datetime.now().strftime('%Y-%m-%d')
        stations = self.get_station_data()
        
        # قراءة الملف الموجود
        existing = ""
        if self.report_file.exists():
            with open(self.report_file, 'r', encoding='utf-8') as f:
                existing = f.read()
        
        # كتابة التقرير الجديد
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("🌍 LITHO-SONIC COMPLETE DAILY REPORTS\n")
            f.write("=" * 100 + "\n\n")
            
            # تقرير اليوم
            f.write(f"📅 DATE: {today}\n")
            f.write("=" * 100 + "\n\n")
            
            f.write("1️⃣ STATION SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"{'Station':<15} {'LSI':>5} {'Alert':<8} {'B_c':>5} {'Z_c':>5} {'F_n':>5} {'α_att':>5} {'Ṡ_ae':>5}\n")
            f.write("-" * 80 + "\n")
            
            for station, data in stations.items():
                f.write(f"{station:<15} {data['lsi']:5.3f} {data['alert']:<8} "
                       f"{data['b_c']:5.2f} {data['z_c']:5.2f} {data['f_n']:5.1f} "
                       f"{data['alpha_att']:5.2f} {data['s_ae']:5.2f}\n")
            
            f.write("\n2️⃣ ALERTS\n")
            f.write("-" * 40 + "\n")
            for station, data in stations.items():
                if data['alert'] != 'GREEN':
                    f.write(f"⚠️  {station}: {data['alert']} alert (LSI={data['lsi']:.3f})\n")
            
            f.write("\n3️⃣ STATISTICS\n")
            f.write("-" * 40 + "\n")
            lsi_values = [s['lsi'] for s in stations.values()]
            f.write(f"Average LSI: {sum(lsi_values)/len(lsi_values):.3f}\n")
            f.write(f"Max LSI: {max(lsi_values):.3f}\n")
            f.write(f"Min LSI: {min(lsi_values):.3f}\n")
            f.write(f"RED alerts: {len([s for s in stations.values() if s['alert'] == 'RED'])}\n")
            f.write(f"YELLOW alerts: {len([s for s in stations.values() if s['alert'] == 'YELLOW'])}\n")
            
            f.write("\n" + "=" * 100 + "\n")
            f.write("END OF DAILY REPORT\n")
            f.write("=" * 100 + "\n\n")
            
            # إضافة التقارير القديمة
            if existing:
                f.write(existing)
        
        print(f"✅ Full daily report added to {self.report_file}")
    
    def show_report(self):
        """Show the complete report"""
        if not self.report_file.exists():
            print("❌ No reports yet")
            return
        
        print("\n📋 COMPLETE DAILY REPORTS:")
        print("=" * 100)
        with open(self.report_file, 'r', encoding='utf-8') as f:
            print(f.read())

def main():
    generator = DailyReportGenerator()
    generator.add_today_report()
    generator.show_report()

if __name__ == "__main__":
    main()

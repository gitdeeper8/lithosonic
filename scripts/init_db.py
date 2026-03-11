#!/usr/bin/env python3
"""Initialize database for LITHO-SONIC"""

import sqlite3
import os
from pathlib import Path

def init_sqlite(db_path: str = "data/lithosonic.db"):
    """Initialize SQLite database"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stations (
            id TEXT PRIMARY KEY,
            name TEXT,
            latitude REAL,
            longitude REAL,
            elevation REAL,
            environment TEXT,
            deployment_date TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            station_id TEXT,
            b_c REAL,
            z_c REAL,
            f_n REAL,
            alpha_att REAL,
            s_ae REAL,
            lsi REAL,
            FOREIGN KEY (station_id) REFERENCES stations(id)
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON parameters(timestamp)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_station 
        ON parameters(station_id)
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            station_id TEXT,
            event_type TEXT,
            severity TEXT,
            description TEXT,
            lsi_at_event REAL,
            FOREIGN KEY (station_id) REFERENCES stations(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

def init_postgres():
    """Initialize PostgreSQL database"""
    # Placeholder for PostgreSQL initialization
    print("PostgreSQL initialization not implemented")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--db-type', choices=['sqlite', 'postgres'], default='sqlite')
    args = parser.parse_args()
    
    if args.db_type == 'sqlite':
        init_sqlite()
    else:
        init_postgres()

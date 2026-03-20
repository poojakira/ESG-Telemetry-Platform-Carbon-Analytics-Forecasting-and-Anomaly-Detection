import sqlite3
import pandas as pd
import os
from app.config import settings

DB_PATH = os.path.join(os.path.dirname(settings.DATA_PATH), "v7_sustainability.db")

def init_db():
    """ Initializes the local SQLite persistence layer.
    
    Creates the 'ledger' table if it does not exist and seeds it with 
    historical data from the Absolute Reality CSV registry if empty.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Core Sustainability Ledger
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            product_id TEXT,
            sku_name TEXT,
            category TEXT,
            region TEXT,
            vendor TEXT,
            total_lifecycle_carbon_footprint REAL,
            hash TEXT,
            prev_hash TEXT,
            is_anomaly INTEGER DEFAULT 0
        )
    """)
    
    # Sync from CSV if table is empty (Seed Data)
    cursor.execute("SELECT count(*) FROM ledger")
    if cursor.fetchone()[0] == 0 and os.path.exists(settings.DATA_PATH):
        df = pd.read_csv(settings.DATA_PATH)
        # Dynamic discovery of carbon footprint column
        carbon_col = next((c for c in df.columns if "total_lifecycle_carbon_footprint" in c), 'total_lifecycle_carbon_footprint')
        
        df_seed = df[['Timestamp', 'Product_ID', 'SKU_Name', 'Category', 'Region', 'Vendor', carbon_col, 'Hash', 'Prev_Hash']]
        df_seed.columns = ['timestamp', 'product_id', 'sku_name', 'category', 'region', 'vendor', 'total_lifecycle_carbon_footprint', 'hash', 'prev_hash']
        df_seed.to_sql('ledger', conn, if_exists='append', index=False)
        print(f"📦 Database seeded with {len(df_seed)} records from CSV.")
    
    conn.commit()
    conn.close()

def get_db_connection():
    """ Establishes a connection to the SQLite sustainability database.
    
    Returns:
        sqlite3.Connection: A connection object with Row factory enabled for dictionary-like access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_ledger_record(record_dict):
    """ Persists a new sustainability record to the immutable ledger.
    
    Args:
        record_dict (dict): A dictionary containing SKU telemetry, metrics, 
                           and SHA-256 hash-chain metadata.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ledger (timestamp, product_id, sku_name, category, region, vendor, total_lifecycle_carbon_footprint, hash, prev_hash, is_anomaly)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_dict['timestamp'], record_dict['product_id'], record_dict['sku_name'],
        record_dict['category'], record_dict['region'], record_dict['vendor'],
        record_dict.get('total_lifecycle_carbon_footprint', record_dict.get('carbon_footprint')), 
        record_dict['hash'], record_dict['prev_hash'],
        record_dict.get('is_anomaly', 0)
    ))
    conn.commit()
    conn.close()

def get_latest_hash():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM ledger ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row['hash'] if row else "0" * 64

if __name__ == "__main__":
    init_db()

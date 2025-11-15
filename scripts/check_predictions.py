#!/usr/bin/env python3
import psycopg2

db_url = 'postgresql://postgres.vmongtwawdphlraijxar:pSRhcw7okkHeSsH1@aws-1-eu-west-1.pooler.supabase.com:6543/postgres'

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name='predictions' 
        ORDER BY ordinal_position
    """)
    columns = cur.fetchall()
    print("Predictions table columns:")
    for col, dtype in columns:
        print(f"  {col}: {dtype}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

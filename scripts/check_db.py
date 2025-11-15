#!/usr/bin/env python3
import os
import psycopg2

db_url = 'postgresql://postgres.vmongtwawdphlraijxar:pSRhcw7okkHeSsH1@aws-1-eu-west-1.pooler.supabase.com:6543/postgres'

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cur.fetchall()]
    print("Existing tables:")
    for t in tables:
        print(f"  - {t}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")

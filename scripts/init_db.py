#!/usr/bin/env python3
"""
Supabase schema initialization script.
Reads schema.sql and executes SQL via PostgreSQL connection string.
"""

import os
import sys
import psycopg2
from psycopg2 import Error

def init_supabase_schema():
    """Initialize Supabase database schema."""
    
    # Get connection details from environment
    db_url = os.getenv('SUPABASE_PG_CONN') or os.getenv('DATABASE_URL')
    
    if not db_url:
        print("ERROR: SUPABASE_PG_CONN or DATABASE_URL not set in environment.")
        return False
    
    # Read schema SQL file
    schema_file = os.path.join(os.path.dirname(__file__), '..', 'supabase', 'schema.sql')
    
    if not os.path.exists(schema_file):
        print(f"ERROR: Schema file not found: {schema_file}")
        return False
    
    with open(schema_file, 'r') as f:
        schema_sql = f.read()
    
    try:
        # Connect to database
        print(f"Connecting to Supabase...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Execute schema SQL
        print("Creating tables...")
        cursor.execute(schema_sql)
        
        # Commit and close
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Schema successfully applied to Supabase!")
        return True
        
    except Error as e:
        print(f"ERROR: Failed to apply schema: {e}")
        return False

if __name__ == '__main__':
    success = init_supabase_schema()
    sys.exit(0 if success else 1)

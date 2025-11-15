#!/usr/bin/env bash
# Init Supabase DB (bash)
# Usage: SUPABASE_PG_CONN='postgresql://user:pass@host:port/db' ./scripts/init_db.sh

SCHEMA_FILE="$(dirname "$0")/../supabase/schema.sql"
if [ ! -f "$SCHEMA_FILE" ]; then
  echo "Schema file not found: $SCHEMA_FILE"
  exit 1
fi

if [ -z "$SUPABASE_PG_CONN" ]; then
  echo "No SUPABASE_PG_CONN provided. Print SQL for manual run."
  cat "$SCHEMA_FILE"
  exit 0
fi

if command -v psql >/dev/null 2>&1; then
  echo "Running psql against SUPABASE_PG_CONN"
  psql "$SUPABASE_PG_CONN" -f "$SCHEMA_FILE"
  exit $?
else
  echo "psql not found. Install Postgres client or run the SQL manually:"
  cat "$SCHEMA_FILE"
  exit 1
fi

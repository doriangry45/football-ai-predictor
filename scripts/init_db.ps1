# Init Supabase DB (PowerShell)
# Usage: set SUPABASE_DB_URL or SUPABASE_PG_CONN then run this script.
# This script attempts to use psql if available. It prints the SQL to run otherwise.

$schemaFile = "$(Resolve-Path ..\supabase\schema.sql)"
Write-Host "Using schema file: $schemaFile"

if (-not (Test-Path $schemaFile)) {
  Write-Error "Schema file not found: $schemaFile"
  exit 1
}

# Read connection info from env (prefer full connection string in SUPABASE_PG_CONN)
$pgConn = $env:SUPABASE_PG_CONN
if (-not $pgConn) {
  Write-Host "No SUPABASE_PG_CONN found. If you have Supabase project, you can run SQL via Supabase SQL editor or set SUPABASE_PG_CONN to a psql connection string."
  Write-Host "Example SUPABASE_PG_CONN=postgresql://user:password@host:port/dbname"
  Write-Host "Printing SQL for manual run:\n"
  Get-Content $schemaFile | Write-Host
  exit 0
}

# If psql command is available, run it
$psql = Get-Command psql -ErrorAction SilentlyContinue
if ($psql) {
  Write-Host "Running psql against connection string provided in SUPABASE_PG_CONN..."
  $env:PGPASSWORD = "" # optional
  psql $pgConn -f $schemaFile
  if ($LASTEXITCODE -ne 0) { Write-Error "psql failed with code $LASTEXITCODE"; exit $LASTEXITCODE }
  Write-Host "Schema applied successfully."
} else {
  Write-Host "psql not found in PATH. Print the SQL to run manually or install psql (Postgres client)."
  Get-Content $schemaFile | Write-Host
}

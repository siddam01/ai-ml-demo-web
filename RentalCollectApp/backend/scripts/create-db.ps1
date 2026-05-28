# Creates the rentflow database on local PostgreSQL (run once).
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Creating database 'rentflow' on local PostgreSQL..."
py -c @"
import psycopg
try:
    conn = psycopg.connect('postgresql://postgres:postgres@localhost:5432/postgres', autocommit=True)
    conn.execute('CREATE DATABASE rentflow')
    conn.close()
    print('Database rentflow created.')
except Exception as e:
    if 'already exists' in str(e).lower():
        print('Database rentflow already exists.')
    else:
        raise
"@

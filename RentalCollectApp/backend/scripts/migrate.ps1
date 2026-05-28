Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Running Alembic migrations..."
py -m alembic upgrade head
Write-Host "Migrations complete."

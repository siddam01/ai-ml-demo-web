Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Starting API on http://127.0.0.1:8000"
Write-Host "Swagger: http://127.0.0.1:8000/api/v1/docs"
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

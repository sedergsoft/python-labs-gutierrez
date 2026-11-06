$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$omniRouteDir = Join-Path $repoRoot "omniroute"
$envFile = Join-Path $omniRouteDir ".env"
$envExample = Join-Path $omniRouteDir ".env.example"
$dataDir = Join-Path $omniRouteDir "data"

if (-not (Test-Path $envFile)) {
    Copy-Item $envExample $envFile
    Write-Host "Created omniroute\.env from the local template."
}

New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
$null = & $env:ComSpec /c "docker image inspect diegosouzapw/omniroute:3.8.52 >nul 2>nul"
$imageAvailable = $LASTEXITCODE -eq 0
if ($imageAvailable) {
    docker compose --env-file $envFile --project-directory $omniRouteDir up -d
    if ($LASTEXITCODE -ne 0) {
        throw "Docker Compose could not start OmniRoute."
    }
} elseif (Get-Command omniroute.cmd -ErrorAction SilentlyContinue) {
    $env:DATA_DIR = $dataDir
    $env:PORT = "20128"
    $env:DASHBOARD_PORT = "20128"
    $env:API_PORT = "20129"
    $env:API_HOST = "127.0.0.1"
    $env:REQUIRE_API_KEY = "true"
    omniroute.cmd serve --port 20128 --no-open --no-tray --daemon
    if ($LASTEXITCODE -ne 0) {
        throw "The local OmniRoute npm installation could not start."
    }
    Write-Host "Using local npm installation because the Docker image is not available."
} else {
    throw "OmniRoute is unavailable. Pull the Docker image or install it with npm."
}

if ($imageAvailable) {
    docker compose --env-file $envFile --project-directory $omniRouteDir ps
}
Write-Host "Dashboard: http://localhost:20128"
Write-Host "API:       http://localhost:20129/v1"

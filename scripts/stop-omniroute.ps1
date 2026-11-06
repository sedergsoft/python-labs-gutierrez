$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$omniRouteDir = Join-Path $repoRoot "omniroute"
$envFile = Join-Path $omniRouteDir ".env"

if (-not (Test-Path $envFile)) {
    Write-Host "OmniRoute has not been configured or started yet."
    exit 0
}

docker compose --env-file $envFile --project-directory $omniRouteDir down
if (Get-Command omniroute.cmd -ErrorAction SilentlyContinue) {
    & omniroute.cmd stop 2>&1 | Out-Null
}

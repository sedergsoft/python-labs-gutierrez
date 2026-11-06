$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$omniRouteDir = Join-Path $repoRoot "omniroute"
$envFile = Join-Path $omniRouteDir ".env"

if (-not (Test-Path $envFile)) {
    throw "Missing omniroute\.env. Start OmniRoute first."
}
if (-not (Get-Command omniroute.cmd -ErrorAction SilentlyContinue)) {
    throw "The local OmniRoute CLI is not installed. Use the dashboard or install the npm package."
}

$providers = @(
    @{ Id = "openrouter"; Env = "OMNIROUTE_OPENROUTER_API_KEY" },
    @{ Id = "openai"; Env = "OMNIROUTE_OPENAI_API_KEY" },
    @{ Id = "anthropic"; Env = "OMNIROUTE_ANTHROPIC_API_KEY" },
    @{ Id = "google"; Env = "OMNIROUTE_GOOGLE_API_KEY" },
    @{ Id = "deepseek"; Env = "OMNIROUTE_DEEPSEEK_API_KEY" },
    @{ Id = "groq"; Env = "OMNIROUTE_GROQ_API_KEY" }
)

foreach ($line in Get-Content $envFile) {
    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], "Process")
    }
}

foreach ($provider in $providers) {
    $credential = [Environment]::GetEnvironmentVariable($provider.Env, "Process")
    if ([string]::IsNullOrWhiteSpace($credential)) {
        Write-Host "Skipping $($provider.Id): $($provider.Env) is empty."
        continue
    }
    omniroute.cmd providers add $provider.Id --credential-env $provider.Env --name $provider.Id --yes
    if ($LASTEXITCODE -ne 0) {
        throw "Could not configure provider $($provider.Id)."
    }
}

omniroute.cmd providers validate

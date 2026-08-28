$ErrorActionPreference = "Stop"

function Get-ProjectRoot {
    $current = Get-Location

    while ($null -ne $current) {
        $aiPath = Join-Path $current.Path ".ai"

        if (Test-Path $aiPath -PathType Container) {
            return $current.Path
        }

        $current = $current.Parent
    }

    throw "Directory .ai not found in current path or parent directories."
}

function Get-DirectoryHash {
    param (
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    $files = Get-ChildItem -Path $Path -File -Recurse -Force |
        Where-Object {
            $_.FullName -notmatch "[\\/]\.ai[\\/]cache[\\/]" -and
            $_.FullName -notmatch "[\\/]\.ai[\\/]\.codex-state[\\/]"
        } |
        Sort-Object FullName

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $stream = New-Object System.IO.MemoryStream
    $writer = New-Object System.IO.StreamWriter($stream)

    foreach ($file in $files) {
        $relativePath = $file.FullName.Substring($Path.Length).TrimStart('\', '/')
        $fileHash = Get-FileHash -Path $file.FullName -Algorithm SHA256

        $writer.WriteLine("$relativePath|$($fileHash.Hash)")
    }

    $writer.Flush()
    $stream.Position = 0

    $hashBytes = $sha256.ComputeHash($stream)
    $hash = [System.BitConverter]::ToString($hashBytes).Replace("-", "").ToLowerInvariant()

    $writer.Dispose()
    $stream.Dispose()
    $sha256.Dispose()

    return $hash
}

function Sync-CodexFolders {
    param (
        [Parameter(Mandatory = $true)]
        [string] $ProjectRoot,

        [Parameter(Mandatory = $true)]
        [string] $AiRoot
    )

    $agentsRoot = Join-Path $ProjectRoot ".agents"
    $codexRoot = Join-Path $ProjectRoot ".codex"

    if (Test-Path $agentsRoot) {
        Remove-Item $agentsRoot -Recurse -Force
    }

    if (Test-Path $codexRoot) {
        Remove-Item $codexRoot -Recurse -Force
    }

    New-Item -Path (Join-Path $agentsRoot "skills") -ItemType Directory -Force | Out-Null
    New-Item -Path (Join-Path $codexRoot "rules") -ItemType Directory -Force | Out-Null

    $sourceAgents = Join-Path $AiRoot "agents"
    $sourceSkills = Join-Path $AiRoot "skills"
    $sourceRules = Join-Path $AiRoot "rules"
    $sourceHooks = Join-Path $AiRoot "hooks.json"
    $sourceConfig = Join-Path $AiRoot "config.toml"
    $sourceAgentsMd = Join-Path $AiRoot "AGENTS.md"

    if (Test-Path $sourceSkills -PathType Container) {
        Copy-Item -Path (Join-Path $sourceSkills "*") `
            -Destination (Join-Path $agentsRoot "skills") `
            -Recurse `
            -Force
    }

    if (Test-Path $sourceRules -PathType Container) {
        Copy-Item -Path (Join-Path $sourceRules "*") `
            -Destination (Join-Path $codexRoot "rules") `
            -Recurse `
            -Force
    }

    if (Test-Path $sourceHooks -PathType Leaf) {
        Copy-Item -Path $sourceHooks `
            -Destination (Join-Path $codexRoot "hooks.json") `
            -Force
    }

    if (Test-Path $sourceConfig -PathType Leaf) {
        Copy-Item -Path $sourceConfig `
            -Destination (Join-Path $codexRoot "config.toml") `
            -Force
    }

    if (Test-Path $sourceAgentsMd -PathType Leaf) {
        Copy-Item -Path $sourceAgentsMd `
            -Destination (Join-Path $ProjectRoot "AGENTS.md") `
            -Force
    }

    if (Test-Path $sourceAgents -PathType Container) {
        New-Item -Path (Join-Path $codexRoot "agents") -ItemType Directory -Force | Out-Null

        Copy-Item -Path (Join-Path $sourceAgents "*") `
            -Destination (Join-Path $codexRoot "agents") `
            -Recurse `
            -Force
    }
}

function Test-CodexFoldersReady {
    param (
        [Parameter(Mandatory = $true)]
        [string] $ProjectRoot
    )

    $agentsRoot = Join-Path $ProjectRoot ".agents"
    $codexRoot = Join-Path $ProjectRoot ".codex"

    return (
        (Test-Path (Join-Path $agentsRoot "skills") -PathType Container) -and
        (Test-Path (Join-Path $codexRoot "rules") -PathType Container)
    )
}

function Disable-GeneratedFolderForRun {
    param (
        [Parameter(Mandatory = $true)]
        [string] $ProjectRoot,

        [Parameter(Mandatory = $true)]
        [string] $FolderName
    )

    $folderRoot = Join-Path $ProjectRoot $FolderName

    if (-not (Test-Path $folderRoot -PathType Container)) {
        return $null
    }

    $suffix = 0

    do {
        $suffix++
        $disabledRoot = Join-Path $ProjectRoot "$FolderName.startup-error.$PID.$suffix"
    } while (Test-Path $disabledRoot)

    Move-Item -LiteralPath $folderRoot -Destination $disabledRoot -Force

    return @{
        FolderRoot = $folderRoot
        DisabledRoot = $disabledRoot
    }
}

function Disable-GeneratedFoldersForRun {
    param (
        [Parameter(Mandatory = $true)]
        [string] $ProjectRoot
    )

    $disabledFolders = @()

    foreach ($folderName in @(".agents", ".codex")) {
        $disabledFolder = Disable-GeneratedFolderForRun -ProjectRoot $ProjectRoot -FolderName $folderName

        if ($null -ne $disabledFolder) {
            $disabledFolders += $disabledFolder
        }
    }

    return $disabledFolders
}

function Restore-GeneratedFoldersAfterRun {
    param (
        [Parameter(Mandatory = $true)]
        [object[]] $DisabledFolders
    )

    foreach ($disabledFolder in $DisabledFolders) {
        $folderRoot = $disabledFolder.FolderRoot
        $disabledRoot = $disabledFolder.DisabledRoot

        if (-not (Test-Path $disabledRoot -PathType Container)) {
            continue
        }

        if (Test-Path $folderRoot) {
            [Console]::Error.WriteLine("Codex startup warning: skipped restoring '$disabledRoot' because '$folderRoot' now exists.")
            continue
        }

        Move-Item -LiteralPath $disabledRoot -Destination $folderRoot -Force
    }
}

$startupLocation = Get-Location
$projectRoot = $startupLocation.Path
$disabledFolders = @()
$codexExitCode = $null

try {
    $projectRoot = Get-ProjectRoot
    $aiRoot = Join-Path $projectRoot ".ai"
    $stateRoot = Join-Path $aiRoot ".codex-state"
    $hashFile = Join-Path $stateRoot "last-ai-hash.txt"

    New-Item -Path $stateRoot -ItemType Directory -Force | Out-Null

    $currentHash = Get-DirectoryHash -Path $aiRoot
    $previousHash = $null

    if (Test-Path $hashFile -PathType Leaf) {
        $previousHash = Get-Content $hashFile -Raw
        $previousHash = $previousHash.Trim()
    }

    if (($currentHash -ne $previousHash) -or (-not (Test-CodexFoldersReady -ProjectRoot $projectRoot))) {
        Sync-CodexFolders -ProjectRoot $projectRoot -AiRoot $aiRoot
        Set-Content -Path $hashFile -Value $currentHash -NoNewline
    }
}
catch {
    [Console]::Error.WriteLine("Codex startup warning: failed to generate .agents and .codex from .ai.")
    [Console]::Error.WriteLine("Codex startup warning: $($_.Exception.Message)")
    [Console]::Error.WriteLine("Codex startup warning: continuing normal startup with generated .agents and .codex disabled for this run.")

    try {
        $disabledFolders = Disable-GeneratedFoldersForRun -ProjectRoot $projectRoot
    }
    catch {
        [Console]::Error.WriteLine("Codex startup warning: could not disable generated folders: $($_.Exception.Message)")
    }
}

Push-Location $projectRoot

try {
    & codex @args
    $codexExitCode = $LASTEXITCODE
}
finally {
    Pop-Location

    if ($disabledFolders.Count -gt 0) {
        Restore-GeneratedFoldersAfterRun -DisabledFolders $disabledFolders
    }
}

if ($null -ne $codexExitCode) {
    exit $codexExitCode
}

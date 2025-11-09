Set-Location $PSScriptRoot

$serviceScripts = Get-ChildItem -Path $PSScriptRoot -Directory | ForEach-Object {
    Get-ChildItem -Path $_.FullName -Filter 'run.ps1' | Select-Object -First 1
}

$procs = @()

foreach ($script in $serviceScripts) {
    $workDir = Split-Path $script
    Write-Host "Starting service: $($script.FullName)"

    $proc = Start-Process powershell `
        -WorkingDirectory $workDir `
        -PassThru `
        -ArgumentList "-NoExit", "-NoLogo", "-ExecutionPolicy", "Bypass", "-File", "`"$($script.FullName)`""
    
    $procs += $proc
}

Write-Host "All services started. Press 'q' to stop all services."

while ($true) {
    $input = Read-Host
    if ($input -match "q") {
        Write-Host "Stopping all services..."
        foreach ($proc in $procs) {
            try {
                Stop-Process -Id $proc.Id -Force -ErrorAction Stop
                Write-Host "Stopped process $($proc.Id)"
            } catch {
                Write-Host "Process $($proc.Id) already closed."
            }
        }
        break
    } else {
        Write-Host "Press 'q' to stop all services."
    }
}
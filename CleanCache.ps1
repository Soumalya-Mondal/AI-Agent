# define parent folder path
$parentFolderPath = (Resolve-Path ".").Path

# initialize counters
$deletedCount = 0
$failedCount = 0

# find all "__pycache__" folders
try {
    $enumerationOptions = [System.IO.EnumerationOptions]::new()
    $enumerationOptions.RecurseSubdirectories = $true
    $enumerationOptions.IgnoreInaccessible = $true
    $enumerationOptions.AttributesToSkip = [System.IO.FileAttributes]::ReparsePoint

    $pycacheFolders = [System.IO.Directory]::GetDirectories(
        $parentFolderPath,
        "__pycache__",
        $enumerationOptions
    )
}
catch {
    Write-Output "ERROR - $($_)"
    exit 1
}

# normalize and de-duplicate paths (helps when symlinked folders like lib64 point to lib)
$uniqueFolders = [System.Collections.Generic.HashSet[string]]::new()
foreach ($folder in $pycacheFolders) {
    try {
        $resolvedFolder = (Resolve-Path -LiteralPath $folder -ErrorAction Stop).ProviderPath
        [void]$uniqueFolders.Add($resolvedFolder)
    }
    catch {
        # ignore folders that no longer resolve
    }
}
$pycacheFolders = @($uniqueFolders)

# delete all the "__pycache__" folders
if ($pycacheFolders.Count -gt 0) {
    foreach ($folder in $pycacheFolders) {
        try {
            if (Test-Path -LiteralPath $folder) {
                Remove-Item -LiteralPath $folder -Recurse -Force -ErrorAction Stop
                $deletedCount++
            }
        }
        catch {
            $failedCount++
        }
    }
    
    Write-Output ""
    Write-Output "=========================================="
    Write-Output "Summary:"
    Write-Output "  Total found: $($pycacheFolders.Count)"
    Write-Output "  Successfully deleted: $deletedCount"
    if ($failedCount -gt 0) {
        Write-Output "  Failed: $failedCount"
    }
    Write-Output "=========================================="
}
else {
    Write-Output "No __pycache__ folders found!"
}

$dbPath = Join-Path -Path $parentFolderPath -ChildPath "database/chat_conversations.db"
if (Test-Path $dbPath) {
    Write-Output ""
    $deleteDb = Read-Host "Also delete database file 'database\chat_conversations.db'? [y/N]"
    if ($deleteDb -match '^[Yy]') {
        try {
            Remove-Item -LiteralPath $dbPath -Force -ErrorAction Stop
            $deletedCount++
            Write-Output "Database file deleted."
        }
        catch {
            $failedCount++
            Write-Output "Failed to delete database file."
        }
    }
}

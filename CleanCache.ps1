# define parent folder path
$parentFolderPath = (Resolve-Path ".").Path

# initialize counters
$deletedCount = 0
$failedCount = 0

# find all "__pycache__" folders
try {
    $pycacheFolders = [System.IO.Directory]::GetDirectories($parentFolderPath, "__pycache__", [System.IO.SearchOption]::AllDirectories)
}
catch {
    Write-Output "ERROR - $($_)"
    exit 1
}

# delete all the "__pycache__" folders
if ($pycacheFolders.Count -gt 0) {
    foreach ($folder in $pycacheFolders) {
        try {
            Remove-Item -Path $folder -Recurse -Force
            $deletedCount++
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
            Remove-Item -Path $dbPath -Force
            $deletedCount++
            Write-Output "Database file deleted."
        }
        catch {
            $failedCount++
            Write-Output "Failed to delete database file."
        }
    }
}
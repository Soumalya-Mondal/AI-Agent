# define parent folder path
$parentFolderPath = (Resolve-Path ".").Path

# initialize counters
$deletedCount = 0
$failedCount = 0

# find all "__pycache__" folders
try {
    $pycacheFolders = Get-ChildItem -Path $parentFolderPath -Recurse -Directory -Filter "__pycache__"
}
catch {
    Write-Output "ERROR - $($_)"
    exit 1
}

# delete all the "__pycache__" folders
if ($pycacheFolders.Count -gt 0) {
    $pycacheFolders | ForEach-Object {
        try {
            Remove-Item -Path $_.FullName -Recurse -Force
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
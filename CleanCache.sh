#!/usr/bin/env bash
set -euo pipefail

parent_folder_path="$(pwd)"
deleted_count=0
failed_count=0

mapfile -t pycache_folders < <(find "$parent_folder_path" -type d -name "__pycache__" 2>/dev/null)

if [ ${#pycache_folders[@]} -gt 0 ]; then
    for folder in "${pycache_folders[@]}"; do
        if rm -rf "$folder" 2>/dev/null; then
            ((++deleted_count))
        else
            ((++failed_count))
        fi
    done

    echo ""
    echo "=========================================="
    echo "Summary:"
    echo "  Total found: ${#pycache_folders[@]}"
    echo "  Successfully deleted: $deleted_count"
    if [ "$failed_count" -gt 0 ]; then
        echo "  Failed: $failed_count"
    fi
    echo "=========================================="
else
    echo "No __pycache__ folders found!"
fi

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

db_path="$parent_folder_path/database/chat_conversations.db"
if [ -f "$db_path" ]; then
    echo ""
    read -rp "Also delete database file 'database/chat_conversations.db'? [y/N]: " delete_db
    if [[ "$delete_db" =~ ^[Yy]$ ]]; then
        if rm -f "$db_path" 2>/dev/null; then
            ((++deleted_count))
            echo "Database file deleted."
        else
            ((++failed_count))
            echo "Failed to delete database file."
        fi
    fi
fi

log_path="$parent_folder_path/log/aiagentlogs.db"
if [ -f "$log_path" ]; then
    echo ""
    read -rp "Also delete log database file 'log/aiagentlogs.db'? [y/N]: " delete_log
    if [[ "$delete_log" =~ ^[Yy]$ ]]; then
        if rm -f "$log_path" 2>/dev/null; then
            ((++deleted_count))
            echo "Log database file deleted."
        else
            ((++failed_count))
            echo "Failed to delete log database file."
        fi
    fi
fi

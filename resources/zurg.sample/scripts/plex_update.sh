#!/bin/bash

# =============================================================================
# PLEX PARTIAL SCAN SCRIPT
# =============================================================================
# This script is triggered by Zurg when library changes are detected.
# It performs a partial library refresh on Plex for the changed paths only.
#
# Configuration in zurg config.yml:
#   on_library_update: sh /app/config/plex_update.sh "$@"
#
# How to get your Plex token:
#   1. Open Plex in a browser and sign in
#   2. Open browser dev console (F12)
#   3. Run: window.localStorage.getItem("myPlexAccessToken")
#
# Credits: godver3, wasabipls
# =============================================================================

# Configuration - Update these values for your setup
# If using Docker, plex_url is typically http://plex:32400 (container name)
# or http://172.17.0.1:32400 (Docker host IP)
plex_url="${PLEX_URL:-http://plex:32400}"
token="${PLEX_TOKEN:-YOUR_PLEX_TOKEN}"
zurg_mount="${ZURG_MOUNT_PATH:-/mnt/zurg}"

# Validate configuration
if [ "$token" = "YOUR_PLEX_TOKEN" ] || [ -z "$token" ]; then
    echo "Warning: Plex token not configured. Library updates will not work."
    echo "Please set PLEX_TOKEN environment variable or update this script."
    exit 0
fi

# Get the list of Plex library section IDs
# Using grep instead of xmllint for better compatibility
echo "Fetching Plex library sections..."
section_ids=$(curl -sLX GET "$plex_url/library/sections" -H "X-Plex-Token: $token" 2>/dev/null | grep -oP 'key="\K[^"]+' | head -20)

if [ -z "$section_ids" ]; then
    echo "Warning: Could not fetch Plex library sections. Check plex_url and token."
    exit 1
fi

echo "Found sections: $section_ids"

# Process each changed path
for arg in "$@"
do
    # Remove backslashes from path
    parsed_arg="${arg//\\}"
    modified_arg="$zurg_mount/$parsed_arg"

    echo "============================================"
    echo "Detected update on: $arg"
    echo "Absolute path: $modified_arg"

    for section_id in $section_ids
    do
        echo "Refreshing section $section_id..."
        curl -s -G -H "X-Plex-Token: $token" \
            --data-urlencode "path=$modified_arg" \
            "$plex_url/library/sections/$section_id/refresh" > /dev/null 2>&1
    done
done

echo "============================================"
echo "All updated sections refreshed successfully"

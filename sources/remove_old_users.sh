#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# shut down all ezarr containers referenced by docker-compose.yml
# If you previously had ezarr installed somewhere else you have to do this manually in the directory where the docker-compose file is.
sudo docker compose -f "$PROJECT_ROOT/docker-compose.yml" down

# Remove old users and group
sudo userdel sonarr
sudo userdel radarr
sudo userdel lidarr
sudo userdel mylar
sudo userdel prowlarr
sudo userdel qbittorrent
sudo userdel jackett
sudo userdel plex
sudo userdel sabnzbd
sudo userdel bazarr
sudo userdel audiobookshelf
# Legacy: zurg/rclone/rdtclient were replaced by decypharr (which runs as ${UID}, no dedicated user).
# Kept here so upgrades from the old debrid stack still clean up these users.
sudo userdel zurg
sudo userdel rclone
sudo userdel rdtclient
sudo groupdel mediacenter


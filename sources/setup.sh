#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Set up your .env file BEFORE running this script!!!
# export all variables from .env
set -a
source "$PROJECT_ROOT/.env"
set +a
# This is always going to complain about UID being a read-only variable. 
# However that is not a problem and it's necessary for UID to be defined in the .env so that docker-compose.yml can take it.
# Reminder to set the UID variable in .env if you haven't already. It needs to be the user you want to run docker as. Find what it should be by running "id -u" from that user's shell.

# Make users and group
sudo useradd sonarr -u $SONARR_UID
sudo useradd radarr -u $RADARR_UID
sudo useradd lidarr -u $LIDARR_UID
sudo useradd mylar -u $MYLAR_UID
sudo useradd prowlarr -u $PROWLARR_UID
sudo useradd qbittorrent -u $QBITTORRENT_UID
sudo useradd jackett -u $JACKETT_UID
sudo useradd plex -u $PLEX_UID
sudo useradd sabnzbd -u $SABNZBD_UID
sudo useradd bazarr -u $BAZARR_UID
sudo useradd audiobookshelf -u $AUDIOBOOKSHELF_UID
sudo groupadd mediacenter -g $MEDIACENTER_GID

# Adds current user to the mediacenter group. This is recommended so that you can still have access to files inside the ezarr folder structure for manual control.
# This is way better than just doing everything as root, especially on NFS shares. Also some services run as the default user anyway (Jellyfin, Tautulli).
sudo usermod -a -G mediacenter $USER
# When you add the user to the group the changes don't take effect immediately. 
# You can force them by running "sudo newgrp mediacenter" but that won't always work and it's better to just reboot after the script finishes running.

# adds all the service users to the group 
sudo usermod -a -G mediacenter sonarr
sudo usermod -a -G mediacenter radarr
sudo usermod -a -G mediacenter lidarr
sudo usermod -a -G mediacenter mylar
sudo usermod -a -G mediacenter prowlarr
sudo usermod -a -G mediacenter qbittorrent
sudo usermod -a -G mediacenter jackett
sudo usermod -a -G mediacenter plex
sudo usermod -a -G mediacenter sabnzbd
sudo usermod -a -G mediacenter bazarr
sudo usermod -a -G mediacenter audiobookshelf

# Make directories
# ${ROOT_DIR:-.}/ means take the value from ROOT_DIR value, if failed or empty place it in the current folder
sudo mkdir -pv ${ROOT_DIR:-.}/config/{sonarr,radarr,lidarr,mylar,prowlarr,qbittorrent,jackett,audiobookshelf,seerr,plex,jellyfin,tautulli,sabnzbd,bazarr,decypharr,kapowarr,questarr,romm,gameyfin,drop,feishin,wizarr,homer,traefik,caddy,nginx-proxy-manager}-config
sudo mkdir -pv ${ROOT_DIR:-.}/data/{torrents,usenet,media}/{tv,movies,music,books,comics,audiobooks,podcasts,audiobookshelf-metadata,games}

# Debrid mount point for decypharr (must exist on the host; decypharr mounts the debrid library here)
sudo mkdir -pv ${DECYPHARR_MOUNT_PATH:-/mnt/debrid}

# Set permissions
sudo chmod -R 775 ${ROOT_DIR:-.}/data/
sudo chmod -R 775 ${ROOT_DIR:-.}/config/
sudo chown -R $UID:mediacenter ${ROOT_DIR:-.}/data/
sudo chown -R $UID:mediacenter ${ROOT_DIR:-.}/config/
sudo chown -R sonarr:mediacenter ${ROOT_DIR:-.}/config/sonarr-config
sudo chown -R radarr:mediacenter ${ROOT_DIR:-.}/config/radarr-config
sudo chown -R lidarr:mediacenter ${ROOT_DIR:-.}/config/lidarr-config
sudo chown -R mylar:mediacenter ${ROOT_DIR:-.}/config/mylar-config
sudo chown -R prowlarr:mediacenter ${ROOT_DIR:-.}/config/prowlarr-config
sudo chown -R qbittorrent:mediacenter ${ROOT_DIR:-.}/config/qbittorrent-config
sudo chown -R jackett:mediacenter ${ROOT_DIR:-.}/config/jackett-config
sudo chown -R $UID:mediacenter ${ROOT_DIR:-.}/config/seerr-config
sudo chown -R plex:mediacenter ${ROOT_DIR:-.}/config/plex-config
sudo chown -R $UID:mediacenter ${ROOT_DIR:-.}/config/jellyfin-config
sudo chown -R $UID:mediacenter ${ROOT_DIR:-.}/config/tautulli-config
sudo chown -R sabnzbd:mediacenter ${ROOT_DIR:-.}/config/sabnzbd-config
sudo chown -R bazarr:mediacenter ${ROOT_DIR:-.}/config/bazarr-config
sudo chown -R audiobookshelf:mediacenter ${ROOT_DIR:-.}/config/audiobookshelf-config

# decypharr runs as ${UID} and owns its own mount point; config/decypharr-config is already
# owned by ${UID} via the recursive chown of config/ above.
sudo chown -R $UID:mediacenter ${DECYPHARR_MOUNT_PATH:-/mnt/debrid}

echo "Done! It is recommended to reboot now."

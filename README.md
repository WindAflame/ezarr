# Ezarr
[![Check running](https://github.com/WindAflame/ezarr/actions/workflows/check_running.yml/badge.svg)](https://github.com/WindAflame/ezarr/actions/workflows/check_running.yml)

Ezarr is a project built to make it EZ to deploy a Servarr mediacenter on an Ubuntu server. The
badge above means that the shell script and docker-compose file in this repository at least *don't
crash*. It doesn't necessarily mean it will run well on your system ;) 
It's set up to follow the [TRaSH guidelines](https://trash-guides.info/Hardlinks/How-to-setup-for/Docker/) so it should at least perform optimally.

Services are grouped into categories, each in its own file under `compose/`, and
toggled from the central `docker-compose.yml.sample` (see [Using](#using)). Within
a category you can pick and choose individual services (for example Prowlarr *or*
Jackett, Plex *or* Jellyfin). It features:

### Media management (`compose/servarr.yml`)
- [Sonarr](https://sonarr.tv/) is an application to manage TV shows. It is capable of keeping track
  of what you'd like to watch, at what quality, in which language and more, and can find a place to
  download this if connected to Prowlarr and qBittorrent. It can also reorganize the media you
  already own in order to create a more uniformly formatted collection.
- [Radarr](https://radarr.video/) is like Sonarr, but for movies.
- [Bazarr](https://www.bazarr.media/) is a companion application to Sonarr and Radarr that manages
  and downloads subtitles based on your requirements.
- [Lidarr](https://lidarr.audio/) is like Sonarr, but for music.
- [Kapowarr](https://github.com/Casvt/Kapowarr) is like Sonarr, but for comic books. It replaces the
  previously used Mylar3. Connect it to Prowlarr the same way as the other -arr apps (add app), using
  an API key you generate within Kapowarr.
- [Questarr](https://github.com/Doezer/Questarr) brings the *arr experience to video games, tracking
  and organizing your game library.
- [Audiobookshelf](https://www.audiobookshelf.org/) is a self-hosted audiobook and podcast server.

### Indexers (`compose/indexers.yml`)
- [Prowlarr](https://wiki.servarr.com/prowlarr) can keep track of indexers, which are services that
  keep track of Torrent or UseNet links. One can search an indexer for certain content and find a
  where to download this. **Note**: when adding an indexer, please do not set the "seed ratio" to
  less than 1. Less than 1 means that you upload less than you download. Not only is this
  unfriendly towards your fellow users, but it can also get you banned from certain indexers.
- [Jackett](https://github.com/Jackett/Jackett) is an alternative to Prowlarr.
- [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr) is a proxy server to bypass Cloudflare and DDoS-GUARD protection.

### Media servers (`compose/media-servers.yml`)
- [PleX](https://www.plex.tv/) is a mediaserver. Using this, you get access to a Netflix-like
  interface across many devices like your laptop or computer, your phone, your TV and more. For
  some features, you need a [PleX pass](https://www.plex.tv/nl/plex-pass/).
- [Jellyfin](https://jellyfin.org/) is an alternative for PleX. Which you'd like to use is a matter
  of preference, and you *could* even use both, although this is probably a waste of resources.
- [Feishin](https://github.com/jeffvli/feishin) is a modern music client that streams from a Jellyfin,
  Navidrome or Subsonic library (pre-configured here to lock onto Jellyfin).
- [Romm](https://romm.app/) is a ROM library manager: it scans, organizes and lets you browse and
  play your retro game collection, enriched with metadata and cover art from IGDB.
- [Gameyfin](https://gameyfin.org/) is a game library frontend that scans a local games folder and
  serves a discovery interface (a lighter, PC-oriented alternative to Romm).
- [Drop](https://droposs.org/) is a self-hosted game library and store — an open-source alternative
  to Steam/Epic. It lets you browse, manage and play your collection through a web UI and a native
  desktop client, with metadata imported from IGDB/GiantBomb/PCGamingWiki. Drop ships with its own
  bundled PostgreSQL database (the `drop-db` service), which is internal-only and not exposed on the
  host. Set `DROP_EXTERNAL_URL` in your `.env` to the URL where Drop will be reachable.

### Requests & user management (`compose/requests.yml`)
- [Seerr](https://seerr.dev) is a request and media discovery portal for Plex and Jellyfin. Users can
  browse, search and request movies and shows, which are then handed off to Sonarr/Radarr to download
  automatically.
- [Tautulli](https://tautulli.com/) is a monitoring application for PleX  which can keep track of
  what has been watched, who watched it, when and where they watched it, and how it was watched.
- [Wizarr](https://github.com/wizarrrr/wizarr) manages user invitations and onboarding for
  Plex/Jellyfin/Emby, so you can hand out self-service invites instead of creating accounts by hand.

### Download clients (`compose/download-clients.yml`)
- [qBittorrent](https://www.qbittorrent.org/) can download torrents and provides a bunch more
  features for management.
- [SABnzbd](https://sabnzbd.org/) can download nzb's (Usenet) and provides a bunch more features for
  management.
- [RDTClient](https://github.com/rogerfar/rdt-client) is a download client that manages your
  Real-Debrid torrents and downloads, and integrates with the -arr apps like a regular client.

### Debrid (`compose/debrid.yml`)
- [Zurg](https://github.com/debridmediamanager/zurg-testing) exposes your Real-Debrid library as a
  self-hosted WebDAV server.
- [rclone](https://rclone.org/) mounts that Zurg WebDAV share as a local filesystem so Plex/Jellyfin
  can read Real-Debrid content directly. Zurg and rclone are enabled together.

### Dashboard (`compose/dashboard.yml`)
- [Homarr](https://homarr.dev/) is _a sleek, modern dashboard that puts all of your apps and services at your fingertips._
- [Homer](https://github.com/bastienwirtz/homer) is a lightweight static dashboard configured through
  a single YAML file (a simpler alternative to Homarr).

### Reverse proxy (`compose/reverse-proxy.yml`, optional)
Pick **one** of the following to expose your services over HTTPS (see the note in
`docker-compose.yml.sample`):
- [Traefik](https://traefik.io/traefik/) is a dynamic reverse proxy with automatic Let's Encrypt
  certificates and Docker-native service discovery.
- [Caddy](https://caddyserver.com/) is a file-driven reverse proxy with automatic HTTPS, configured
  via a `Caddyfile`.
- [Nginx Proxy Manager](https://nginxproxymanager.com/) provides a web UI to manage nginx reverse
  proxy rules and Let's Encrypt certificates.

## Requirements
Currently, this script only works on Linux. There is a chance that the sample docker compose file will work on Windows,
although untested. The only requirements other than that are **Python 3** and **docker** with **docker-compose-v2**.
While this script _may_ work on docker-compose-v1 it's made to be and highly recommended to be run using v2.
The easiest way to install these dependencies on Ubuntu and other Debian-based distors is by running:
```
sudo apt-get install python3 docker.io docker-compose-v2
```
For other Linux distros you may have to use a different package manager or download directly from docker's website.

## Using

### How the compose files are organized
Ezarr uses a **modular** Docker Compose setup. The top-level `docker-compose.yml.sample`
does not define any service itself; instead it `include:`s one file per category from
the `compose/` directory (`servarr.yml`, `indexers.yml`, `media-servers.yml`,
`requests.yml`, `download-clients.yml`, `debrid.yml`, `dashboard.yml` and, optionally,
`reverse-proxy.yml`):

```yaml
include:
  - compose/servarr.yml
  - compose/indexers.yml
  # ...
  # Uncomment ONE of the three reverse proxies:
  # - compose/reverse-proxy.yml
```

This requires Docker Compose **v2.20+** (check with `docker compose version`). To
disable a whole category, comment out its line in `docker-compose.yml.sample`. For
finer-grained control (e.g. Plex vs Jellyfin, qBittorrent vs SABnzbd, Homarr vs Homer),
keep the category included and comment out individual services inside the matching file
in `compose/`. Configuration is driven by the variables in your `.env` file (see
[Environment variables](#environment-variables)).

> **Reverse proxy:** the three reverse proxies (Traefik, Caddy, Nginx Proxy Manager)
> all bind ports 80/443, so enable **only one** of them.

### Using the CLI
To make things easier, a CLI has been developed. First, clone the repository in a directory of your
choosing. You can run it by entering `python3 sources/main.py` and the CLI will guide you through the
process. This is the recommended method if you're setting this up for the first time on a new system. 
Please take a look at [important notes](#important-notes) before you continue. 
**NOTE: This script will create users for each container with IDs ranging from 13001 to 13017. 
If you want to choose your own IDs (or some of them are occupied) you have to go through the manual install.**

### Manually
If you're installing this for the first time simply follow these steps. 
If you're coming from an older version or reinstalling with different IDs, run `remove_old_users.sh` to clean up old users and then follow these steps.
1. To get started, clone the repository in a directory of your choosing. `git clone https://github.com/WindAflame/ezarr.git`
2. Copy `.env.sample` to a real `.env` by running `$ cp .env.sample .env`.
3. Set the environment variables to your liking (see [Environment variables](#environment-variables) for the full list). Pay special attention to `ROOT_DIR` as this is where everything is going to be stored in.
   The path in this value needs to be **absolute** and start with `/`. Leaving it empty is **not** recommended: because of how Docker Compose expands `${ROOT_DIR}`, an empty value resolves to `/config/...` and `/data/...` at the **root of your filesystem**, not the current directory.
   `UID` should be set to the ID of the user that you want to run docker with. You can find this by running `id -u` from that user's shell.
4. Run `setup.sh` as superuser. This will set up your users, a system of directories and ensure permissions are set correctly.
5. Copy `docker-compose.yml.sample` to a real `docker-compose.yml` by running `$ cp docker-compose.yml.sample docker-compose.yml`.
6. Choose which services to run (see [How the compose files are organized](#how-the-compose-files-are-organized)):
   - In `docker-compose.yml`, comment out (`#`) any whole category you don't want. If you want a reverse proxy, uncomment **exactly one** of the three under the reverse-proxy line.
   - For finer control (for example, running PleX and Jellyfin at the same time is a bit unusual), keep the category included and comment out individual services inside the matching file in `compose/`.
   - Double check that your `.env` file is set up properly. Also make sure to add a newly generated encryption key to the Homarr section in `compose/dashboard.yml`, if you want to use it.
7. If you want to use zurg, you need to copy `resources/zurg.sample` to `resources/zurg` by running `$ cp -r resources/zurg.sample resources/zurg`.
   Also, configure it with its documentation.
8. Run `docker compose up -d` to start the containers. If it complains about permissions run the following commands to add your current user to the docker group and apply changes:
    ```
    sudo groupadd docker
    sudo usermod -aG docker $USER
    newgrp docker
    ```
    If it still doesn't work reboot your system.

That's it! Your containers are now up and you can continue to set up the settings in them. Please
take a look at [important notes](#important-notes) before you continue.

## Environment variables
All configuration lives in your `.env` file (copied from `.env.sample`). The most important
variables:

| Variable | Purpose |
|----------|---------|
| `TIMEZONE` | Timezone for all containers (e.g. `Europe/Amsterdam`). |
| `ROOT_DIR` | Absolute path where all configs and data are stored. **Must** start with `/` — see manual step 3. |
| `UID` | ID of the user Docker runs as, and the user for services without a dedicated user (Jellyfin, Tautulli, Seerr, Wizarr, rclone mount). Find it with `id -u`. |
| `MEDIACENTER_GID` | Shared group ID for all media services (default `13000`). |
| `PLEX_CLAIM` | Optional Plex claim token from https://www.plex.tv/claim/ (valid 4 minutes). |
| `REALDEBRID_TOKEN` | Real-Debrid API token for Zurg/RDTClient. Get it from https://real-debrid.com/apitoken. |
| `ZURG_MOUNT_PATH` | Host path where rclone mounts the Zurg filesystem (default `/mnt/zurg`). |
| `PLEX_URL` / `PLEX_TOKEN` | Plex address and token used by Zurg to trigger library updates (optional). |
| `ACME_EMAIL` | Email used by Traefik/Caddy to register Let's Encrypt certificates. |
| `IGDB_CLIENT_ID` / `IGDB_CLIENT_SECRET` | IGDB credentials for Romm game metadata (register at https://api.igdb.com). |
| `ROMM_AUTH_SECRET_KEY` | Secret used to sign Romm session tokens — generate with `openssl rand -hex 32`. |

Per-service user IDs (`SONARR_UID`, `RADARR_UID`, …) default to values in the `13001`–`13017`
range and generally don't need changing; adjust any that conflict with an existing user on your
system. See `.env.sample` for the complete, commented list.

## Important notes
- You probably shouldn't run the python script as root. Ideally you should create a brand new user that's just for these services, but any regular user will do.
  It will need your password for `sudo` to set up the permissions and folder structures, but you shouldn't run it *as* root.
- If you already used this script previously and want to clean up old users, run `remove_old_users.sh`.
  This is also recommended if you are updating from an earlier version of this script, since there were previously some conflicts in user IDs.
- It is recommended to restart your system after script completion, so that newly created users and groups can be loaded properly.
- When linking one service to another, remember to use the container name instead of `localhost`.
- Please set the settings of the -arr containers as soon as possible to the following (use
  advanced):
  - Media management:
    - Use hardlinks instead of Copy: `true`
    - Root folder: `/data/media/` and then tv, movies or music depending on service
  - qBittorrent ships with a default username `admin` and a one-time password that can be viewed by running `docker logs qbittorrent`.
  - Make sure to set a username and password for all servarr services and qBittorrent!
- In qBittorrent, after connecting it to the -arr services, you can indicate it should move
  torrents in certain categories to certain directories, like torrents in the `radarr` category
  to `/data/torrents/movies`. You should do this. Also set the `Default Save Path` to
  `/data/torrents`. Set "Run external program on torrent completion" to true and enter this in the
  field: `chmod -R 775 "%F/"`.
- You'll have to add indexers in Prowlarr by hand. Use Prowlarrs settings to connect it to the
  other -arr apps.

### IMPORTANT IF USING NFS SHARES
- NFS shares' permissions are mapped by user IDs. If you want to access a file as a client, your user ID needs to match the user ID of the owner (or group) of that file on the NFS server. 
Note that if you are a group member (and not the owner), having matching group IDs won't be enough, there also needs to be a corresponding user on the NFS server. The easiest way to make sure
the users and groups are set up on both sides correctly is to run `setup.sh` on both your NFS server and your client. 
On your server:
- Copy `.env` and `setup.sh` to your NFS server.
- You may have to adjust `.env` so that `ROOT_DIR` reflects where it will be stored on your server, which is most likely different from the mapped location on the client.
- Make sure that the `.env` file is not a .sample. Run `setup.sh`.
- Now follow all the same steps but on your client machine. Always double-check that `.env` is set correctly, especially `ROOT_DIR`.
You don't have to do this on your server first but it's recommended. If you are running this script on the client **make sure that you temporarily enable -no-root-squash on your NFS server**, 
as the script needs superuser privileges to run and by default on NFS the root user is mapped to nowhere to prevent abuse.
  
### SABnzbd External internet access denied message
When you're trying to access SABnzbd the first time you'll come across the message `External
internet access denied`. To fix this simple modify the `sabnzbd.ini` and change `inet_exposure` to
`4`, restart the docker container for sabnzbd (`docker restart sabnzbd`) and now you can access the
UI of SABnzbd (note: you may get a `Access denied - Hostname verification failed`, to fix this,
simply go to the IP of your server directly instead of the hostname). After accessing the UI don't
forget to set a username and password (https://sabnzbd.org/wiki/configuration/3.7/general,
section Security).

For more instructions or help see also https://sabnzbd.org/wiki/extra/access-denied.html on the
official SABnzbd website.

## FAQ

### How to update containers
There is an `update_containers.sh` script that takes care of this. Simply run it and it updates
all containers and removes old images. If you want to keep them, simply comment out the last line of the script.
It's essentially the following steps but automated:
If you'd like to it manually, go to the directory of your `docker-compose.yml` file
and run `(sudo) docker compose pull`. This pulls the newest versions of all images (blueprints for
containers) listed in the `docker-compose.yml` file. Then, you can run `(sudo) docker compose up
-d`. This will deploy the new versions without losing uptime. Afterwards, you can run `(sudo)
docker image prune` to remove the old images, freeing up space.

### Why do I need to set some settings myself, can that be added?
Some settings, particularly for the Servarr suite, are set in databases. While it *might* be
possible to interact with this database after creation, I'd rather not touch these. It's not
that difficult to set them yourself, and quite difficult to do it automatically. For other
containers, configuration files are automatically generated, so these are more easily edited,
but I currently don't believe this is worth the effort.

On top of the above, connecting the containers above would mean setting a password and creating an
API key for all of them. This would lead to everyone using Ezarr having the same API key and user/
password combination. Personally, I'd rather trust users to figure this out on their own rather
than trusting them to change these passwords and keys.

import getpass
import os
import pwd

class ContainerConfig:
    def __init__(self,
                 root_dir,
                 timezone,
                 plex_claim='',
                 realdebrid_token='',
                 zurg_mount_path='/mnt/zurg',
                 plex_url='http://plex:32400',
                 plex_token='',
                 use_zurg=False,
                 ):
        self.root_dir = root_dir
        self.timezone = timezone
        self.config_dir = f'{root_dir}/config'
        self.plex_claim = plex_claim
        self.realdebrid_token = realdebrid_token
        self.zurg_mount_path = zurg_mount_path
        self.plex_url = plex_url
        self.plex_token = plex_token
        self.use_zurg = use_zurg
        self.movie_dir = f'{root_dir}/media/movies'
        self.tv_dir = f'{root_dir}/media/tv'
        self.music_dir = f'{root_dir}/media/music'
        self.book_dir = f'{root_dir}/media/books'
        self.comic_dir = f'{root_dir}/media/comics'
        self.games_dir = f'{root_dir}/data/media/games'
        self.torrent_dir = f'{root_dir}/data/torrents'
        self.usenet_dir = f'{root_dir}/data/usenet'
        self.homarr_dir = f'{root_dir}/data/homarr/appdata'
        # Detected UID of the invoking user, used as the default fallback for
        # services that run as ${UID} in compose/*.yml (jellyfin, tautulli, seerr,
        # wizarr, homer, rclone mount). Defaults keep the generated file working
        # even without a .env, while still honouring it when present.
        self.UID = pwd.getpwnam(getpass.getuser()).pw_uid

    # === Media servers (compose/media-servers.yml) ===

    def plex(self):
        # Media server: streams your library to apps and devices, with optional hardware transcoding
        config = (
            '  plex:\n'
            '    image: lscr.io/linuxserver/plex:latest\n'
            '    container_name: plex\n'
            '    network_mode: host\n'
        )
        if self.use_zurg:
            config += (
                '    depends_on:\n'
                '      rclone:\n'
                '        condition: service_healthy\n'
            )
        config += (
            '    environment:\n'
            '      - PUID=${PLEX_UID:-13010}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - VERSION=docker\n'
            f'      - PLEX_CLAIM={self.plex_claim}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/plex-config:/config\n'
            f'      - {self.root_dir}/data/media:/media\n'
        )
        if self.use_zurg:
            config += f'      - {self.zurg_mount_path}:/zurg:rshared\n'
        config += '    restart: unless-stopped\n\n'
        return config

    def jellyfin(self):
        # Free, open-source media server (Plex alternative)
        config = (
            '  jellyfin:\n'
            '    image: lscr.io/linuxserver/jellyfin:latest\n'
            '    container_name: jellyfin\n'
        )
        if self.use_zurg:
            config += (
                '    depends_on:\n'
                '      rclone:\n'
                '        condition: service_healthy\n'
            )
        config += (
            '    environment:\n'
            f'      - PUID=${{UID:-{self.UID}}}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/jellyfin-config:/config\n'
            f'      - {self.root_dir}/data/media:/data\n'
        )
        if self.use_zurg:
            config += f'      - {self.zurg_mount_path}:/zurg:rshared\n'
        config += (
            '    ports:\n'
            '      - "8096:8096"\n'
            '    restart: unless-stopped\n\n'
        )
        return config

    def feishin(self):
        # Modern web/desktop music client for Jellyfin, Navidrome or Subsonic libraries
        return (
            '  feishin:\n'
            '    image: ghcr.io/jeffvli/feishin:latest\n'
            '    container_name: feishin\n'
            '    environment:\n'
            '      - SERVER_NAME=jellyfin\n'
            '      - SERVER_LOCK=true\n'
            '      - SERVER_TYPE=jellyfin\n'
            '      - SERVER_URL=jellyfin:8096\n'
            '    ports:\n'
            '      - "9180:9180"\n'
            '    restart: unless-stopped\n\n'
        )

    def romm(self):
        # ROM library manager: scan, browse and play your retro game collection with metadata and cover art
        return (
            '  romm:\n'
            '    image: rommapp/romm:latest\n'
            '    container_name: romm\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '      - IGDB_CLIENT_ID=${IGDB_CLIENT_ID}\n'
            '      - IGDB_CLIENT_SECRET=${IGDB_CLIENT_SECRET}\n'
            '      - ROMM_AUTH_SECRET_KEY=${ROMM_AUTH_SECRET_KEY}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/romm-config:/romm/config\n'
            f'      - {self.config_dir}/romm-config/database:/romm/database\n'
            f'      - {self.config_dir}/romm-config/resources:/romm/resources\n'
            f'      - {self.config_dir}/romm-config/logs:/romm/logs\n'
            f'      - {self.root_dir}/data/media/games:/romm/library\n'
            '    ports:\n'
            '      - "8083:8080"\n'
            '    restart: unless-stopped\n\n'
        )

    def gameyfin(self):
        # Game library frontend: scan a local games folder and serve a discovery interface with metadata
        return (
            '  gameyfin:\n'
            '    image: grimsi/gameyfin:latest\n'
            '    container_name: gameyfin\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '      - SPRING_DATASOURCE_URL=jdbc:h2:file:/gameyfin/data/gameyfin\n'
            '    volumes:\n'
            f'      - {self.config_dir}/gameyfin-config:/gameyfin/data\n'
            f'      - {self.root_dir}/data/media/games:/games:ro\n'
            '    ports:\n'
            '      - "8084:8080"\n'
            '    restart: unless-stopped\n\n'
        )

    def tautulli(self):
        # Monitoring and statistics dashboard for Plex viewing activity
        return (
            '  tautulli:\n'
            '    image: lscr.io/linuxserver/tautulli:latest\n'
            '    container_name: tautulli\n'
            '    environment:\n'
            '      # Tautulli does not recommend using non-default UID/GID.\n'
            '      # - PUID=${UID}\n'
            '      # - PGID=${MEDIACENTER_GID}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/tautulli-config:/config\n'
            '    ports:\n'
            '      - "8181:8181"\n'
            '    restart: unless-stopped\n\n'
        )

    # === Media management (compose/servarr.yml) ===

    def sonarr(self):
        # TV series manager: tracks, searches and organizes TV show downloads
        return (
            '  sonarr:\n'
            '    image: lscr.io/linuxserver/sonarr:latest\n'
            '    container_name: sonarr\n'
            '    environment:\n'
            '      - PUID=${SONARR_UID:-13001}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/sonarr-config:/config\n'
            f'      - {self.root_dir}/data:/data\n'
            '    ports:\n'
            '      - "8989:8989"\n'
            '    restart: unless-stopped\n\n'
        )

    def radarr(self):
        # Movie manager: tracks, searches and organizes movie downloads
        return (
            '  radarr:\n'
            '    image: lscr.io/linuxserver/radarr:latest\n'
            '    container_name: radarr\n'
            '    environment:\n'
            '      - PUID=${RADARR_UID:-13002}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/radarr-config:/config\n'
            f'      - {self.root_dir}/data:/data\n'
            '    ports:\n'
            '      - "7878:7878"\n'
            '    restart: unless-stopped\n\n'
        )

    def bazarr(self):
        # Subtitle manager companion for Sonarr/Radarr
        return (
            '  bazarr:\n'
            '    image: lscr.io/linuxserver/bazarr:latest\n'
            '    container_name: bazarr\n'
            '    environment:\n'
            '      - PUID=${BAZARR_UID:-13013}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/bazarr-config:/config\n'
            f'      - {self.root_dir}/data/media:/media\n'
            '    ports:\n'
            '      - "6767:6767"\n'
            '    restart: unless-stopped\n\n'
        )

    def lidarr(self):
        # Music manager: tracks, searches and organizes music album downloads
        return (
            '  lidarr:\n'
            '    image: lscr.io/linuxserver/lidarr:latest\n'
            '    container_name: lidarr\n'
            '    environment:\n'
            '      - PUID=${LIDARR_UID:-13003}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/lidarr-config:/config\n'
            f'      - {self.root_dir}/data:/data\n'
            '    ports:\n'
            '      - "8686:8686"\n'
            '    restart: unless-stopped\n\n'
        )

    def kapowarr(self):
        # Comic book library manager: searches, downloads and organizes digital comics (Mylar3 alternative)
        return (
            '  kapowarr:\n'
            '    container_name: kapowarr\n'
            '    image: mrcas/kapowarr:latest\n'
            '    environment:\n'
            '      - PUID=0\n'
            '      - PGID=0\n'
            '      - TZ=Etc/UTC\n'
            '    volumes:\n'
            f'      - {self.config_dir}/kapowarr-config:/app/db\n'
            f'      - {self.root_dir}/data:/data\n'
            '    ports:\n'
            '      - 5656:5656\n\n'
        )

    def questarr(self):
        # Video game manager for the *arr ecosystem
        return (
            '  questarr:\n'
            '    image: ghcr.io/doezer/questarr:latest\n'
            '    container_name: questarr\n'
            '    environment:\n'
            '      - SQLITE_DB_PATH=/app/data/sqlite.db\n'
            '    volumes:\n'
            f'      - {self.root_dir}/data:/data\n'
            '    ports:\n'
            '      - "5000:5000"\n'
            '    restart: unless-stopped\n\n'
        )

    def audiobookshelf(self):
        # Self-hosted audiobook and podcast server
        return (
            '  audiobookshelf:\n'
            '    image: ghcr.io/advplyr/audiobookshelf:latest\n'
            '    container_name: audiobookshelf\n'
            '    environment:\n'
            '      - user=${AUDIOBOOKSHELF_UID:-13014}:${MEDIACENTER_GID:-13000}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/audiobookshelf:/config\n'
            f'      - {self.root_dir}/data/media/audiobooks:/audiobooks\n'
            f'      - {self.root_dir}/data/media/podcasts:/podcasts\n'
            f'      - {self.root_dir}/data/media/audiobookshelf-metadata:/metadata\n'
            '    ports:\n'
            '      - "13378:80"\n'
            '    restart: unless-stopped\n\n'
        )

    # === Indexers (compose/indexers.yml) ===

    def prowlarr(self):
        # Indexer manager: centralizes and syncs torrent/usenet indexers across the *arr apps
        return (
            '  prowlarr:\n'
            '    image: lscr.io/linuxserver/prowlarr:develop\n'
            '    container_name: prowlarr\n'
            '    environment:\n'
            '      - PUID=${PROWLARR_UID:-13006}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/prowlarr-config:/config\n'
            '    ports:\n'
            '      - "9696:9696"\n'
            '    restart: unless-stopped\n\n'
        )

    def jackett(self):
        # Indexer proxy: translates torrent/usenet tracker searches into a unified API (Prowlarr alternative)
        return (
            '  jackett:\n'
            '    image: lscr.io/linuxserver/jackett:latest\n'
            '    container_name: jackett\n'
            '    environment:\n'
            '      - PUID=${JACKETT_UID:-13008}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/jackett-config:/config\n'
            '    ports:\n'
            '      - 9117:9117\n'
            '    restart: unless-stopped\n\n'
        )

    def flaresolverr(self):
        # Proxy that solves Cloudflare/DDoS-Guard challenges on behalf of indexers
        return (
            '  flaresolverr:\n'
            '    image: ghcr.io/flaresolverr/flaresolverr:latest\n'
            '    container_name: flaresolverr\n'
            '    environment:\n'
            '      - LOG_LEVEL=${LOG_LEVEL:-info}\n'
            '      - LOG_HTML=${LOG_HTML:-false}\n'
            '      - CAPTCHA_SOLVER=${CAPTCHA_SOLVER:-none}\n'
            f'      - TZ={self.timezone}\n'
            '    ports:\n'
            '      - "8191:8191"\n'
            '    restart: unless-stopped\n\n'
        )

    # === Requests & user management (compose/requests.yml) ===

    def seerr(self):
        # Request and media discovery manager for Plex/Jellyfin
        return (
            '  seerr:\n'
            '    image: ghcr.io/seerr-team/seerr:latest\n'
            '    container_name: seerr\n'
            '    environment:\n'
            '      # Seerr does not recommend using non-default UID/GID.\n'
            '      # - PUID=${UID}\n'
            '      # - PGID=${MEDIACENTER_GID}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/seerr-config:/app/config\n'
            '    ports:\n'
            '      - "5055:5055"\n'
            '    restart: unless-stopped\n\n'
        )

    def wizarr(self):
        # Invite and onboarding manager for Plex/Jellyfin/Emby users
        return (
            '  wizarr:\n'
            '    image: ghcr.io/wizarrrr/wizarr:latest\n'
            '    container_name: wizarr\n'
            '    environment:\n'
            '      # Wizarr does not recommend using non-default UID/GID.\n'
            '      # - PUID=${UID}\n'
            '      # - PGID=${MEDIACENTER_GID}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/wizarr-config:/data\n'
            '    ports:\n'
            '      - "5690:5690"\n'
            '    restart: unless-stopped\n\n'
        )

    # === Download clients (compose/download-clients.yml) ===

    def qbittorrent(self):
        # BitTorrent client with a web UI
        return (
            '  qbittorrent:\n'
            '    image: lscr.io/linuxserver/qbittorrent:latest\n'
            '    container_name: qbittorrent\n'
            '    environment:\n'
            '      - PUID=${QBITTORRENT_UID:-13007}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '      - WEBUI_PORT=8080\n'
            '    volumes:\n'
            f'      - {self.config_dir}/qbittorrent-config:/config\n'
            f'      - {self.torrent_dir}:/data/torrents\n'
            '    ports:\n'
            '      - "8080:8080"\n'
            '      - "6881:6881"\n'
            '      - "6881:6881/udp"\n'
            '    restart: unless-stopped\n\n'
        )

    def sabnzbd(self):
        # Usenet (NZB) download client
        return (
            '  sabnzbd:\n'
            '    image: lscr.io/linuxserver/sabnzbd:latest\n'
            '    container_name: sabnzbd\n'
            '    environment:\n'
            '      - PUID=${SABNZBD_UID:-13011}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            '      - UMASK=002\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/sabnzbd-config:/config\n'
            f'      - {self.usenet_dir}:/data/usenet\n'
            '    ports:\n'
            '      - "8081:8080"\n'
            '    restart: unless-stopped\n\n'
        )

    def rdtclient(self):
        # Web client to manage Real-Debrid torrents/downloads
        config = (
            '  rdtclient:\n'
            '    image: rogerfar/rdtclient:latest\n'
            '    container_name: rdtclient\n'
        )
        if self.use_zurg:
            config += (
                '    depends_on:\n'
                '      rclone:\n'
                '        condition: service_healthy\n'
            )
        config += (
            '    environment:\n'
            '      - PUID=${RDTCLIENT_UID:-13017}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/rdtclient-config:/data/db\n'
            f'      - {self.root_dir}/data/torrents:/data/downloads\n'
        )
        if self.use_zurg:
            config += f'      - {self.zurg_mount_path}:/zurg:rshared\n'
        config += (
            '    ports:\n'
            '      - "6500:6500"\n'
            '    restart: unless-stopped\n\n'
        )
        return config

    # === Debrid (compose/debrid.yml) ===

    def zurg(self):
        # Real-Debrid WebDAV server: exposes your debrid library as a mountable filesystem
        return (
            '  zurg:\n'
            '    image: ghcr.io/debridmediamanager/zurg-testing:latest\n'
            '    container_name: zurg\n'
            '    environment:\n'
            '      - PUID=${ZURG_UID:-13015}\n'
            '      - PGID=${MEDIACENTER_GID:-13000}\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/zurg-config/config.yml:/app/config.yml\n'
            f'      - {self.config_dir}/zurg-config/scripts/plex_update.sh:/app/plex_update.sh\n'
            '      - zurgdata:/app/data\n'
            '    ports:\n'
            '      - "9999:9999"\n'
            '    healthcheck:\n'
            '      test: ["CMD", "curl", "-f", "http://localhost:9999/dav/"]\n'
            '      interval: 30s\n'
            '      timeout: 10s\n'
            '      retries: 3\n'
            '      start_period: 10s\n'
            '    restart: unless-stopped\n\n'
        )

    def rclone(self):
        # Mounts the Zurg WebDAV share as a local filesystem so Plex/Jellyfin can read it
        return (
            '  rclone:\n'
            '    image: rclone/rclone:latest\n'
            '    container_name: rclone\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.zurg_mount_path}:/data:rshared\n'
            f'      - {self.config_dir}/rclone-config/rclone.rd.conf:/config/rclone/rclone.conf\n'
            '    cap_add:\n'
            '      - SYS_ADMIN\n'
            '    security_opt:\n'
            '      - apparmor:unconfined\n'
            '    devices:\n'
            '      - /dev/fuse:/dev/fuse:rwm\n'
            '    depends_on:\n'
            '      zurg:\n'
            '        condition: service_healthy\n'
            f'    command: "mount zurg: /data --uid ${{UID:-{self.UID}}} --gid ${{MEDIACENTER_GID:-13000}} --allow-other --allow-non-empty --dir-cache-time 10s --vfs-cache-mode full"\n'
            '    healthcheck:\n'
            '      test: ["CMD", "ls", "/data"]\n'
            '      interval: 30s\n'
            '      timeout: 10s\n'
            '      retries: 3\n'
            '      start_period: 15s\n'
            '    restart: unless-stopped\n\n'
        )

    # === Dashboard (compose/dashboard.yml) ===

    def homarr(self):
        # Customizable dashboard with Docker integration for all your services
        key = os.urandom(32).hex()  # 32 random bytes rendered as 64 hex characters
        return (
            '  homarr:\n'
            '    container_name: homarr\n'
            '    image: ghcr.io/homarr-labs/homarr:latest\n'
            '    environment:\n'
            f'      - SECRET_ENCRYPTION_KEY={key}\n'
            '    volumes:\n'
            '      - /var/run/docker.sock:/var/run/docker.sock\n'
            f'      - {self.homarr_dir}:/appdata\n'
            '    ports:\n'
            '      - "7575:7575"\n'
            '    restart: unless-stopped\n\n'
        )

    def homer(self):
        # Lightweight static dashboard configured via a single YAML file (Homarr alternative)
        return (
            '  homer:\n'
            '    container_name: homer\n'
            '    image: b4bz/homer:latest\n'
            f'    user: ${{UID:-{self.UID}}}:${{MEDIACENTER_GID:-13000}}\n'
            '    environment:\n'
            '      - INIT_ASSETS=1\n'
            '    volumes:\n'
            f'      - {self.config_dir}/homer-config:/www/assets\n'
            '    ports:\n'
            # 8080 is used by qbittorrent, so homer is mapped to 8082 on the host
            '      - 8082:8080\n'
            '    restart: unless-stopped\n\n'
        )

    # === Reverse proxy (compose/reverse-proxy.yml) — enable only ONE ===

    def traefik(self):
        # Dynamic reverse proxy with automatic Let's Encrypt and Docker-native service discovery
        return (
            '  traefik:\n'
            '    image: traefik:latest\n'
            '    container_name: traefik\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '    command:\n'
            '      - "--api.dashboard=true"\n'
            '      - "--providers.docker=true"\n'
            '      - "--providers.docker.exposedbydefault=false"\n'
            '      - "--entrypoints.web.address=:80"\n'
            '      - "--entrypoints.websecure.address=:443"\n'
            '      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"\n'
            '      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"\n'
            '      - "--certificatesresolvers.letsencrypt.acme.storage=/etc/traefik/acme.json"\n'
            '    volumes:\n'
            '      - /var/run/docker.sock:/var/run/docker.sock:ro\n'
            f'      - {self.config_dir}/traefik-config:/etc/traefik\n'
            '    ports:\n'
            '      - "80:80"\n'
            '      - "443:443"\n'
            '      - "8880:8080"\n'
            '    restart: unless-stopped\n\n'
        )

    def caddy(self):
        # File-driven reverse proxy with automatic HTTPS — configure via Caddyfile (Traefik alternative)
        return (
            '  caddy:\n'
            '    image: caddy:latest\n'
            '    container_name: caddy\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/caddy-config/Caddyfile:/etc/caddy/Caddyfile\n'
            f'      - {self.config_dir}/caddy-config/data:/data\n'
            f'      - {self.config_dir}/caddy-config/config:/config\n'
            '    ports:\n'
            '      - "80:80"\n'
            '      - "443:443"\n'
            '      - "443:443/udp"\n'
            '    restart: unless-stopped\n\n'
        )

    def nginx_proxy_manager(self):
        # Web UI for managing nginx reverse proxy rules and Let's Encrypt certificates (Traefik alternative)
        return (
            '  nginx-proxy-manager:\n'
            '    image: jc21/nginx-proxy-manager:latest\n'
            '    container_name: nginx-proxy-manager\n'
            '    environment:\n'
            f'      - TZ={self.timezone}\n'
            '    volumes:\n'
            f'      - {self.config_dir}/nginx-proxy-manager-config:/data\n'
            f'      - {self.config_dir}/nginx-proxy-manager-config/letsencrypt:/etc/letsencrypt\n'
            '    ports:\n'
            '      - "80:80"\n'
            '      - "443:443"\n'
            '      - "81:81"\n'
            '    restart: unless-stopped\n\n'
        )

    def zurg_volumes(self):
        """Returns the volumes section for zurg (to be added at the end of docker-compose)"""
        return (
            'volumes:\n'
            '  zurgdata:\n'
        )

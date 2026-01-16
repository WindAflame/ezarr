import os


class UserGroupSetup:
    def __init__(self, root_dir='/', zurg_mount_path='/mnt/zurg', realdebrid_token='', plex_url='http://plex:32400', plex_token=''):
        self.root_dir = root_dir
        self.zurg_mount_path = zurg_mount_path
        self.realdebrid_token = realdebrid_token
        self.plex_url = plex_url
        self.plex_token = plex_token
        os.system('sudo groupadd mediacenter -g 13000')
        os.system('sudo usermod -a -G mediacenter $USER')
        os.system(
            '/bin/bash -c "sudo mkdir -pv ' + self.root_dir + '/data/{media,usenet,torrents} -m 775'
            ' ; sudo chown $(id -u):mediacenter ' + self.root_dir + '/data'
            ' ; sudo chown $(id -u):mediacenter ' + self.root_dir + '/data/{media,usenet,torrents}"'
        )

    def create_config_dir(self, service_name):
        os.system(
            f'sudo mkdir -p {self.root_dir}/config/{service_name}-config -m 775' # -m 775 gives read/write access to the whole mediacenter group, change to 755 for only read
            f' ; sudo chown -R {service_name}:mediacenter {self.root_dir}/config/{service_name}-config'
            f' ; sudo chown $(id -u):mediacenter {self.root_dir}/config'
        )

    def sonarr(self):
        os.system(
            '/bin/bash -c "sudo useradd sonarr -u 13001'
            ' ; sudo mkdir -pv ' + self.root_dir + '/data/{media,usenet,torrents}/tv -m 775'
            ' ; sudo chown -R sonarr:mediacenter ' + self.root_dir + '/data/{media,usenet,torrents}/tv"'
        )
        self.create_config_dir('sonarr')
        os.system('sudo usermod -a -G mediacenter sonarr')

    def radarr(self):
        os.system(
            '/bin/bash -c "sudo useradd radarr -u 13002'
            ' ; sudo mkdir -pv ' + self.root_dir + '/data/{media,usenet,torrents}/movies -m 775'
            ' ; sudo chown -R radarr:mediacenter ' + self.root_dir + '/data/{media,usenet,torrents}/movies"'
        )
        self.create_config_dir('radarr')
        os.system('sudo usermod -a -G mediacenter radarr')

    def bazarr(self):
        os.system('/bin/bash -c "sudo useradd bazarr -u 13013"')
        self.create_config_dir('bazarr')
        os.system('sudo usermod -a -G mediacenter bazarr')

    def lidarr(self):
        os.system(
            '/bin/bash -c "sudo useradd lidarr -u 13003'
            ' ; sudo mkdir -pv ' + self.root_dir + '/data/{media,usenet,torrents}/music -m 775'
            ' ; sudo chown -R lidarr:mediacenter ' + self.root_dir + '/data/{media,usenet,torrents}/music"'
        )
        self.create_config_dir('lidarr')
        os.system('sudo usermod -a -G mediacenter lidarr')

    def mylar3(self):
        os.system(
            '/bin/bash -c "sudo useradd mylar -u 13005'
            ' ; sudo mkdir -pv ' + self.root_dir + '/data/{media,usenet,torrents}/comics -m 775'
            ' ; sudo chown -R mylar:mediacenter ' + self.root_dir + '/data/{media,usenet,torrents}/comics"'
        )
        self.create_config_dir('mylar')
        os.system('sudo usermod -a -G mediacenter mylar')

    def audiobookshelf(self):
        os.system(
            '/bin/bash -c "sudo useradd audiobookshelf -u 13014'
            ' ; sudo mkdir -pv ' + self.root_dir + '/data/media/{audiobooks,podcasts,audiobookshelf-metadata} -m 775'
            ' ; sudo chown -R audiobookshelf:mediacenter ' + self.root_dir + '/data/media/{audiobooks,podcasts,audiobookshelf-metadata}"'
        )
        self.create_config_dir('audiobookshelf')
        os.system('sudo usermod -a -G mediacenter audiobookshelf')

    def prowlarr(self):
        os.system('sudo useradd prowlarr -u 13006')
        self.create_config_dir('prowlarr')
        os.system('sudo usermod -a -G mediacenter prowlarr')

    def qbittorrent(self):
        os.system('sudo useradd qbittorrent -u 13007')
        os.system('sudo usermod -a -G mediacenter qbittorrent')

    def overseerr(self):
        os.system('sudo useradd overseerr -u 13009')
        self.create_config_dir('overseerr')
        os.system('sudo usermod -a -G mediacenter overseerr')

    def plex(self):
        os.system('sudo useradd plex -u 13010')
        self.create_config_dir('plex')
        os.system('sudo usermod -a -G mediacenter plex')

    def sabnzbd(self):
        os.system('sudo useradd sabnzbd -u 13011')
        self.create_config_dir('sabnzbd')
        os.system('sudo usermod -a -G mediacenter sabnzbd')

    def jellyseerr(self):
        os.system('sudo useradd jellyseerr -u 13012')
        self.create_config_dir('jellyseerr')
        os.system('sudo usermod -a -G mediacenter jellyseerr')
    
    def jackett(self):
        os.system('sudo useradd jackett -u 13008')
        self.create_config_dir('jackett')
        os.system('sudo usermod -a -G mediacenter jackett')

    def zurg(self):
        os.system('sudo useradd zurg -u 13015')
        os.system('sudo usermod -a -G mediacenter zurg')

        # Create zurg config directory
        config_dir = f'{self.root_dir}/config/zurg-config'
        os.system(f'sudo mkdir -p {config_dir} -m 775')
        os.system(f'sudo chown -R zurg:mediacenter {config_dir}')

        # Create zurg mount point
        os.system(f'sudo mkdir -p {self.zurg_mount_path} -m 775')
        os.system(f'sudo chown -R zurg:mediacenter {self.zurg_mount_path}')

        # Generate config.yml
        config_content = f'''zurg: v1
token: {self.realdebrid_token if self.realdebrid_token else 'YOUR_REALDEBRID_TOKEN'}
check_for_changes_every_secs: 10
enable_repair: true
auto_delete_rar_torrents: true
on_library_update: sh /app/config/plex_update.sh "$@"

directories:
  anime:
    group_order: 10
    group: media
    filters:
      - regex: /\\b[a-fA-F0-9]{{8}}\\b/
      - any_file_inside_regex: /\\b[a-fA-F0-9]{{8}}\\b/

  shows:
    group_order: 20
    group: media
    filters:
      - has_episodes: true

  movies:
    group_order: 30
    group: media
    only_show_the_biggest_file: true
    filters:
      - regex: /.*/
'''
        config_path = f'{config_dir}/config.yml'
        with open('/tmp/zurg_config.yml', 'w') as f:
            f.write(config_content)
        os.system(f'sudo mv /tmp/zurg_config.yml {config_path}')
        os.system(f'sudo chown zurg:mediacenter {config_path}')

        # Generate plex_update.sh
        plex_script = f'''#!/bin/bash
# PLEX PARTIAL SCAN script
# Triggered by zurg when library changes are detected

plex_url="{self.plex_url if self.plex_url else 'http://plex:32400'}"
token="{self.plex_token if self.plex_token else 'YOUR_PLEX_TOKEN'}"
zurg_mount="{self.zurg_mount_path}"

# Get the list of section IDs
section_ids=$(curl -sLX GET "$plex_url/library/sections" -H "X-Plex-Token: $token" | grep -oP 'key="\\K[^"]+' | head -20)

for arg in "$@"
do
    parsed_arg="${{arg//\\\\}}"
    modified_arg="$zurg_mount/$parsed_arg"
    echo "Detected update on: $arg"
    echo "Absolute path: $modified_arg"

    for section_id in $section_ids
    do
        echo "Refreshing section ID: $section_id"
        curl -G -H "X-Plex-Token: $token" --data-urlencode "path=$modified_arg" "$plex_url/library/sections/$section_id/refresh"
    done
done

echo "All updated sections refreshed"
'''
        script_path = f'{config_dir}/plex_update.sh'
        with open('/tmp/plex_update.sh', 'w') as f:
            f.write(plex_script)
        os.system(f'sudo mv /tmp/plex_update.sh {script_path}')
        os.system(f'sudo chmod +x {script_path}')
        os.system(f'sudo chown zurg:mediacenter {script_path}')

    def rclone(self):
        os.system('sudo useradd rclone -u 13016')
        os.system('sudo usermod -a -G mediacenter rclone')

        # Create rclone config directory
        config_dir = f'{self.root_dir}/config/rclone-config'
        os.system(f'sudo mkdir -p {config_dir} -m 775')
        os.system(f'sudo chown -R rclone:mediacenter {config_dir}')

        # Generate rclone.conf
        rclone_config = '''[zurg]
type = webdav
url = http://zurg:9999/dav
vendor = other
pacer_min_sleep = 0
'''
        config_path = f'{config_dir}/rclone.conf'
        with open('/tmp/rclone.conf', 'w') as f:
            f.write(rclone_config)
        os.system(f'sudo mv /tmp/rclone.conf {config_path}')
        os.system(f'sudo chown rclone:mediacenter {config_path}')

    def rdtclient(self):
        os.system('sudo useradd rdtclient -u 13017')
        os.system('sudo usermod -a -G mediacenter rdtclient')

        # Create rdtclient config directory
        config_dir = f'{self.root_dir}/config/rdtclient-config'
        os.system(f'sudo mkdir -p {config_dir} -m 775')
        os.system(f'sudo chown -R rdtclient:mediacenter {config_dir}')

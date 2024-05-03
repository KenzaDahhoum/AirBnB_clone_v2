#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers using do_deploy."""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['54.237.7.136', '54.85.9.73']  # IP addresses of web servers
env.user = 'ubuntu'  # Username on the web servers
env.key_filename = '~/.ssh/id_rsa'  # Private key for SSH

def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    # Check if the archive exists
    if not exists(archive_path):
        print(f"Archive '{archive_path}' does not exist")
        return False

    try:
        # Upload the archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/ directory
        archive_filename = archive_path.split('/')[-1]
        archive_folder = archive_filename.split('.')[0]
        release_path = f'/data/web_static/releases/{archive_folder}/'
        run(f'sudo mkdir -p {release_path}')
        run(f'sudo tar -xzf /tmp/{archive_filename} -C {release_path}')

        # Delete the uploaded archive
        run(f'sudo rm /tmp/{archive_filename}')

        # Delete the current symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of the code
        run(f'sudo ln -s {release_path} /data/web_static/current')

        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=<path_to_archive>")
        sys.exit(1)
    archive_path = sys.argv[1].split('=')[-1]
    do_deploy(archive_path)

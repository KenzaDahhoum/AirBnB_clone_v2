#!/usr/bin/python3
"""Fabric script to deploy archive to web servers using the function do_deploy."""

from fabric.api import env, run, put
from os.path import isfile

env.hosts = ['54.237.7.136', '54.85.9.73']  # IP addresses of web servers
env.user = 'ubuntu'  # Username on the web servers
env.key_filename = '~/.ssh/id_rsa'  # Private key for SSH

def do_deploy(archive_path):
    if not isfile(archive_path):
        print("Archive path does not exist")
        return False

    file_name = archive_path.split('/')[-1]
    base_name = file_name.split('.')[0]
    remote_tmp_path = f"/tmp/{file_name}"
    release_dir = f"/data/web_static/releases/{base_name}/"

    try:
        put(archive_path, remote_tmp_path)  # Upload the archive
        run(f"sudo mkdir -p {release_dir}")
        run(f"sudo tar -xzf {remote_tmp_path} -C {release_dir}")
        run(f"sudo rm {remote_tmp_path}")
        run(f"sudo mv {release_dir}web_static/* {release_dir}")
        run(f"sudo rm -rf {release_dir}web_static")
        run("sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {release_dir} /data/web_static/current")
        print("New version deployed successfully!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

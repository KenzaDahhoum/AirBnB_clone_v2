#!/usr/bin/python3
"""Fabric script to deploy archive to web servers"""

from fabric.api import *
from os.path import isfile

env.hosts = ['54.237.7.136', '54.85.9.73']
env.user = 'ubuntu'

def do_deploy(archive_path):
    if not isfile(archive_path):
        print("Archive path does not exist")
        return False

    # Extracting file names
    file_name = archive_path.split("/")[-1]
    no_ext = file_name.split(".")[0]
    
    # Remote paths
    remote_tmp_path = "/tmp/" + file_name
    release_dir = "/data/web_static/releases/" + no_ext + "/"

    try:
        # Upload the archive
        put(archive_path, remote_tmp_path)
        
        # Uncompress the archive to the folder on the web server
        run("mkdir -p " + release_dir)
        run("tar -xzf " + remote_tmp_path + " -C " + release_dir)
        
        # Delete the archive from the web server
        run("rm " + remote_tmp_path)
        
        # Move content to the parent directory
        run("mv " + release_dir + "web_static/* " + release_dir)
        
        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        
        # Create a new the symbolic link /data/web_static/current on the web server
        run("ln -s " + release_dir + " /data/web_static/current")
        
        print("New version deployed successfully!")
        return True
    except:
        print("Deployment failed")
        return False

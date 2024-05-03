#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
    ..an archive to your web servers, using the function do_deploy: """


from fabric.api import *
from os.path import exists

env.hosts = ['54.237.7.136', '54.85.9.73']  # IP addresses of your web servers
env.user = 'ubuntu'  # Username on the web servers
env.key_filename = '~/.ssh/id_rsa'  # Path to your SSH private key


def do_deploy(archive_path):
    """ distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False  # Returns False if the file at archive_path doesn't exist
    
    filename = archive_path.split('/')[-1]
    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}/".format(no_tgz))
        run("sudo tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("sudo rm {}".format(tmp))
        run("sudo mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("sudo rm -rf {}/web_static".format(no_tgz))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}/ /data/web_static/current".format(no_tgz))
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False

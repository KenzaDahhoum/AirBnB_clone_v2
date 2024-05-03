#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

# Define remote user and hosts
env.user = 'ubuntu'
env.hosts = ['54.237.7.136', '54.85.9.73']


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the directory versions if it doesn't exist
    local("mkdir -p versions")

    # Create archive name with timestamp
    date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(date_time)

    # Pack web_static into the archive_name.tgz inside versions folder
    command = "tar -cvzf {} web_static".format(archive_name)
    result = local(command)

    # Check if the archive has been successfully created and return its path
    if result.failed:
        return None
    return archive_name


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    # Upload the archive to the /tmp/ directory of the web server
    put(archive_path, '/tmp')

    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
    file_name = archive_path.split('/')[-1]
    folder_name = file_name.split('.')[0]
    run('sudo mkdir -p /data/web_static/releases/{}'.format(folder_name))
    run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, folder_name))

    # Delete the archive from the web server
    run('sudo rm /tmp/{}'.format(file_name))

    # Delete the symbolic link /data/web_static/current from the web server
    run('sudo rm -rf /data/web_static/current')

    # Create a new the symbolic link /data/web_static/current on the web server
    run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(folder_name))

    return True


def deploy():
    """
    Creates and distributes an archive to your web servers
    """
    # Call the do_pack() function and store the path of the created archive
    archive_path = do_pack()

    # Return False if no archive has been created
    if not archive_path:
        return False

    # Call the do_deploy(archive_path) function, using the new path of the new archive
    return do_deploy(archive_path)


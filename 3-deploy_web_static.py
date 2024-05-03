#!/usr/bin/python3
""" Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy: """


from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['54.237.7.136', '54.85.9.73']
env.user = 'ubuntu'  # Username on the web servers
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to your web servers
    """
    if exists(archive_path) is False:
        return False  # Returns False if the file at archive_path doesnt exist
    filename = archive_path.split('/')[-1]
    folder_name = filename.split('.')[0]
    release_path = f'/data/web_static/releases/{folder_name}/'
    tmp_path = f'/tmp/{filename}'

    try:
        put(archive_path, '/tmp/')
        run(f'sudo mkdir -p {release_path}')
        run(f'sudo tar -xzf {tmp_path} -C {release_path}')
        run(f'sudo rm {tmp_path}')

        # Create new symbolic link
        current_path = '/data/web_static/current'
        run(f'sudo rm -rf {current_path}')
        run(f'sudo ln -s {release_path} {current_path}')
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """ creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result

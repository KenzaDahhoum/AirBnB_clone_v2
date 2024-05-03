#!/usr/bin/python3

from fabric.api import local
from datetime import datetime


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

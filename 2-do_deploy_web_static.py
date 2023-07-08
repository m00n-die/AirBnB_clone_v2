#!/usr/bin/python3
# deploys archived web static
import os
from datetime import datetime
from fabric.api import env, local, put, run


env.hosts = ["54.237.84.19", "35.175.130.93"]
env.user = 'ubuntu'


def do_deploy(archive_path):
    """deploys static files to servers"""

    if not os.path.exists(archive_path):
        return False
    filename = os.path.basename(archive_path)
    dir_name = filename.replace(".tgz", "")
    dir_path = "/data/web_static/releases/{}/".format(dir_name)

    complete = False

    try:
        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(dir_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, dir_path))
        run("rm -rf /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(dir_path, dir_path))
        run("rm -rf {}web_static".format(dir_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dir_path))
        print('New version deployed!')
        complete = True

    except Exception as e:
        complete = False
    return complete

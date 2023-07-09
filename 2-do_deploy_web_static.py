#!/usr/bin/python3
# deploys archives to web server
import os
from datetime import datetime
from fabric.api import env, put, run, local


env.hosts = ["54.237.84.19", "35.175.130.93"]
env.user = 'ubuntu'


def do_pack():
    """creates an archive of web static files"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_date = datetime.now()
    out = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_date.year,
        cur_date.month,
        cur_date.day,
        cur_date.hour,
        cur_date.minute,
        cur_date.second
    )

    try:
        print("Packing web_static to {}".format(out))
        local("tar -cvzf {} web_static".format(out))
        out_size = os.stat(out).st_size
        print("web_static packed: {} -> {} Bytes".format(out, out_size))

    except Exception as e:
        return None


def do_deploy(archive_path):
    """deploys archive to web server"""
    if not os.path.exists(archive_path):
        return False
    filename = os.path.basename(archive_path)
    dir_name = filename.replace(".tgz", "")
    dir_path = "/data/web_static/releases/{}/".format(dir_name)

    complete = False

    try:
        put(archive_path, "/tmp/{}".format(filename))
        run("sudo mkdir -p {}".format(dir_path))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, dir_path))
        run("sudo rm -rf /tmp/{}".format(filename))
        run("sudo mv {}web_static/* {}".format(dir_path, dir_path))
        run("sudo rm -rf {}web_static".format(dir_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(dir_path))
        print('New version deployed!')
        complete = True

    except Exception as e:
        return False

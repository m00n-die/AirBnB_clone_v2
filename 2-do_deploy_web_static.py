#!/usr/bin/python3
# deploys archives to web server
import os
from datetime import datetime
from fabric.api import env, put, run, local


env.hosts = ["54.237.84.19", "35.175.130.93"]


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
    """deploys archives to web sever"""
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True

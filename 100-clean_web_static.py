#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ['54.237.84.19', '35.175.130.93']


def do_pack():
    """creates an archive"""
    cur_date = datetime.now()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(cur_date.year,
                                                         cur_date.month,
                                                         cur_date.day,
                                                         cur_date.hour,
                                                         cur_date.minute,
                                                         cur_date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


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


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)


def do_clean(number=0):
    """deletes out of date files"""
    arcs = os.listdir('versions/')
    arcs.sort(reverse=True)
    start = int(number)
    
    if not start:
        start += 1
    if start < len(arcs):
        arcs = arcs[start:]
    else:
        arcs = []
    for archive in arcs:
        os.unlink('versions/{}'.format(archive))
    cmd = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd))

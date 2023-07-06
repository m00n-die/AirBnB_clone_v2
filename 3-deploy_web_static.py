#!/usr/bin/python3
"""creates and distributes an archive"""
import os.path
from fabric.api import *
from datetime import datetime


env.hosts = ['54.237.84.19', '35.175.130.93']
env.user = 'ubuntu'


def do_pack():
    """creates an archive"""
    cur_date = datetime.now()
    out_dir = "versions/web_static_{}{}{}{}{}{}.tgz".format(cur_date.year,
                                                            cur_date.month,
                                                            cur_date.day,
                                                            cur_date.hour,
                                                            cur_date.minute,
                                                            cur_date.second)
    f os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(out_dir)).failed is True:
        return None
    return out_dir


def do_deploy(archive_path):
    """deploys static files to servers"""
    try:
        if not (path.exists(archive_path)):
            return False
        put(archive_path, '/tmp/')

        time = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'
            .format(time))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
            .format(time, time))
        run('sudo rm /tmp/web_static_{}.tgz'.format(time))
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(time, time))
        run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
            .format(time))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(time))
    except Exception as e:
        return False
    return True


def deploy():
    """deploys web satic"""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)

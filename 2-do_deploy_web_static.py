#!/usr/bin/python3
"""distributes an archive to your web servers"""
import os.path
from fabric.api import *


env.hosts = ['54.237.84.19', '35.175.130.93']
env.user = 'ubuntu'


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

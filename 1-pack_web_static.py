#!/usr/bin/python3
# a Fabric script that generates a .tgz archive
from fabric.api import local
from time import strftime
from datetime import date


def do_pack():
    """generates archive from the contents of the web_static"""
    cur_date = strftime("%Y%m%d%H%M%S")
    
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(cur_date))

        return "versions/web_static_{}.tgz".format(cur_date)

    except Exception as e:
        return None

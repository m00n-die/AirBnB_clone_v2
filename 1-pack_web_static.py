#!/usr/bin/python3
# a Fabric script that generates a .tgz archive
from fabric.api import local
from time import strftime
from datetime import date
import os


def do_pack():
    """generates archive from the contents of the web_static"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_date = strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz web_static/".format(cur_date)
    
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        tar_size = os.stat(filename).st_size
        print("web_static packed: {} -> {} Bytes".format(output, tar_size))
        return "versions/web_static_{}.tgz".format(cur_date)

    except Exception as e:
        return None

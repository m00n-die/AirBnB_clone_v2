#!/usr/bin/python3
"""script that creates an archive file"""
import os.path
from datetime import datetime
from fabric.api import local


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

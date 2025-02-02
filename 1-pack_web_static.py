#!/usr/bin/python3
"""deploys web static with fabric"""
import os
from datetime import datetime
from fabric.api import local


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

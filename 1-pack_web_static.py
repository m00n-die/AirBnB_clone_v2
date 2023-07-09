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
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )

    try:
        print("Packing web_static to {}".format(out))
        local("tar -cvzf {} web_static".format(out))
        out_size = os.stat(out).st_size
        print("web_static packed: {} -> {} Bytes".format(output, out_size))

    except Exception as e:
        return None

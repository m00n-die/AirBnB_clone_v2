#!/usr/bin/python3
# DEPLOYS ARCHIVE WITH FABRIC
import os
from datetime import datetime
from fabric.api import env, local, put, run


env.hosts = ["54.237.84.19", "35.175.130.93"]
env.user = 'ubuntu'


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
        run("mkdir -p {}".format(dir_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, dir_path))
        run("rm -rf /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(dir_path, dir_path))
        run("rm -rf {}web_static".format(dir_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dir_path))
        print('New version deployed!')
        complete = True

    except Exception as e:
        return False


def deploy():
    """deploys sarchive files to servers"""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False

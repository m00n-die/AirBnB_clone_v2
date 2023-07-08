#!/usr/bin/python3
# DEPLOYS ARCHIVE WITH FABRIC
import os
from datetime import datetime
from fabric.api import env, local, put, run


def deploy():
    """deploys sarchive files to servers"""

    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False

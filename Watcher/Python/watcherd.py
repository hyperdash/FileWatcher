#! /usr/local/bin/python
#-*- coding: utf-8 -*-

from __future__ import with_statement
import daemon.pidlockfile
from watcher import Watcher
import time
import logging
import sys

if __name__ == "__main__":
    logger = logging.getLogger("watcherd")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("watcherd.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    hdlrConsole = logging.StreamHandler(sys.stdout)
    hdlrConsole.setFormatter(formatter)
    logger.addHandler(hdlrConsole)
    logger.info("watcherd started")
    
    watcher = Watcher(logger)
    _count = 0
    pid = daemon.pidlockfile.TimeoutPIDLockFile("/tmp/watcherd.pid", 10)
    daemon_context = daemon.DaemonContext(pidfile=pid, files_preserve=[handler.stream])
    with daemon_context:
        while 1:
            _count+=1
            if _count%40 == 0:
                logger.info(_count)
            watcher.watch()
            time.sleep(15)
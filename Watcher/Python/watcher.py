#! /usr/local/bin/python
#-*- coding: utf-8 -*-

import yaml
import datetime
import time
import os
import sys
import logging
import traceback

class Watcher:
    
    def __init__(self, logger):
        self._logger = logger
        try:
            file = open('settings.yaml', 'r')
            str = file.read()
            str = str.decode('utf8')
            data = yaml.load(str)
            self._path = data['path']
            self._cmd = data['cmd']
        except:
            self._logger.error(traceback.format_exc())
        finally:
            file.close()
        d = datetime.datetime.today()
        self._lastwatch = time.mktime(d.timetuple())
    
    def watch(self):
        execute = False
        for path in self._path:
            if os.path.getmtime(path) > self._lastwatch:
                execute = True
                break
        if execute:
            for cmd in self._cmd:
                try:
                    os.system(cmd)
                except:
                    self._logger.error(traceback.format_exc())
        d = datetime.datetime.today()
        self._lastwatch = time.mktime(d.timetuple())

if __name__ == '__main__':
    logger = logging.getLogger("watcher")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("watcher.log")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    hdlrConsole = logging.StreamHandler(sys.stdout)
    hdlrConsole.setFormatter(formatter)
    logger.addHandler(hdlrConsole)
    logger.info("watcher started")
    
    watcher = Watcher(logger)
    watcher.watch()
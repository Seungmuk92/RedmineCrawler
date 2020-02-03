##################################################
## File: logger.py
## Auth: smoh
## Create: 20.02.03
## Desc: Customized logger for crawler.
##################################################

import logging
import time
import json
import datetime
import os

class Logger:
    def __init__(self, name, log_file):
        self.name = name
        self.log_file = log_file
        logging.basicConfig(level = logging.INFO, format = '%(message)s')
        self.logger = logging.getLogger(self.name)
        self.log_hadler = logging.FileHandler(self.log_file)
        self.logger.addHandler(self.log_hadler)
        return
    
    def log(self, event, value):
        log_obj = {
            'component': self.name,
            'dttm': str(datetime.datetime.now().isoformat()),
            'log': {
                'event': event,
                'desc': value
            }
        }
        self.logger.info(json.dumps(log_obj))
        return

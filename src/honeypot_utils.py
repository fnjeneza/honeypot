#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

import yaml
import logging
from logging.handlers import RotatingFileHandler

def _init_logger(log_file='/tmp/honeypot.log',log_level='debug'):
    logger = logging.getLogger('honeypot')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s %(module)s[%(process)d] : '
            +'%(levelname)s : %(message)s')


    file_handler = RotatingFileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    # add  handler
    logger.addHandler(file_handler)
    
    # stream logger
    sh = logging.StreamHandler()
    sh_fmt = logging.Formatter('line %(lineno)s -- %(funcName)s -- %(message)s')
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(sh_fmt)
    # add handler 
    logger.addHandler(sh)
    #return logger

def get_logger(name):
    """
    Get logging instance
    """
    if '.' in name:
        name = 'honeypot.%s' % name.rpartition('.')[-1]
    else: name = 'honeypot.inspector'

    return logging.getLogger(name)

class Config():
    def __init__(self):
        #TODO loading configuration
        with open('config.yaml') as config_file:
            configuration = yaml.load(config_file)

        self.db_uri = configuration['database']['uri']
        self.broker_interval = configuration['database']['check_interval']

        self.log_file = configuration['log']['file']
        self.log_level = configuration['log']['level']

        self.inspector_logfile = configuration['inspector']['logfile']
        self.inspector_regex = configuration['inspector']['regex']
        self.inspector_command = configuration['inspector']['command']
        self.inspector_bantime = configuration['inspector']['bantime']
        self.inspector_interval = configuration['inspector']['check_interval']

        _init_logger(self.log_file, self.log_level)

        #if (LOG_FILE and LOG_LEVEL):
        #    logger()


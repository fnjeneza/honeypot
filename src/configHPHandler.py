#!/usr/bin/python3
#-*-coding:utf-8*-*
__author__ = 'fnjeneza'

import logging
from logging.handlers import RotatingFileHandler
from os import path

"""
Gestion de  la configuration
"""


#chemin du dossier de logs par défaut, 
#peut être modifié dans la config
log_dir=""

#log
logger = logging.getLogger('HoneyPot')

def log_config(logger, log_dir):
    """
    charge le niveau, le formattage, les handlers
    """
    logger = logging.getLogger('HoneyPot')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

#    critic_handler = RotatingFileHandler(log_dir+'critic.log', 'a', 1000000, 1)
#    warn_handler = RotatingFileHandler(log_dir+'warn.log', 'a', 1000000, 1)
    info_handler = RotatingFileHandler(log_dir+'info.log', 'a', 1000000, 1)

#    critic_handler.setLevel(logging.CRITICAL)
#    warn_handler.setLevel(logging.WARNING)
    info_handler.setLevel(logging.DEBUG)

#    critic_handler.setFormatter(formatter)
#    warn_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

#    logger.addHandler(critic_handler)
#    logger.addHandler(warn_handler)
    logger.addHandler(info_handler)


######## charge les logs par défaut ####
log_config(logger, log_dir)

####################################
## Chargement de la configuration ##
####################################
config_file ="config/main.cfg" #config file
config={} # les paramètres de configuration
if path.exists(config_file):
    with open(config_file) as conf:
        nb_line=0
        for line in conf.readlines():
            nb_line+=1
            line = line.strip()
            if line=='' or line[0]=="#":
                continue
            
            line = line.split('=')
            if len(line)!=2:
                logger.critical("Configuration incorrecte ligne "+str(nb_line))
                logger.critical("Arrêt du programme")
                exit()

            config[line[0].strip()] = line[1].strip()

else:
    logger.critical('Fichier de configuration non trouvé')
    logger.critical('Arrêt du programme')
    exit()
    
## recharge le dossier des logs en fonction de la config
try:
    log_dir = config['log_dir']
    if log_dir!='':
        log_config(logger, log_dir)
except:
    pass

#logger.debug("hello world")
#logger.warn("this is a warning")
#logger.critical("ohhh! This is critical")

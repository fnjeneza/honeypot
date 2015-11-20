#!/usr/bin/python3
#-*-coding:utf-8*-*
__author__ = 'fnjeneza'

from os import path

"""
Configuration handler
"""

def load_configuration(config_file=None):
    """
    Load configuration

    @param config_file: Path to config file
    Raise exceptions if no config file is found
    or syntax is incorrect
    @return configs: configurations map {key:value}
    """
    if config_file is None:
        config_file ="config/main.conf"
        
    config={} # configuration parameters
    if path.exists(config_file):
        with open(config_file) as conf:
            nb_line=0
            for line in conf.readlines():
                nb_line+=1
                line = line.strip()
                if line=='' or line[0]=="#":
                    continue
                
                line = line.split()
                if len(line)!=2:
                    raise Exception("Incorrect syntax, line "+str(nb_line))

                config[line[0].strip()] = line[1].strip()

    else:
        raise Exception('Configuration file unfound')
    
    return configs

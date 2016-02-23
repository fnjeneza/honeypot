#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

from threading import Timer
from concurrent import futures
from ldap import LDAP
import yaml
import time
import datetime

from hphttp import handle_webspam
from db import DatabaseHandler
from scheduler import work_hour
from utils import  get_logger, Config
from inspector import supervisor

import sys

"""
Handle the honeypot service
This is the main module of the application
"""

logger = get_logger(__name__)

class _Honeypotd:
    def __init__(self):
        self.config =Config()
        self.db =  DatabaseHandler(self.config.db_name,
                self.config.db_user,
                self.config.db_password,
                self.config.db_host,
                self.config.db_port) 
    
    def _generate_and_send_info(self,url, uid):
        
        dbh = self.db #DatabaseHandler(self.db_uri) 
        
        # person info
        person = dbh.generatePersonInfo()
        logger.debug(person)
        logger.info('processing webspam form from %s' %(url,))
        
        code = None
        # handle the webspam
        try:
            tags = self.config.tags
            code = handle_webspam(url, person, tags)
        except Exception as e:
            code=e
            dbh.remove_url(uid)

        logger.info("%s - code returned %s" %(url,code,))
        if code not in [200,302,301]:
            logger.error("%s not handled" %(url,))

        else :
            logger.debug("saving generated info ")
            # save person info in db
            dbh.savePersonInfo(url,person)

            # change processed state
            dbh.update_processed_value(uid)

            # connect to LDAP
            logger.debug('Connection to LDAP')
            user = self.config.ldap_user
            password = self.config.ldap_password
            baseObject = self.config.ldap_baseObject
            host = self.config.ldap_host
            hp_ldap = LDAP(user, password, baseObject, host)
            cn = "%s %s" % (person['NCK'], person['NAM'])
            dn = 'cn='+cn+','+self.config.ldap_baseObject
            logger.debug("cn=%s" % cn)
            sn = person['NAM']
            mail = person['EML']
            userPassword = person['PWD']
            attrs = {'cn':cn, 'sn':sn, 'mail':mail,'userPassword':userPassword}
            logger.debug(attrs)
            # add info to LDAP
            added = hp_ldap.add(dn,attrs)
            logger.debug("ldap add action performed. %s" %added)


    def _check_broker(self):
        dbh = self.db #DatabaseHandler(self.db_uri) 
        broker_interval = self.config.broker_interval

        while True:
            #dbh = DatabaseHandler(db_uri) 
            # check if there is new urls in the broker
            urls = dbh.newUrl()
            if urls:
                for url,uid in urls:
                    logger.info("processing %s" % url)
                    # compute a date to handle it
                    schedule = work_hour()
                    #schedule = 2
                    logger.debug('%s scheduled at %s' % (url, schedule))
                    # add the schedule_date to the database
                    dbh.updateScheduleDate(uid,schedule)
                    # compute the waiting time
                    now = datetime.datetime.now()
                    wait_time = schedule-now
                    # wait time in seconds
                    wait_time = wait_time.total_seconds()
                    logger.debug('wait time %d' % wait_time)
                    # wait till time is over and send info to the spam webpage
                    Timer(wait_time,self._generate_and_send_info, args=(url,uid,)).start()

            time.sleep(broker_interval)

    def _check_inspector(self):
        """
        supervision of the log file
        """
        logger.info('start inspector')
        inspect_file = self.config.inspector_logfile
        logger.debug('log file to inspect "%s"' % inspect_file)
        regexfile = self.config.inspector_regex
        #db connection
        dh = self.db #DatabaseHandler(self.db_uri)
        #read the file
        with open(regexfile) as rf:
            regex = rf.read()

        last_check = dh.last_check()
        logger.info('last check %s' % last_check)
        inspector_interval = self.config.inspector_interval
        logger.debug('inspector interval %s' % inspector_interval)
        while True:
            logger.info("checking '%s'" % inspect_file)
            cmd = self.config.inspector_command
            # check the log
            ip_list = supervisor(inspect_file, regex, last_check, cmd)
            now = datetime.datetime.now()
            # last update
            dh.update_last_check(now)
            last_check = now
            # add banned address to db
            dh.add_ban_address(ip_list, now)
            logger.debug(ip_list)
            logger.debug("wait for next execution")
            time.sleep(inspector_interval)

    def main(self):
        
        with futures.ThreadPoolExecutor(2) as e:
            e.submit(self._check_broker)
            e.submit(self._check_inspector)

if __name__=='__main__':
    honeypot = _Honeypotd()
    honeypot.main()

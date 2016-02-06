#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

from threading import Timer
#from hp_httphandler import retrieve_form_fields, submit_form
from hp_httphandler import handle_webspam
from db import DatabaseHandler
from scheduler import work_hour
import yaml
import time
#import logging
#from logging.handlers import RotatingFileHandler
import sys
from honeypot_utils import  get_logger, Config
from concurrent import futures
import datetime
from inspector import supervisor


logger = get_logger(__name__)

class _Honeypotd:
    def __init__(self):
        self.config =Config()
        #uri to the db
        self.db_uri = self.config.db_uri
        self.db =  DatabaseHandler(self.db_uri) 
    
    def _send_generated_info(self,url):
        
        dbh = DatabaseHandler(self.db_uri) 
        # load tags
        with open('fields.yaml') as _tags:
            tags = yaml.load(_tags)
            logger.debug(tags)
            
        # person info
        person = dbh.generatePersonInfo()
        logger.debug(person)
        logger.info('processing webspam form from %s' %(url,))
        code = handle_webspam(url, person, tags)
        logger.info("%s - code returned %d" %(url,code,))
        if code not in [200,302,301]:
            logger.error("%s not handled" %(url,))

        else :
            # TODO finish savePersonInfo
            logger.info("saving generated info ")
            # savePersonInfo()
            pass

    def _check_broker(self):
        #dbh = DatabaseHandler(URI_DB) 
        # TODO is dbh well created
        dbh = DatabaseHandler(self.db_uri) 
        broker_interval = self.config.broker_interval

        while True:
            #dbh = DatabaseHandler(db_uri) 
            # check if there is new urls in the broker
            urls = dbh.newUrl()
            print(urls)
            #urls = ['https://cas.unicaen.fr/login?service=https%3A%2F%2Fwebmail.unicaen.fr%3A443%2Fpublic%2Fpreauth-unicaen-fr.jsp#1']
            # if there is new url(s)
            if urls:
                for url in urls:
                    logger.info("processing %s" % url)
                    # compute a date to handle it
                    schedule = work_hour()
                    schedule = 2
                    logger.debug('%s scheduled at %d' % (url, schedule))
                    # add the schedule_date to the database
                    dbh.updateScheduleDate(url,schedule)
                    # run the task at schedule date
                    # compute the waiting time
                    now = datetime.datetime.now().timestamp()
                    wait_time = schedule-now
                    logger.debug('wait time %d' % wait_time)
                    # wait till time is over and send info to the spam webpage
                    Timer(wait_time,self._send_generated_info, args=(url,)).start()
                    # TODO INFO handle a request

            time.sleep(broker_interval)

    def _check_inspector(self):
        """
        supervision of the log file
        """
        logger.info('start inspector')
        #dbh = DatabaseHandler(db_uri)
        inspect_file = self.config.inspector_logfile
        logger.debug('log file to inspect "%s"' % inspect_file)
        regexfile = self.config.inspector_regex
        #db connection
        dh = DatabaseHandler(self.db_uri)
        #read the file
        with open(regexfile) as rf:
            regex = rf.read()

        last_check = dh.last_check()
        last_check = datetime.datetime.fromtimestamp(last_check)
        logger.info('last check %s' % last_check)
        inspector_interval = self.config.inspector_interval
        logger.debug('inspector interval %s' % inspector_interval)
        while True:
            logger.info("checking '%s'" % inspect_file)
            # check the log
            ip_list = supervisor(inspect_file, regex, last_check)
            now = datetime.datetime.now()
            # last update
            dh.update_last_check(now.timestamp())
            last_check = now
            # add banned address to db
            dh.add_ban_address(ip_list, now)
            logger.debug("wait for next execution")
            time.sleep(inspector_interval)

    def main(self):
        
        with futures.ThreadPoolExecutor(1) as e:
            #e.submit(_check_broker, 'sql/honeypot.db')
            e.submit(self._check_inspector)

if __name__=='__main__':
    honeypot = _Honeypotd()
    #honeypot.main()
    honeypot._check_broker()

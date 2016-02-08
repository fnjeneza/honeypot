#!/usr/bin/python3

__author__ = 'fnjeneza'

import sqlite3 as sql
from random import randrange, gauss
from datetime import date, datetime
from honeypot_utils import get_logger

logger = get_logger(__name__)


class DatabaseHandler:
    def __init__(self, path, port=None, userId=None, passwd=None, pilote="sqlite3"):
        """
        path: path to the database
        port: port used by the database
        user: user login
        passwd: password 
        pilote: sqlite3, postgresql, mysql, mariadb
        """
        #connection to the base
        self.conn = sql.connect(path)
        #cursor
        self.cur = self.conn.cursor()
    
    def newUrl(self):
        """
        Checks if there is a new url added.
        return list of urls
        """
        logger.debug("check for new urls in the broker")
        self.cur.execute("""SELECT url FROM broker WHERE
                schedule_date is NULL""")
        return [url[0] for url in self.cur.fetchall()]

    def updateScheduleDate(self,url,schedule):
        """
        update the schedule date
        """
        self.cur.execute("UPDATE broker SET schedule_date=? WHERE url=?",
                (schedule,url,))
        self.conn.commit()

    def generatePersonInfo(self):
        """
        Generate person information (first name, last name, email, password)
        return  (cn, email, password)
        cn will be common name e.g: Jean Dupont
        """
        cur = self.cur

        # last_name
        cur.execute( "SELECT count(id) from last_name")
        length = cur.fetchone()[0]
        _id = randrange(length)+1
        cur.execute('SELECT lname from last_name WHERE id=?', (_id,))
        lname = cur.fetchone()[0]

        # first_name
        cur.execute( "SELECT count(id) from first_name")
        length = cur.fetchone()[0]
        _id = randrange(length)+1
        cur.execute('SELECT fname, gender from first_name WHERE id=?', (_id,))
        fname, gender = cur.fetchone()
        
        #common name
        cn = fname[0]+lname
        cn = cn.lower()

        # password
        cur.execute( "SELECT count(id) from password")
        length = cur.fetchone()[0]
        _id = randrange(length)+1
        cur.execute('SELECT passwd from password WHERE id=?', (_id,))
        password = cur.fetchone()[0]

        # mail
        email = lname.lower()+"."+fname.lower()+'@unicaen.fr'
        specialChar = {'é':'e','è':'e','ê':'e','ç':'c','à':'a','î':'i'}
        for char in specialChar:
            email = email.replace(char, specialChar[char])

        # birth date
        # gauss distribution
        # mean = 45*365*24*60*60  //45 years in seconds
        # sigma = 10*365*24*60*60 //10 years in seconds
        mean = 1419120000
        sigma = 315360000
        years = gauss(mean, sigma)
        # current timestamp in second
        now = datetime.now().timestamp()
        # compute birth
        birth = date.fromtimestamp(now-years).isoformat()

        return {'NAM':lname,
                'NCK':fname,
                'USR':cn,
                'EML':email,
                'PWD':password,
                'GEN':gender,
                'BIR':birth}

    def savePersonInfo(self, url, person):
        """
        save Person information in database
        cn: common name (e.g: Jean Dupont)
        email:
        password:2015-12-09 12:29:43
        """
        cur = self.cur
        conn = self.conn
        cn = fname[0]+lname
        cn = cn.lower()
        try:
            cur.execute("INSERT INTO person VALUES(?,?,?,?,?,?,?,?,datetime('now'))",
                    (person['USR'],
                        url,
                        person['NCK'],
                        person['NAM'],
                        person['EML'],
                        person['PWD'],
                        person['BIR'],
                        person['GEN']))
        except sql.IntegrityError:
            msg = '%s already exists' % cn
            logger.error(msg)
            #raise Exception(msg)

        conn.commit()

    def deletePersonInfo(self, fname, lname):
        """
        Delete a person from database
        fname: first name
        lname: last naem
        """
        cur = self.cur
        conn = self.conn

        cn = fname+' '+lname
        try:
            cur.execute("DELETE FROM person WHERE cn=?",(cn,))
        except:
            msg = '%s can not be deleted' % cn
            logger.error(msg)
            #raise Exception(msg)
        conn.commit()

    def saveForm(self,url, form):
        """
        Save form in database
        e.g:
        { 
            form:{
                'action':'www.test.fr/form.php',
                'method':'post'
            },
            element:{
                'firstname':'Jean',
                'lastname':'Dupont',
                'email':'jean.dupont@unicaen.fr',
                'passwd':'123456'
            }
        }
        """
        cur = self.cur
        conn = self.conn
        try:
            cur.execute("INSERT INTO form(url,form, modified) VALUES(?,?,datetime('now'))",
                    (url,str(form)))
        except:
            logger.error('saving form error')
        conn.commit()
    
    def update_last_check(self,check_time):
        """
        update last_check table
        """
        cur = self.cur
        conn = self.conn
        cur.execute("UPDATE last_check SET last_check=?",(check_time,))
        conn.commit()

    def last_check(self):
        """
        return last check date as timestamp
        """
        cur = self.cur
        cur.execute('SELECT last_check FROM last_check')
        lc = cur.fetchone()[0]
        return lc

    def add_ban_address(self,adrs, current):
        """
        add banned adress to db

        Arguments:
            adrs: adresse list or tuple
            current: now timestamp
        """
        #if adrs is empty
        if not adrs:
            return
        cur = self.cur
        conn = self.conn
        for adr in adrs:
            cur.execute('INSERT INTO ban_address VALUES(?,?)',(adr, current))
        conn.commit()

    def ban_address(self):
        """
        return all banned address
        """
        cur = self.cur
        cur.execute('SELECT ip from ban_address')
        adrs = cur.fetchall()
        return [adr[0] for adr in adrs]

#!/usr/bin/python3

__author__ = 'fnjeneza'

import sqlite3 as sql
import random

#connection to the base
conn = sql.connect('sql/honeypot.db')

cur = conn.cursor()


def generatePeopleInfo():
    """
    Generate people information (first name, last name, email, password)
    return  (cn, email, password)
    cn will be common name e.g: Jean Dupont
    """
    # last_name
    cur.execute( "SELECT count(id) from last_name")
    length = cur.fetchone()[0]
    _id = random.randrange(length)+1
    cur.execute('SELECT lname from last_name WHERE id=?', (_id,))
    lname = cur.fetchone()[0]

    # first_name
    cur.execute( "SELECT count(id) from first_name")
    length = cur.fetchone()[0]
    _id = random.randrange(length)+1
    cur.execute('SELECT fname from first_name WHERE id=?', (_id,))
    fname = cur.fetchone()[0]
    
    # password
    cur.execute( "SELECT count(id) from password")
    length = cur.fetchone()[0]
    _id = random.randrange(length)+1
    cur.execute('SELECT passwd from password WHERE id=?', (_id,))
    password = cur.fetchone()[0]

    # mail
    email = lname.lower()+"."+fname.lower()+'@unicaen.fr'
    specialChar = {'é':'e','è':'e','ê':'e','ç':'c','à':'a','î':'i'}
    for char in specialChar:
        email = email.replace(char, specialChar[char])

    return lname+' '+fname,email,password

def savePeopleInfo(cn,email,password):
    """
    save people information in database
    cn: common name (e.g: Jean Dupont)
    email:
    password:
    """
    try:
        cur.execute("INSERT INTO people VALUES(?,?,?,datetime('now'))",(cn,email,password))
    except sql.IntegrityError:
        raise Exception(cn+" already exists")

    conn.commit()

def saveForm(url, form):
    """
    Save form in database
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
    try:
        cur.execute("INSERT INTO form(url,form, modified) VALUES(?,?,datetime('now'))",
                (url,str(form)))
    except :
        pass

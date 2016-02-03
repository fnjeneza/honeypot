#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

import pytest
import datetime
from src.hp_httphandler import submit_form
from src.inspector import supervisor

@pytest.fixture()
def init_db():
    from src.db import DatabaseHandler
    db = DatabaseHandler('../src/sql/testhoneypot.db')
    return db

def test_submit_form():
    url = 'http://192.168.1.80:8000/hello'
    params={'email':'test@test.com',
            'pass':'123456'}
    out = submit_form(url,params)
    assert out == 501

def test_generate_person_info(init_db):
    db = init_db
    person = db.generatePersonInfo()
    for v in person:
        assert person[v]!=''

from src.hp_httphandler import retrieve_form_fields
def test_retrieve_form_fields():
    attr = retrieve_form_fields(("https://cas.unicaen.fr/login?"
    "service=https%3A%2F%2Fwebmail.unicaen.fr%3A443%2Fpublic"
    "%2Fpreauth-unicaen-fr.jsp"))
    print(attr)
    assert  not attr==""

def test_work_hour():
    import time
    from src.scheduler import work_hour
    ntime = time.time()
    schedule = work_hour()
    #schedule = schedule.timestamp()
    assert schedule > ntime

from src.ldap import LDAP
@pytest.fixture()
def init_ldap():
    baseObject = "ou=people,dc=honeypot,dc=com"
    user="cn=admin,dc=honeypot,dc=com"
    password = "ubuntu"
    host = "10.0.3.132"
    return LDAP(user,password,baseObject,host)


def test_ldap_exists(init_ldap ):
    ldap = init_ldap
    baseObject = "ou=people,dc=honeypot,dc=com"
    assert ldap.exists(baseObject, "dupont")

def test_ldap_add(init_ldap):
    ldap = init_ldap
    dn = "uid=med,ou=people,dc=honeypot,dc=com"
    attr = {'uid':'med',
            'cn':'med test',
            'sn':'test'}
    assert ldap.add(dn,attr)==True

def test_ldap_delete(init_ldap):
    ldap = init_ldap
    dn = "uid=med,ou=people,dc=honeypot,dc=com"
    assert ldap.delete(dn)==True

def test_supervisor():
    journal = 'files/log.test'
    with open('files/regex.filter') as reg:
        regex = reg.read()
    last_check = datetime.datetime(2015,1,1)
    ips = supervisor(journal, regex, last_check)
    tuple_ips = ('192.168.1.1','192.168.58.58')
    assert ips==tuple_ips

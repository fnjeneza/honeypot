#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

import pytest
from src.configHPHandler import load_configuration
from src.hp_httphandler import submit_form

def test_load_configuration():
    out = load_configuration()
    assert out == {'test':'test'}

def test_load_configuration_arg():
    out = load_configuration("files/main.config")
    assert out == {'test':'test'}
    
def test_submit_form():
    url = 'http://192.168.1.80:8000/hello'
    params={'email':'test@test.com',
            'pass':'123456'}
    out = submit_form(url,params)
    assert out == 501

from src.hp_httphandler import retrieve_input_attr
def test_retrieve_input_attr():
    attr = retrieve_input_attr(("https://cas.unicaen.fr/login?"
    "service=https%3A%2F%2Fwebmail.unicaen.fr%3A443%2Fpublic"
    "%2Fpreauth-unicaen-fr.jsp"))
    #print(attr)
    assert attr==""

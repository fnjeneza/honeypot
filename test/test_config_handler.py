#!/usr/bin/python3
#*-*Coding: UTF-8 *-*
__author__ = "fnjeneza"

import pytest
from src.configHPHandler import load_configuration

def test_load_configuration():
    out = load_configuration()
    assert out == {'test':'test'}

def test_load_configuration_arg():
    out = load_configuration("files/main.config")
    assert out == {'test':'test'}

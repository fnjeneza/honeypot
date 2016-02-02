#!/usr/bin/python3
#*-*coding: UTF-8 *-*
__author__ = "fnjeneza"

from urllib.request import urlopen
from html.parser import HTMLParser
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urlparse, urlencode

class _HPHTMLParser(HTMLParser):
    """
    Parse an html page
    """
    def __init__(self):
        HTMLParser.__init__(self)
        #check if <form> start
        self.__is_form_opened = False
        self.__inputtags={"form":None,
                "inputs":[]}

    def handle_starttag(self, tag, attrs):
        if tag=="form":
            attr_temp={}
            self.__is_form_opened = True
            attr_type = ["method", "action"]
            for attr in attrs:
                if attr[0] in attr_type:
                    attr_temp[attr[0]] = attr[1]
            self.__inputtags["form"]=attr_temp

        if tag == "input" and self.__is_form_opened:
            attr_temp={}
            attr_type=["type","name","value","placeholder"]
            for attr in attrs:
                if attr[0] in attr_type:
                    attr_temp[attr[0]]=attr[1]
            self.__inputtags["inputs"].append(attr_temp)
    
    def get_input_attr(self):
        """
        @return input_attrs:a map of attr and values
        """
        return self.__inputtags


    def handle_endtag(self, tag):
        if tag == "form":
            self.__is_form_opened = False


def retrieve_form_fields(url):
    """
    Retrieve list of input's attr inside a form
    
    <form>
        <input name='nom_utilisateur'>
        <input type='submit'>
    </form>

    Raise ValueError if url is incoherent

    @param html: html syntax
    @return inputs: map of <input, type, name, value>
    """
    # retrieve the url content
    page = urlopen(url)
    
    content_type = page.getheader('content-type')
    
    #check if it is a html page
    if not content_type.find("text/html")>=0:
        raise Exception('Not an html page')
    
    charset='' # encoding
    if content_type.find("charset")>=0:
        charset = content_type.split(";")[1]
        index = charset.find("=")+1
        charset = charset[index:]

    hp = _HPHTMLParser()
    url_content = page.read()

    # if encoding is given
    if charset!='':
        text = url_content.decode(charset)
    else:
        try:
            text = url_content.decode() # utf-8
        except UnicodeDecodeError:
            text = bytes_text.decode('latin-1')

    hp.feed(text)
    
    return hp.get_input_attr()

def submit_form(url, params, method = 'POST', userAgent=None):
    """
    submit the form with completed input
    """

    u = urlparse(url)
    scheme = u.scheme # http or https
    host = u.hostname
    port = None
    if u.port is not None:
        port = u.port
    path = u.path

    if userAgent==None:
        #default User Agent
        header = {'User-Agent':("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; "
        "rv:24.0) Gecko/20100101 Firefox/24.0)")}
    header["Content-Type"]="application/x-www-form-urlencoded"

    if(scheme.find("https")>=0):
        #connection
        conn = HTTPSConnection(host,port)
    else:
        conn = HTTPConnection(host,port)

    data = urlencode(params)

    req = conn.request(method, path, data, header) #request
    resp = conn.getresponse() #response
    code = resp.getcode() # returned code

    return code

def handle_webspam(url, person, tags):
    """
    1. retrieve all fields of a form
    2. feed all fields
    3  send a response 

    Args: 
        url: url
        person: information on a person
        tag: normalized correspondence of fields

    return: html code response
    """
    # retrieve fields
    form = retrieve_form_fields(url)

    action = form['form']['action']
    inputs = form['inputs']
    
    #parameters
    params={}

    for _input in inputs:
        field_name = _input['name']
        try:
            _tag = tags[field_name]
            params[field_name] = person[_tag]
        except KeyError:
            params[field_name] = _input['value']

    url = url+action
    print(url)
    code = submit_form(url, params)
    return code


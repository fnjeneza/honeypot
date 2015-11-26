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


def retrieve_input_attr(url):
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
    page = urlopen(url)
    
    content_type = page.getheader('content-type')
    
    if not content_type.find("text/html")>=0:
        raise Exception('Not an html page')
    
    charset='' # encoding
    if content_type.find("charset")>=0:
        charset = content_type.split(";")[1]
        index = charset.find("=")+1
        charset = charset[index:]

    hp = _HPHTMLParser()
    url_content = page.read()

    if charset!='':
        text = url_content.decode(charset)
    else:
        try:
            text = url_content.decode() # utf-8
        except UnicodeDecodeError:
            text = bytes_text.decode('latin-1')

    hp.feed(text)
    
    return hp.get_input_attr()

def submit_form(url, params, userAgent=None):
    """
    submit the form with completed input
    """

    u = urlparse(url)
    scheme = u.scheme # protocol http or https
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

    req = conn.request('POST', path, data, header) #request
    resp = conn.getresponse() #response
    code = resp.getcode() # returned code

    return code

#!/usr/bin/python3
#*-*coding: UTF-8 *-*
__author__ = "fnjeneza"

from urllib.request import urlopen
from html.parser import HTMLParser


class _HPHTMLParser(HTMLParser):
    """
    Parse an html page
    """
    def __init__(self):
        HTMLParser.__init__(self)
        #check if <form> start
        self.__is_form_opened = False
        self.__inputtags=[] 

    def handle_starttag(self, tag, attrs):
        if tag=="form":
            self.__is_form_opened = True

        if tag == "input" and self.__is_form_opened:
            attr_temp={}
            attr_type=["type","name","value","placeholder"]
            for attr in attrs:
                if attr[0] in attr_type:
                    attr_temp[attr[0]]=attr[1]
            self.__inputtags.append(attr_temp)
    
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

def submit_form():
    """
    submit the form with completed input
    """
    pass

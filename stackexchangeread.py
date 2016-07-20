#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import argparse
import contextlib
import os

global URL

def get_url():
    global URL
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    URL = args.url

def get_html():
    #ua = UserAgent()
    #ua.chrome
    req = urllib.request.Request(URL,
                                headers={'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) 
                                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2774.3 
                                Safari/537.36'''})
    with contextlib.closing(urllib.request.urlopen(req)) as f:
        return f.read().decode('utf-8');

def _remove_attrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    [s.extract() for s in soup('script')]
    title=soup.find('div', {'id':'question-header'}).h1.a.text
    # print (title)
    main=soup.find('div', {'id':'mainbar'})
    question = main.find('div', {'id':'question'}).table.tr.find('td', class_='postcell').\
    div.div
    # print (question)
    owner = main.find('div', {'id':'question'}).table.tr.find('td', class_='postcell').\
    find('table', class_='fw').tr.find('td', class_='owner').\
    div.find('div', class_="user-details").a.text
    # print (owner)
    comments = main.find('div', {'id':'question'}).table.findAll('tr')[2].findAll('td')[1].\
    find('div', class_='comments').table.tbody.tr.find('td', class_='comment-text').div.span.prettify()
    print (comments)


get_url()
html_doc = get_html()
#matches = get_matches(html_doc)
get_matches(html_doc)
#print_matches(matches)

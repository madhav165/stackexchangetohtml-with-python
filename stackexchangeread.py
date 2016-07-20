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
    req = urllib.request.Request(URL, \
      headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2774.3 Safari/537.36'})
    with contextlib.closing(urllib.request.urlopen(req)) as f:
        return f.read().decode('utf-8');

def _remove_attrs(soup):
    for tag in soup.findAll(True): 
        tag.attrs = {}
    return soup

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    title = soup.title.text
    [s.extract() for s in soup('script')]
    script_path = os.path.realpath(__file__)
    script_dir = os.path.split(script_path)[0]
    html_folder_path = os.path.join(script_dir, 'html')
    if (not os.path.exists(html_folder_path)):
        os.makedirs(html_folder_path)
    rel_path = 'html/'+title.replace('/','')+'.html'
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path ,'w')
    f.write('<!doctype html><html><head><title>'+title+'</title><meta author="stackexchange.com"></head><body>')
    f.write ('<h1>'+title+'</h1>')
    main=soup.find('div', {'id':'mainbar'})

    q_votes = main.find('div', {'id':'question'}).table.tr.find('td', class_='votecell').div.span.text
    f.write('<p><b>'+q_votes+' Votes - ')

    y = main.find('div', {'id':'question'}).table.tr.find('td', class_='postcell').\
    find('table', class_='fw').tr.findAll('td', class_='post-signature')
    for k in y:
      if k.div.find('div', class_='user-details').a is not None:
          if k.div.find('div', class_='user-action-time').a is not None:
            f.write(k.div.find('div', class_='user-action-time').a.find(recursive=False, text=True).strip() + ' by ')
            f.write(k.div.find('div', class_='user-details').a.text)
            f.write(' (Rep: '+k.div.find('div', class_='user-details').div.span.text+') - ')
          else:
            f.write(k.div.find('div', class_='user-action-time').find(recursive=False, text=True).strip() + ' by ')
            f.write(k.div.find('div', class_='user-details').a.text)
            f.write(' (Rep: '+k.div.find('div', class_='user-details').div.span.text+')')
    f.write('</b></p>')

    question = main.find('div', {'id':'question'}).table.tr.find('td', class_='postcell').\
    div.div
    f.write ('<p>'+str(question)+'</p>')
    
    comment_full = main.find('div', {'id':'question'}).table.findAll('tr')[2].findAll('td')[1].\
    find('div', class_='comments').table.tbody.findAll('tr')
    i = 1
    f.write('<blockquote>')
    for acomm in comment_full:
      if acomm.find('td', class_='comment-text') is not None:
        f.write('<p>'+str(i)+'. '+str(acomm.find('td', class_='comment-text').find('div', class_='comment-body').span))
        if acomm.find('td', class_='comment-actions') is not None:
          f.write(' - '+acomm.find('td', class_='comment-text').find('div', class_='comment-body').a.text + ' - ')
          f.write(acomm.find('td', class_='comment-actions').table.tr.find('td', class_='comment-score').span.text+' Votes</p>')
        else:
          f.write(' - '+acomm.find('td', class_='comment-text').find('div', class_='comment-body').a.text + '</p>')
        i += 1
    f.write('</blockquote>')

    #answers
    answers = main.find('div', {'id':'answers'})
    
    n_ans = int(answers.find('div', {'id':'answers-header'}).div.h2.span.text)
    f.write ('<h3>'+str(n_ans)+' Answers</h3>')
    ans = answers.findAll('div', class_='answer')

    for i, x in enumerate(ans):
      x = x.table
      q_votes = x.tr.find('td', class_='votecell').div.span.text
      f.write('<p><b>'+str(i+1)+') '+q_votes+' Votes - ')
      
      y = x.tr.find('td', class_='answercell').table.tr.findAll('td', class_='post-signature')
      for k in y:
        if k.div.find('div', class_='user-details').a is not None:
          if k.div.find('div', class_='user-action-time').a is not None:
            f.write(str(k.div.find('div', class_='user-action-time').a.find(recursive=False, text=True).strip()) + ' by ')
            f.write(k.div.find('div', class_='user-details').a.text)
            f.write(' (Rep: '+k.div.find('div', class_='user-details').div.span.text+') - ')
          else:
            f.write(str(k.div.find('div', class_='user-action-time').find(recursive=False, text=True).strip()) + ' by ')
            f.write(k.div.find('div', class_='user-details').a.text)
            f.write(' (Rep: '+k.div.find('div', class_='user-details').div.span.text+')')
      f.write('</b></p>')

      f.write ('<p>'+str(x.tr.find('td', class_='answercell').find('div', class_='post-text'))+'</p>')

      acomms = x.findAll('tr', recursive=False)[1].find('div', class_='comments').table.tbody.findAll('tr')
      i = 1
      f.write('<blockquote>')
      for acomm in acomms:
        if acomm.find('td', class_='comment-text') is not None:
          f.write('<p>'+str(i)+'. '+str(acomm.find('td', class_='comment-text').find('div', class_='comment-body').span))
          if acomm.find('td', class_='comment-actions') is not None:
            f.write(' - '+acomm.find('td', class_='comment-text').find('div', class_='comment-body').a.text + ' - ')
            f.write(acomm.find('td', class_='comment-actions').table.tr.find('td', class_='comment-score').span.text+' Votes</p>')
          else:
            f.write(' - '+acomm.find('td', class_='comment-text').find('div', class_='comment-body').a.text + '</p>')
          i += 1
      f.write('</blockquote>')
    f.write('</body></html>')
    f.close()


get_url()
html_doc = get_html()
print ('Connection established')
#matches = get_matches(html_doc)
get_matches(html_doc)
#print_matches(matches)

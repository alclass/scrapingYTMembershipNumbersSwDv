#!/usr/bin/python3
import json, os
import bs4

SUBSCRIBERS_NUMBER_HTMLCLASSNAME = 'yt-subscription-button-subscriber-count-branded-horizontal'
DATA_LOCALFOLDERNAME = 'data'

'''
<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
  title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span> 
'''
class YtVideoPagesTraversal:

  def __init__(self):
    self.files_w_abspath = []
    self.traverse()

  def traverse(self):
    self.get_abspathfiles_list()
    self.parse_htmls_on_data_folder()

  def get_abspathfiles_list(self):
    # look up data folder
    thisfolder_abspath = os.path.abspath('.') # this about this (either '.' or a configured folder)
    datafolder_abspath = os.path.join(thisfolder_abspath, DATA_LOCALFOLDERNAME)
    entries = os.listdir(datafolder_abspath)
    for entry in entries:
      entry_abspath = os.path.join(datafolder_abspath, entry)
      if os.path.isfile(entry_abspath):
        self.files_w_abspath.append(entry_abspath)
    # return files_w_abspath

  def parse_htmls_on_data_folder(self):
    for entry_abspath in self.files_w_abspath:
      filename = os.path.split(entry_abspath)[1]
      print('Parsing =>', filename)
      extlessname = os.path.splitext(filename)[0]
      content = open(entry_abspath).read()
      bsoup = bs4.BeautifulSoup(content, 'html.parser')
      # result, if found, is a bs4.element.Tag object
      result = bsoup.find('span', attrs={'class':SUBSCRIBERS_NUMBER_HTMLCLASSNAME})
      if result is None:
        print('Subscribers number not found for', extlessname)
        continue
      try:
        arialabel = result['aria-label']
        print (extlessname, 'has', arialabel)
      except IndexError:
        print('Subscribers number not found for', extlessname)

def process():
  YtVideoPagesTraversal()

if __name__ == '__main__':
  process()
#!/usr/bin/python3
import json, os
import bs4

fp = open('channelvideosytpages.json', 'r')
content = fp.read()
jsondictlist = json.loads(content)
nameurldict = {}

prefix = "https://www.youtube.com/"
sufix = "/videos"
def form_url(murl):
  return prefix + murl + sufix

for d in jsondictlist:
  nname = d['nname']
  murl  = d['murl']
  nameurldict[nname] = form_url(murl)
print(nameurldict)

'''
<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip" 
  title="433 mil" tabindex="0" aria-label="433 mil inscritos">433 mil</span> 
'''
# look up data folder
thisfolder_abspath = os.path.abspath('.')
datafolder_abspath = os.path.join(thisfolder_abspath, 'data')
entries = os.listdir(datafolder_abspath)
files_w_abspath = []
for entry in entries:
  entry_abspath = os.path.join(datafolder_abspath, entry)
  if os.path.isfile(entry_abspath):
    files_w_abspath.append(entry_abspath)

for entry_abspath in files_w_abspath:
  content = open(entry_abspath).read()
  bsoup = bs4.BeautifulSoup(content, 'html.parser')
  result = bsoup.find({'class':'yt-subscription-button-subscriber-count-branded-horizontal subscribed'})
  print(result)
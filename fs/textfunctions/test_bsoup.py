#!/usr/bin/python3
import bs4 # , datetime, json, os, string

t = '''
<html>
 <yt-formatted-string id="subscriber-count" class="style-scope ytd-c4-tabbed-header-renderer">
   365&nbsp;mil inscritos
 </yt-formatted-string>
</html>
'''
bsoup = bs4.BeautifulSoup(t, 'html.parser')
result = bsoup.find('yt-formatted-string', attrs={'id': 'subscriber-count'})
if result:
  print(result.text)
else:
  print('result is None', result)

t = '''
<span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip"
 title="194&nbsp;mil" tabindex="0" aria-label="194&nbsp;mil inscritos">
 194&nbsp;mil
 </span>
'''
bsoup = bs4.BeautifulSoup(t, 'html.parser')
result = bsoup.find('span', attrs={'class':'yt-subscription-button-subscriber-count-branded-horizontal'})
if result:
  print(result.text)
else:
  print('result is None', result)

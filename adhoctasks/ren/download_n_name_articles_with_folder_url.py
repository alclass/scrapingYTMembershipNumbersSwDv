#!/usr/bin/python3
'''
  This is a temporary script just to download and rename a group of newspaper articles.
  If it's possible to generalize this script, then move it to the user-bin folder,
    otherwise, move it to the downloaded articles folder as a reference.
'''
import os, requests

dir_abspath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/001_BRA_pol_newspapers/Bozo on Newspapers/Henry Bugalho artigos'
filename = 'z-carta-capital-links.url'
filepath = os.path.join(dir_abspath, filename)

def get_urls(filepath):
  lines = open(filepath).readlines()
  lines = map(lambda word:word.strip(' \r\n'), lines)
  n_of_downloads = 0; n_of_urls = 0
  for url in lines:
    if url.find('opiniao') > -1:
      n_of_urls += 1
      print(url)
      pp = url.split('/')
      pp = list(filter(lambda x: x != '', pp))
      article_filename = pp[-1] + '.html'
      article_abspath = os.path.join(dir_abspath, article_filename)
      if os.path.isfile(article_abspath):
        print ('File', article_filename)
        print ('  has already been downloaded to folder.')
        continue
      print('Downloading', article_filename)
      req = requests.get(url)
      n_of_downloads += 1
      print(n_of_downloads, 'Saving it as', article_abspath)
      fp = open(article_abspath, 'w', encoding='utf8')
      fp.write(req.text)
      fp.close()
  print( 'n_of_urls = %d; n_of_downloads = %d' %(n_of_urls, n_of_downloads) )

def process():
  get_urls(filepath)

if __name__ == '__main__':
  process()
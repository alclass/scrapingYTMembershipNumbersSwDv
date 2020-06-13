#!/usr/bin/python3
'''
=> This script is to correct a bug in "wget --convert-links"
  to replace string ".png.html" to ".png" correcting the related image link
=> It runs against html files in a directory.
=> It was used to correct wget-fetched The Flask Megatutorial blog.miguelgrinberg.com
'''
import os

base_abspath = '/home/dados/Books/Books (mostly epubs)/CompSci Bks/L CompLang Bks/P Languages (PHP, Processing etc) Bks/Python Bks/Web CompSi Py Bks/Web Frameworks Py Bks/Flask & PyJs Bks/Flask Bks/html Flask Bks/The Flask Megatutorial blog.miguelgrinberg.com 11Gb html Bk/post'

lambdaIsHtml = lambda word : word.endswith('.html')
htmls = os.listdir(base_abspath)
htmls = list(filter(lambdaIsHtml, htmls))

n_of_replaces = 0
def rename():
  global n_of_replaces
  for i, html in enumerate(htmls):
    seq = i+1
    print(seq, 'Replacing png.html to png in', html)
    fileabspath = os.path.join(base_abspath, html)
    fs = open(fileabspath, 'r', encoding='utf8')
    text = fs.read()
    fs.close()
    text = text.replace('.png.html', '.png')
    fs = open(fileabspath, 'w', encoding='utf8')
    fs.write(text)
    fs.close()
    n_of_replaces += 1

def process():
  rename()
  print ('n_of_replaces', n_of_replaces, 'total of files', len(htmls))

if __name__ == '__main__':
  process()
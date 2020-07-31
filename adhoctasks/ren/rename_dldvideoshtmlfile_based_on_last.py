#!/usr/bin/env python3
import os

baseabspath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020-05'
sourcenamereldir = '2020-05-24'
targetreldir = '2020-05-22'


sourcenameabspath = os.path.join(baseabspath, sourcenamereldir)
entries = os.listdir(sourcenameabspath)
sourcenames = []
for entry in entries:
  name = os.path.split(entry)[1]
  sourcenames.append(name)


targetabspath = os.path.join(baseabspath, targetreldir)
entries = os.listdir(targetabspath)
minlen = 50
for entry in entries:
  filename = os.path.split(entry)[1]
  name, ext = os.path.splitext(filename)
  print(name, ext)
  if ext != '.html':
    continue
  size = len(name)
  minlen = size if size < minlen else minlen
  print(name, minlen)


def find_counterpart(ptrunk):
  for sourcefilename in sourcenames:
    if sourcefilename.startswith(ptrunk):
      onewname = targetreldir + sourcefilename[10:]
      return onewname
  return None


rename_pair_list = []
for entry in entries:
  from_filename = os.path.split(entry)[1]
  trunk = from_filename[:minlen]
  trunk = sourcenamereldir + trunk[10:]
  newname = find_counterpart(trunk)
  if newname is None:
    continue
  print(from_filename, newname)
  rename_pair = (from_filename, newname)
  rename_pair_list.append(rename_pair)

count = 0
for rename_pair in rename_pair_list:
  from_filename, newname = rename_pair
  frompath = os.path.join(targetabspath, from_filename)
  topath = os.path.join(targetabspath, newname)
  if os.path.isfile(frompath) and not os.path.isfile(topath):
    print('rename: ', from_filename, 'TO', newname)
    os.rename(frompath, topath)
    count += 1
print('count', count)

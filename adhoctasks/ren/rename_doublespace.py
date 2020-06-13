#!/usr/bin/python3
import os
import fs.filefunctions.pathfunctions as pathfs

n_of_renames = 0;   total_checked = 0
def rename_filename_if_doublespace(filename, filepath, folderpath):
  global n_of_renames, total_checked
  _, ext = os.path.splitext(filename)
  ext = ext.lstrip('.')
  if ext not in ['htm', 'html']:
    return
  total_checked += 1
  print(total_checked, 'Checking for doublespace =>', filename)
  if filename.find('  ') > -1:
    newname = filename.replace('  ', ' ')
    newnamepath = os.path.join(folderpath, newname)
    n_of_renames += 1
    print (n_of_renames, ': renaming', filename, 'to', newname)
    os.rename(filepath, newnamepath)

def rename_in_level2(l2folderpath):
  entries = os.listdir(l2folderpath)
  print('L2 n of entries', len(entries))
  for filename in entries:
    filepath = os.path.join(l2folderpath, filename)
    if os.path.isfile(filepath):
      print(filepath, 'is file')
      rename_filename_if_doublespace(filename, filepath, l2folderpath)

def search_rename_in_level2(l1folderpath):
  entries = os.listdir(l1folderpath)
  print('L2 n of entries', len(entries))
  for entry in entries:
    l2folderpath = os.path.join(l1folderpath, entry)
    if os.path.isdir(l2folderpath):
      print(entry, 'is dir')
      rename_in_level2(l2folderpath)

def search_rename_in_level1():
  base_abspath = pathfs.get_ytvideo_htmlfiles_baseabsdir()
  entries = os.listdir(base_abspath)
  print('L1 n of entries', len(entries))
  for entry in entries:
    if len(entry) == len('yyyy-mm'):
      entrypath = os.path.join(base_abspath, entry)
      print (entrypath)
      if os.path.isdir(entrypath):
        print('Entry:', entry, 'is dir: going to rename_in_dir(entrypath)')
        search_rename_in_level2(entrypath)

def process():
  search_rename_in_level1()
  print ('n_of_renames', n_of_renames, 'total_checked', total_checked)

if __name__ == '__main__':
  process()
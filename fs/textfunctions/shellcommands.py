#!/usr/bin/env python3
"""
"""
import os

YOUTUBEDL_VIDEOGET_COMM_INTERPOL = 'youtube-dl -w -f 18 %s'


def issue_youtubedl_videoget_comm(url):
  comm = YOUTUBEDL_VIDEOGET_COMM_INTERPOL % url
  print(comm)
  ans = input('Is command above okay? (Y/n) ')
  if ans in ['Y', 'y', '']:
    os.system(comm)
  return


def process():
  pass


if __name__ == '__main__':
  process()

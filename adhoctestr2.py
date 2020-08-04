#!/usr/bin/env python3
"""
"""
# import datetime
import logging
import os
import config

logfilepath = os.path.join(config.get_logfolder_abspath(), __file__+'.log')
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def adtest():
  logger.info('adtest() Started')
  pass
  logger.debug('adtest() Finished')
  adtest2()


def adtest2():
  logger.info('adtest() Started')
  pass
  logger.debug('adtest() Finished')


def process():
  adtest()


if __name__ == '__main__':
  process()

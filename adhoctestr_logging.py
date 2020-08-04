#!/usr/bin/env python3
"""
"""
# import datetime
import logging
import os
import config
import adhoctestr2

logfilepath = os.path.join(config.get_logfolder_abspath(), __file__+'.log')
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def funct1():
  logger.info('funct1 Started')
  pass
  logger.info('funct1 Finished')
  adhoctestr2.adtest()


def process():
  log_msg = 'process() hi hi hello'
  # logger.addHandler(loghandler)
  logger.info(log_msg)
  log_msg = 'process() debug msg'
  logger.debug(log_msg)
  log_msg = 'process() error msg'
  logger.error(log_msg)
  funct1()


if __name__ == '__main__':
  process()

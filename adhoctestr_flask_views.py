#!/usr/bin/env python3
"""
"""
# import datetime
import logging
import os
import requests
import config
import flaskapp.views as vws
import flaskapp as fa

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


def adhoc_test_via_flaskview():
  # fapp = fa.create()
  # ac = fa.app.app_context()
  flaskcnf = config.FlaskConfig
  flaskcnf.SQLALCHEMY_DATABASE_URI = config.get_engine_line_sa_uri()
  flaskcnf.SQLALCHEMY_BINDS = 1
  fapp = fa.app
  fapp.config.from_object(flaskcnf)
  fapp.app_context()
  with fapp:
    ytchannelid = 'ueduardoamoreira'
    res = vws.ytchannel_summary(ytchannelid)
    print(res)


def adhoc_test_via_http():
  ytchannelid = 'ueduardoamoreira'
  url = 'http://127.0.0.1:5000/channel/' + ytchannelid
  res = requests.get(url)
  text = res.text
  text = text if len(text) < 200 else text[:200]
  print(text)


def process():
  adhoc_test_via_http()


if __name__ == '__main__':
  process()

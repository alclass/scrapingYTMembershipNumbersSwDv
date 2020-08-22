#!/usr/bin/env python3
"""
"""
import datetime
import logging
import os
import sys
# from sqlalchemy.sql.expression import desc
import config
# import fs.textfunctions.shellcommands as shell
import models.sa_models.ytchannelsubscribers_samodels as sam
# import models.gen_models.YtVideosPageMod as ytvpM
import fs.db.sqlalchdb.sqlalchemy_conn as con
# import dld_videopages_for_channels_on_db_n_scrape as dldmod
# from models.scrapers import drill_down_json as drill

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_channel_from_args_with_open_session(session, confirm_msg_to_interpolate=None):
  if len(sys.argv) < 2:
    print('''
    ================ Missing Parameter ================ 
    Please, enter a nname or part of it to download a ytchannel.
    ================ ================  ================ 
    ''')
    _ = input('Press any key and/or [ENTER] ')
    return None
  likename = sys.argv[1]
  nminutes = 20
  try:
    nminutes = int(sys.argv[2])
  except IndexError:
    pass
  except ValueError:
    pass
  ytchannel = session.query(sam.YTChannelSA).filter(sam.YTChannelSA.nname.contains("%" + likename + "%")).first()
  if confirm_msg_to_interpolate is not None:
    confirm_msg = confirm_msg_to_interpolate % ytchannel.nname
    confirm_msg += ' nminutes = %d ' % nminutes
    ans = input(confirm_msg)
    if ans not in ['', 'Y', 'y']:
      return None
  return ytchannel, nminutes


def process_fetch():
  session = con.Session()
  confirm_msg_to_interpolate = None
  ytchannel, nminutes = get_channel_from_args_with_open_session(session, confirm_msg_to_interpolate)
  print('ytchannel', ytchannel)
  for i, vitem in enumerate(ytchannel.vinfolist):
    if vitem.duration_in_sec and vitem.duration_in_sec < nminutes*60+1:
      print(vitem.ytvideoid, i+1, vitem.duration_in_hms, vitem.title)
  session.close()


def process():
  process_fetch()


if __name__ == '__main__':
  process()

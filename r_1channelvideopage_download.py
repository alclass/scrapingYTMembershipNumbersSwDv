#!/usr/bin/env python3
"""
"""
import datetime
import logging
import os
import sys
import config
import models.sa_models.ytchannelsubscribers_samodels as sam
import models.gen_models.YtVideosPageMod as ytvpmod
import fs.db.sqlalchdb.sqlalchemy_conn as con
import r_download_channelsvideopage as dldmod
import drill_down_json as drill

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_channel_from_args():
  if len(sys.argv) < 2:
    print('''
    ================ Missing Parameter ================ 
    Please, enter a nname or part of it to download a ytchannel.
    ================ ================  ================ 
    ''')
    sys.exit(1)
  likename = sys.argv[1]
  session = con.Session()
  ytchannel = session.query(sam.YTChannelSA).filter(sam.YTChannelSA.nname.contains("%" + likename + "%")).first()
  confirm_msg = 'Download channel %s ? (Y/n) ' % ytchannel.nname
  ans = input(confirm_msg)
  if ans not in ['', 'Y', 'y']:
    return None
  return ytchannel


def process():
  ytchannel = get_channel_from_args()
  ytvideopage = ytvpmod.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  text = dldmod.download_save_n_retrieve_text(ytvideopage, delete_before_dld=True)
  drill.extract_subscribers_from_htmltext(text, ytvideopage)
  drill.extract_vitems_from_htmltext(text, ytvideopage)



if __name__ == '__main__':
  process()

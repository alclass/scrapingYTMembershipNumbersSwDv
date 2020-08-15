#!/usr/bin/env python3
"""
"""
import datetime
import logging
import os
import sys
from sqlalchemy.sql.expression import desc
import config
import fs.textfunctions.shellcommands as shell
import models.sa_models.ytchannelsubscribers_samodels as sam
import models.gen_models.YtVideosPageMod as ytvpM
import fs.db.sqlalchdb.sqlalchemy_conn as con
import dld_videopages_for_channels_on_db_n_scrape as dldmod
from models.scrapers import drill_down_json as drill

_, logfilename = os.path.split(__file__)
logfilename = str(datetime.date.today()) + '_' + logfilename[:-3] + '.log'
logfilepath = os.path.join(config.get_logfolder_abspath(), logfilename)
logging.basicConfig(filename=logfilepath, filemode='w', format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_channel_from_args(confirm_msg_to_interpolate=None):
  if len(sys.argv) < 2:
    print('''
    ================ Missing Parameter ================ 
    Please, enter a nname or part of it to download a ytchannel.
    ================ ================  ================ 
    ''')
    ans = input('Press any key and/or [ENTER] ')
    return None
  likename = sys.argv[1]
  session = con.Session()
  ytchannel = session.query(sam.YTChannelSA).filter(sam.YTChannelSA.nname.contains("%" + likename + "%")).first()
  session.close()
  if confirm_msg_to_interpolate is not None:
    confirm_msg = confirm_msg_to_interpolate % ytchannel.nname
    ans = input(confirm_msg)
    if ans not in ['', 'Y', 'y']:
      return None
  return ytchannel


def get_most_recent_video_for(ytchannel):
  session = con.Session()
  vinfo = session.query(sam.YTVideoItemInfoSA). \
      filter(sam.YTVideoItemInfoSA.ytchannelid == ytchannel.ytchannelid).\
      order_by(desc(sam.YTVideoItemInfoSA.publishdatetime)).\
      first()
  session.close()
  return vinfo


def download_scrape_n_dbsave(ytvideopage):
  text = dldmod.download_save_n_retrieve_text(ytvideopage, delete_before_dld=True)
  drill.extract_subscribers_from_htmltext(text, ytvideopage)
  drill.extract_vitems_from_htmltext(text, ytvideopage)


def process():
  confirm_msg_to_interpolate = 'Download channel %s ? (Y/n) '  # % ytchannel.nname
  ytchannel = get_channel_from_args(confirm_msg_to_interpolate)
  ytvideopage = ytvpM.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  vinfo_before = get_most_recent_video_for(ytchannel)
  download_scrape_n_dbsave(ytvideopage)
  vinfo_after = get_most_recent_video_for(ytchannel)
  print('='*30)
  print(ytchannel.nname, 'most_recent_video', vinfo_before)
  print('-'*30)
  print('Refetched most_recent_video', vinfo_after)
  ans = input('Do you want to download that? (Y/n) ')
  if ans in ['Y', 'y', '']:
    url = vinfo_after.form_video_url()
    shell.issue_youtubedl_videoget_comm(url)
  return


if __name__ == '__main__':
  process()

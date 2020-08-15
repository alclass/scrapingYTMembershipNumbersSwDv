#!/usr/bin/env python3
"""
"""
import models.sa_models.ytchannelsubscribers_samodels as sam
import models.gen_models.YtVideosPageMod as ytvpM
import fs.db.sqlalchdb.sqlalchemy_conn as con
from models.scrapers import drill_down_json as drill
import dld_1channelvideopage_n_scrape as dld1


def show(ytvideopage):
  htmltext = ytvideopage.get_html_text()
  viscrapers = drill.extract_vitems_from_htmltext_nondb(htmltext, ytvideopage)
  for viscraper in viscrapers:
    print(viscraper)


DEFAULT_LIKENAME_FOR_CHANNEL_FIND = "%plantão br%"


def process():
  """
    filepath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020/2020-08' \
                '/2020-08-13/2020-08-13 Plantão Br [cUC3-JLGJpMKwymQoRFJMkgSg].html'
    text = open(filepath, encoding='utf8').read()

  :return:
  """
  ytchannel = dld1.get_channel_from_args()
  if ytchannel is None:
    sess = con.Session()
    ytchannel = sess.query(sam.YTChannelSA).\
        filter(sam.YTChannelSA.nname.like(DEFAULT_LIKENAME_FOR_CHANNEL_FIND)).first()
    sess.close()
  ytvideopage = ytvpM.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  show(ytvideopage)


if __name__ == '__main__':
  process()

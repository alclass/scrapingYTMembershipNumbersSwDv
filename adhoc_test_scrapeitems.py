#!/usr/bin/env python3
"""
"""
import models.sa_models.ytchannelsubscribers_samodels as sam
import models.gen_models.YtVideosPageMod as ytvpM
import fs.db.sqlalchdb.sqlalchemy_conn as con
import drill_down_json as drill


def show(ytvideopage):
  entry_abspath = ytvideopage.datedpage_filepath
  htmltext = ytvideopage.get_html_text()
  viscrapers = drill.extract_vitems_from_htmltext_nondb(htmltext, ytvideopage)
  for viscraper in viscrapers:
    print(viscraper)


def process():
  """
    filepath = '/media/friend/SAMSUNG/Ytvideos BRA Politics/z Other ytchannels/000_scrape_ytdata/2020/2020-08' \
                '/2020-08-13/2020-08-13 Plantão Br [cUC3-JLGJpMKwymQoRFJMkgSg].html'
    text = open(filepath, encoding='utf8').read()

  :return:
  """
  sess = con.Session()
  ytchannel = sess.query(sam.YTChannelSA).filter(sam.YTChannelSA.nname.like("%plantão br%")).first()
  ytvideopage = ytvpM.YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  show(ytvideopage)


if __name__ == '__main__':
  process()
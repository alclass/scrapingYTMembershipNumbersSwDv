#!/usr/bin/env python3
from sqlalchemy.orm import sessionmaker
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.sa_models.ytchannelsubscribers_samodels import YTChannelSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
Session = sessionmaker(bind=sqlalchemy_engine)


class YtChannelVideosAndItsViews:

  def __init__(self, ytchannel, tuplelist_vinfos_n_vviews):
    self.ytchannel = ytchannel
    self.vvideos_views_dict = {}
    self.tuplelistsize = 0
    self.set_views_per_video(tuplelist_vinfos_n_vviews)  # type 'list_reverseiterator'
    self.make_views_pngs()
    # self.tuplelist_vinfo_n_vviews =

  def set_views_per_video(self, tuplelist_vinfos_n_vviews):
    for tuple_vinfo_n_vview in tuplelist_vinfos_n_vviews:
      vinfo = tuple_vinfo_n_vview[0]
      self.tuplelistsize += 1
      if vinfo.ytvideoid in self.vvideos_views_dict.keys():
        tuplelist = self.vvideos_views_dict[vinfo.ytvideoid]
        tuplelist.append(tuple_vinfo_n_vview)
      else:
        self.vvideos_views_dict[vinfo.ytvideoid] = [tuple_vinfo_n_vview]

  def make_views_pngs_for_videoid(self, ytvideoid):
    tuplelist_vinfos_n_vviews = self.vvideos_views_dict[ytvideoid]
    vinfo = tuplelist_vinfos_n_vviews[0][0]
    vviewsobjlist = list(map(lambda t: t[1], tuplelist_vinfos_n_vviews))
    viewslist = list(map(lambda o: o.views, vviewsobjlist))
    dateslist = list(map(lambda o: o.infodate, vviewsobjlist))
    return vinfo, viewslist, dateslist

  def make_views_pngs(self):
    # videodict = {}
    for i, ytvideoid in enumerate(self.vvideos_views_dict):
      vinfo, viewslist, dateslist = self.make_views_pngs_for_videoid(ytvideoid)
      print('vinfo', vinfo)
      print('viewslist', viewslist)
      print('dateslist', dateslist)

  def __repr__(self):
    listlen = len(self.vvideos_views_dict)
    repr_str = 'YtChannelVideosAndItsViews <ytchannel={}, len(tuplelist)={}>'.format(self.ytchannel.nname, listlen)
    return repr_str

  def __str__(self):
    outstr = ''
    line = 'VideosAndItsViews for {}\n'.format(self.ytchannel.nname)
    outstr += line
    line = '-'*50 + '\n'
    outstr += line
    for i, ytvideoid in enumerate(self.vvideos_views_dict):
      tuplelist_vinfos_n_vviews = self.vvideos_views_dict[ytvideoid]
      for j, tuplelist_vinfos_n_vviews_per_video in enumerate(tuplelist_vinfos_n_vviews):
        vinfo = tuplelist_vinfos_n_vviews_per_video[0]
        vviews = tuplelist_vinfos_n_vviews_per_video[1]
        line = '{}-{} title "{}" vviews {} on date {}\n'.format(i+1, j+1, vinfo.title, vviews.views, vviews.infodate)
        outstr += line
    line = 'tuplelistsize {}'.format(self.tuplelistsize)
    outstr += line
    return outstr


def fetch_ytchannelvideos_n_its_views(ytchannelid):
  """

  :param ytchannelid:
  :return: ychannel_n_its_tuplelist_vinfo_n_vviews_dict
  """
  session = Session()
  ytchannel = session.query(YTChannelSA). \
      filter(YTChannelSA.ytchannelid == ytchannelid). \
      first()
  print(ytchannel)

  tuplelist_vinfo_n_vviews = session.query(YTVideoItemInfoSA, YTVideoViewsSA). \
      filter(YTVideoItemInfoSA.ytchannelid == ytchannelid). \
      filter(YTVideoViewsSA.ytvideoid == YTVideoItemInfoSA.ytvideoid). \
      order_by(YTVideoViewsSA.infodate). \
      all()
  session.close()

  tuplelist_vinfo_n_vviews = reversed(tuplelist_vinfo_n_vviews)
  ytchannelvideos_n_its_views = YtChannelVideosAndItsViews(ytchannel, tuplelist_vinfo_n_vviews)
  return ytchannelvideos_n_its_views


def fetch_ytvideospage_by_its_dbid(ytchannelid):
  session = Session()
  ytchannel = session.query(YTChannelSA) \
      .filter(YTChannelSA.ytchannelid == ytchannelid) \
      .first()
  ytvideospage = None
  if ytchannel:
    ytvideospage = YtVideosPage(ytchannel.ytchannelid, ytchannel.nname)
  session.close()
  return ytvideospage


def adhoc_test():
  ytchannelid = 'ueduardoamoreira'
  ytchannelvideos_n_its_views = fetch_ytchannelvideos_n_its_views(ytchannelid)
  print (ytchannelvideos_n_its_views)
  ytchannelvideos_n_its_views.make_views_pngs()


def process():
  adhoc_test()


if __name__ == '__main__':
  process()

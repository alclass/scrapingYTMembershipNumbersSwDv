#!/usr/bin/env python3
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA, YTVideoViewsSA

Session = sessionmaker(bind=sqlalchemy_engine)


class VideoItemInsertor:

  def __init__(self, videoinfo):
    """
    Important:
      one way to implement this class is to receive
        session, from sqlalchemy, from caller
      another way is to use session on spot and close it appropriately
      => this observation was motivated by a connection_pool overflown,
         ie, care should be taken with session and its pool size

    :param videoinfo:
    """
    self.total_videoinfo_insmod = 0
    self.total_videoinfo_records = 0
    self.total_videoviews_insmod = 0
    self.total_videoviews_records = 0

    self.videoinfo = videoinfo
    if self.videoinfo.infodate is None:
      error_msg = 'Error: videoinfo.infodate is None in VideoItemInsertor.transpose_fields()'
      raise ValueError(error_msg)

  def update_if_needed(self, videoitem_in_db, session):
    if videoitem_in_db.ytvideoid == self.videoinfo.ytvideoid and \
       videoitem_in_db.title == self.videoinfo.title and \
       videoitem_in_db.duration_in_sec == self.videoinfo.duration_in_sec:
      print('No need to updating: ytvideo, title & duration_in_sec coincide: ytvideoid =', self.videoinfo.ytvideoid)
      # no need to commit here but session should be closed so that connectionpool does not overflow
      # session.close()
      return False
    transpose_happened = self.transpose_fields(videoitem_in_db, session)
    if not transpose_happened:
      print('Not Updating videoitem_in_db', videoitem_in_db)
    # session.commit()
    # treat views
    # session.close()
    print('Updating videoitem_in_db', videoitem_in_db)
    return True

  def transpose_fields(self, videoitem_in_db, session, dbinsert=False):
    """

    :param videoitem_in_db:
    :param session:
    :param dbinsert:
    :return:
    """
    if dbinsert:
      videoitem_in_db.ytvideoid = self.videoinfo.ytvideoid

    former_infodate = None
    if videoitem_in_db.infodate != self.videoinfo.infodate:
      if videoitem_in_db.infodate is None:
        videoitem_in_db.infodate = self.videoinfo.infodate
      elif videoitem_in_db.infodate > self.videoinfo.infodate:
        # TO-DO create a --force parameter to undo a former insert/update
        return False
      former_infodate = videoitem_in_db.infodate

    changelog = videoitem_in_db.changelog
    if changelog is None:
      changelog = ''

    if videoitem_in_db.title != self.videoinfo.title:
      changelog += 'title: [%s]\n' % videoitem_in_db.title  # former_value
      videoitem_in_db.title = self.videoinfo.title

    if videoitem_in_db.duration_in_sec != self.videoinfo.duration_in_sec:
      changelog += 'duration_in_sec: [%s]\n' % str(videoitem_in_db.duration_in_sec)  # former_value
      videoitem_in_db.duration_in_sec = self.videoinfo.duration_in_sec

    if self.videoinfo.publishdate is not None:
      publishdate = self.videoinfo.publishdate
    else:
      # fallback to infodate
      publishdate = self.videoinfo.infodate

    if publishdate is None:
      error_msg = 'Error: publishdate is None (which means both this and infodate are None)\n'
      error_msg += '  => value of videoinfo = ' + str(self.videoinfo)
      raise ValueError(error_msg)

    if videoitem_in_db.publishdate != publishdate:
      videoitem_in_db.publishdate = publishdate

    if videoitem_in_db.published_time_ago != self.videoinfo.published_time_ago:
      if videoitem_in_db.published_time_ago is None:
        videoitem_in_db.published_time_ago = self.videoinfo.published_time_ago

    if self.videoinfo.ytchannel:
      if videoitem_in_db.ytchannelid != self.videoinfo.ytchannel.ytchannelid:
        former_value = videoitem_in_db.ytchannelid
        videoitem_in_db.ytchannelid = self.videoinfo.ytchannel.ytchannelid
        # changelog will be emptied if dbinsert is True, but this change
        # would happen if a videoid could change its ytuser/ytchannel (something that's not known)
        changelog += 'ytchannelid: [%s]\n' % former_value

    if not dbinsert and videoitem_in_db.changelog != changelog:
      changelog += 'on: [%s]\n' % str(former_infodate)
      changelog += '-----------------\n'
      videoitem_in_db.changelog = changelog
      print('Updating videoitem_in_db', videoitem_in_db)
      return True  # recipient must commit, something was changed

    if dbinsert:
      videoitem_in_db.changelog = ''
      print('Insert videoitem_in_db', videoitem_in_db)
      session.add(videoitem_in_db)
      return True  # recipient must commit, something was changed

    return False  # recipient doesn't need to commit, nothing was changed

  def inserts(self):
    session = Session()
    self.total_videoviews_records += 1
    self.total_videoviews_records += 1
    bool_modif_info = self.insert_videoinfo(session)
    bool_modif_views = self.insert_videoviews(session)
    if bool_modif_info or bool_modif_views:
      if bool_modif_views:
        self.total_videoviews_insmod += 1
      if bool_modif_info:
        self.total_videoinfo_insmod += 1
      session.commit()
    session.close()

  def insert_videoviews(self, session):
    # views part
    viewsitem_in_db = session.query(YTVideoViewsSA) \
      .filter(YTVideoViewsSA.ytvideoid == self.videoinfo.ytvideoid) \
      .filter(YTVideoViewsSA.infodate == self.videoinfo.infodate) \
      .first()
    if viewsitem_in_db is None:
      viewsitem_in_db = YTVideoViewsSA()
      viewsitem_in_db.ytvideoid = self.videoinfo.ytvideoid
      viewsitem_in_db.views = self.videoinfo.views
      viewsitem_in_db.infodate = self.videoinfo.infodate
      print('Adding views record:', viewsitem_in_db)
      session.add(viewsitem_in_db)
      return True
    print('Views record exists:', viewsitem_in_db)
    return False

  def insert_videoinfo(self, session):
    videoitem_in_db = session.query(YTVideoItemInfoSA) \
      .filter(YTVideoItemInfoSA.ytvideoid == self.videoinfo.ytvideoid) \
      .first()
    if videoitem_in_db:
      return self.update_if_needed(videoitem_in_db, session)
    videoitem_in_db = YTVideoItemInfoSA()
    # _ (underline var) is boolean not used in insert, only update
    _ = self.transpose_fields(videoitem_in_db, session, dbinsert=True)
    print('Adding/updating videoitem_in_db', videoitem_in_db)
    # views part
    return True

  def report(self):
    outstr = '''Report VideoItemInsertor:
  total_videoinfo_insmod = %d;  self.total_videoinfo_records = %d
  total_videoviews_insmod = %d; self.total_videoviews_records = %d    
    ''' % (
      self.total_videoinfo_insmod, self.total_videoinfo_records,
      self.total_videoviews_insmod, self.total_videoviews_records,
    )
    print(outstr)


def test1():
  pass


def process():
  print('Not testable for the time being.')
  # test1()


if __name__ == '__main__':
  process()

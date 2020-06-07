#!/usr/bin/python3
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA

Session = sessionmaker(bind=sqlalchemy_engine)

class VideoItemInsertor:

  def __init__(self, videoinfo):
    '''
    Important:
      one way to implement this class is to receive
        session, from sqlalchemy, from caller
      another way is to use session on spot and close it appropriately
      => this observation was motivated by a connection_pool overflown,
         ie, care should be taken with session and its pool size

    :param videoinfo:
    '''
    self.videoinfo = videoinfo
    if self.videoinfo.info_refdate is None:
      error_msg = 'Error: videoinfo.info_refdate is None in VideoItemInsertor.transpose_fields()'
      raise ValueError(error_msg)

  def update_if_needed(self, videoitem_in_db, session):
    if videoitem_in_db.ytvideoid == self.videoinfo.ytvideoid and \
       videoitem_in_db.views == self.videoinfo.views:
      print('No need to updating, record is still the same, ie views =', self.videoinfo.views)
      # no need to commit here but session should be closed so that connectionpool does not overflow
      session.close()
      return False
    transpose_happened = self.transpose_fields(videoitem_in_db)
    if transpose_happened:
      print('Updating', videoitem_in_db)
      session.commit()
    session.close()
    return True

  def transpose_fields(self, videoitem_in_db, dbinsert=False):
    '''

    :param videoitem_in_db:
    :return:
    '''
    if dbinsert:
      videoitem_in_db.ytvideoid = self.videoinfo.ytvideoid

    changelog = videoitem_in_db.changelog
    if changelog is None:
      changelog = ''

    if videoitem_in_db.title != self.videoinfo.title:
      former_value = videoitem_in_db.title
      videoitem_in_db.title = self.videoinfo.title
      changelog += 'title: [%s]\n' %former_value

    if videoitem_in_db.duration_in_sec != self.videoinfo.duration_in_sec:
      former_value = videoitem_in_db.duration_in_sec
      videoitem_in_db.duration_in_sec = self.videoinfo.duration_in_sec
      changelog += 'duration_in_sec: [%s]\n' %str(former_value)

    if videoitem_in_db.views != self.videoinfo.views:
      former_value = videoitem_in_db.views
      videoitem_in_db.views = self.videoinfo.views
      changelog += 'views: [%s]\n' %str(former_value)

    if videoitem_in_db.publishdate != self.videoinfo.publishdate:
      if videoitem_in_db.publishdate is None:
        videoitem_in_db.publishdate = self.videoinfo.publishdate

    if videoitem_in_db.published_time_ago != self.videoinfo.published_time_ago:
      if videoitem_in_db.published_time_ago is None:
        videoitem_in_db.published_time_ago = self.videoinfo.published_time_ago

    if videoitem_in_db.info_refdate != self.videoinfo.info_refdate:
      if videoitem_in_db.info_refdate is None:
        videoitem_in_db.info_refdate = self.videoinfo.info_refdate

    if self.videoinfo.ytchannel:
      if videoitem_in_db.ytchannelid != self.videoinfo.ytchannel.ytchannelid:
        former_value = videoitem_in_db.ytchannelid
        videoitem_in_db.ytchannelid = self.videoinfo.ytchannel.ytchannelid
        # changelog will be emptied if dbinsert is True, but this change would happen if a videoid could change its ytuser/ytchannel (something that's not known)
        changelog += 'ytchannelid: [%s]\n' %former_value

    if dbinsert:
      videoitem_in_db.changelog = ''
      return True # recipient must commit, something was changed

    if videoitem_in_db.changelog != changelog:
      changelog += 'on: [%s]\n' %str(self.videoinfo.info_refdate)
      changelog += '-----------------\n'
      videoitem_in_db.changelog = changelog
      return True # recipient must commit, something was changed

    return False # recipient doesn't need to commit, nothing was changed

  def insert(self):
    session = Session()
    videoitem_in_db = session.query(YTVideoItemInfoSA) \
      .filter(YTVideoItemInfoSA.ytvideoid == self.videoinfo.ytvideoid) \
      .first()
    if videoitem_in_db:
      return self.update_if_needed(videoitem_in_db, session)
    videoitem_in_db = YTVideoItemInfoSA()
    _ = self.transpose_fields(videoitem_in_db, dbinsert=True) # _ (underline var) is boolean not used in insert, only update
    print('Adding', videoitem_in_db)
    session.add(videoitem_in_db)
    session.commit()
    session.close()
    return True

def test1():
  pass

def process():
  print ('Not testable for the time being.')
  # test1()

if __name__ == '__main__':
  process()

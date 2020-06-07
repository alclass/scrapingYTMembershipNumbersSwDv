#!/usr/bin/python3
import datetime
from models.sa_models.ytchannelsubscribers_samodels import YTDailySubscribersSA
from fs.db.sqlalchdb.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=sqlalchemy_engine)

class SubscriberInsertor:

  def __init__(self, ytchid, refdate, n_subscribers):
    '''
    Important:
      one way to implement this class is to receive
        session, from sqlalchemy, from caller
      another way is to use session on spot and close it appropriately
      => this observation was motivated by a connection_pool overflown,
         ie, care should be taken with session and its pool size
    :param ytchid:
    :param refdate:
    :param n_subscribers:
    '''
    self.ytchid        = ytchid
    self.refdate       = refdate
    self.n_subscribers = n_subscribers
    self.boolean_dbmodified = False
    self.boolean_dbmodified = self.insert()

  def update_if_needed(self, dailysubs, session):
    if dailysubs.subscribers == self.n_subscribers:
      print('No need to updating, record is still the same =>', dailysubs)
      # no need to commit here but session should be closed
      session.close()
      return False
    dailysubs.subscribers = self.n_subscribers
    print('Updating', dailysubs)
    session.commit()
    session.close()
    return True

  def insert(self):
    session = Session()
    dailysubs = session.query(YTDailySubscribersSA).\
      filter(YTDailySubscribersSA.ytchannelid == self.ytchid). \
      filter(YTDailySubscribersSA.date == self.refdate). \
      first()
    if dailysubs:
      return self.update_if_needed(dailysubs, session)
    dailysubs = YTDailySubscribersSA(
      ytchannelid = self.ytchid,
      date        = self.refdate,
      subscribers = self.n_subscribers
    )
    print('Adding', dailysubs)
    session.add(dailysubs)
    session.commit()
    session.close()
    return True

def test1():
  ytchid = 'upgjr23'
  refdate = datetime.date(2020,5,2)
  n_subscribers = 200 * 1000
  SubscriberInsertor(ytchid, refdate, n_subscribers)

def process():
  print ('Not testable for the time being.')
  # test1()

if __name__ == '__main__':
  process()

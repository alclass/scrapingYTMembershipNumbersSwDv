#!/usr/bin/python3
import datetime
from db.models_sqlalchemy import DailySubscribers
from db.sqlalchemy_conn import sqlalchemy_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=sqlalchemy_engine)

class SubscriberInsertor:

  def __init__(self, ytchid, refdate, n_subscribers):
    self.ytchid        = ytchid
    self.refdate       = refdate
    self.n_subscribers = n_subscribers
    self.session = Session()
    self.insert()

  def update_if_needed(self, dailysubs):
    if dailysubs.subscribers == self.n_subscribers:
      print('No need to updating, record is still the same =>', dailysubs)
      return False
    dailysubs.subscribers = self.n_subscribers
    print('Updating', dailysubs)
    self.session.commit()
    return True

  def insert(self):
    dailysubs = self.session.query(DailySubscribers).\
      filter(DailySubscribers.ytchannelid == self.ytchid). \
      filter(DailySubscribers.date == self.refdate). \
      first()
    if dailysubs:
      return self.update_if_needed(dailysubs)
    dailysubs = DailySubscribers(ytchannelid=self.ytchid, date=self.refdate, subscribers=self.n_subscribers)
    print('Adding', dailysubs)
    self.session.add(dailysubs)
    self.session.commit()
    return True

def test():
  ytchid = 'upgjr23'
  refdate = datetime.date(2020,5,2)
  n_subscribers = 200 * 1000
  SubscriberInsertor(ytchid, refdate, n_subscribers)

def process():
  test()

if __name__ == '__main__':
  process()

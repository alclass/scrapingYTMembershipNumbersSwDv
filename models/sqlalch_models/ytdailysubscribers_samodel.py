#!/usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.sqlalch_models.ytchannels_samodel import YTChannelSA

class YTDailySubscribersSA(Base): # YTDailySubscribersSA <= DailySubscribers
  '''
  DailySubscribers class to dailychannelsubscribernumbers sql-table
  '''
  __tablename__ = 'dailychannelsubscribernumbers'
  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  date = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship('Channel')

  def __repr__(self):
    return '<DailySubscribers(ytchannelid="%s", date="%s". subscribers=%d)>' % (self.ytchannelid, str(self.date), self.subscribers)

def test():
  '''
  This test does not take a Session object so it does not record to db
  :return:
  '''
  test_channel = YTChannelSA(ytchannelid='upgjr23', nname="Ghiraldelli Louco")
  print('test_channel', test_channel)
  daily19 = YTDailySubscribersSA(subscribers=40, date='2020-05-19', ytchannel=test_channel)
  daily20 = YTDailySubscribersSA(subscribers=37, date='2020-05-20', ytchannelid='upgjr23')
  print ('daily19', daily19)
  print ('daily19.ytchannel', daily19.ytchannel)
  print('daily19.ytchannelid', daily19.ytchannelid)
  print ('daily20', daily20)
  print ('daily20.ytchannel', daily20.ytchannel)

def process():
  test()

if __name__ == '__main__':
  process()

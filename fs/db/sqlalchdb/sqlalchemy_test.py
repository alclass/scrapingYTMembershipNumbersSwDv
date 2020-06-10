#!/usr/bin/python3
'''
In other to make mysql work with sqlalchemy, two things were done:
  1) Ubuntu's package python3-dev and libmysqlclient-dev were installed;
  2) after that, mysqlclient was installed via pip.

Because in this machine, a virtualenv is taken by the IDE (PyCharm),
 mysqlclient was installed both globally (so that flaskapp could be run without activating
 virtualenv and then also installed locally. so that PyCharm could also run flaskapp).

SqlAlchemy

=> to learn how to use Foreign Keys in SqlAlchemy
  => docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign key

'''

#from db.sqlalchemy_conn import sqlalchemy_engine
#print(sqlalchemy_engine)

# import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Channel(Base):

  __tablename__ = 'channels'
  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(String)

  def __repr__(self):
    return '<Channel(nname="%s", ytchannelid="%s")>' %(self.nname, self.ytchannelid)

channel_ghira = Channel(ytchannelid='upgjr23', nname="Paulo Ghiraldelli")
print (channel_ghira)

class DailySubscribers(Base):

  __tablename__ = 'dailychannelsubscribernumbers'
  id = Column(Integer, primary_key=True)
  subscribers = Column(Integer)
  date = Column(Date)

  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  ytchannel = relationship('Channel')

  def __repr__(self):
    return '<DailySubscribers(ytchannelid="%s", subscribers=%d, infodate="%s")>' % (self.ytchannelid, self.subscribers, str(self.date))

daily19 = DailySubscribers(ytchannel=channel_ghira, subscribers=40, date='2020-05-19')
daily20 = DailySubscribers(ytchannel=channel_ghira, subscribers=40, date='2020-05-20')
print ('daily19', daily19)
print ('daily19.ytchannel', daily19.ytchannel)
print ('daily20', daily20)
print ('daily20.ytchannel', daily20.ytchannel)


def process():
  pass

if __name__ == '__main__':
  process()
#!/usr/bin/python3
'''
In other to make mysql work with sqlalchemy, two things were done:
  1) Ubuntu's package python3-dev and libmysqlclient-dev were installed;
  2) after that, mysqlclient was installed via pip.

Because in this machine, a virtualenv is taken by the IDE (PyCharm), 
 mysqlclient was installed both globally (so that app could be run without activating
 virtualenv and then also installed locally. so that PyCharm could also run app).

SqlAlchemy

=> to learn how to use Foreign Keys in SqlAlchemy
  => docs.sqlalchemy.org/en/13/orm/join_conditions.html?highlight=foreign key

'''
# import sqlalchemy
from sqlalchemy import create_engine
import config


this_db = config.THIS_DATABASE;
user         = config.DATABASE_DICT[this_db]['USER']
password     = config.DATABASE_DICT[this_db]['PASSWORD']
address      = config.DATABASE_DICT[this_db]['ADDRESS']
port         = config.DATABASE_DICT[this_db]['PORT']
databasename = config.DATABASE_DICT[this_db]['DATABASENAME']

engine_line = this_db + '://' + user + ':' + password + '@' + address + '/' + databasename

engine = create_engine(engine_line)
print (engine_line)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Date, ForeignKey

class Channel(Base):

  __tablename__ = 'channels'
  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, unique=True)
  nname = Column(String)
  obs = Column(String)

  def __repr__(self):
    return '<Channel(nname="%s", ytchid="%s")>' %(self.nname, self.ytchannelid)

channel = Channel(ytchannelid='upgjr23', nname="Ghira louca")
print (channel)

class DailySubscribers(Base):

  __tablename__ = 'dailychannelsubscribernumbers'
  id = Column(Integer, primary_key=True)
  ytchannelid = Column(String, ForeignKey('channels.ytchannelid'))
  subscribers = Column(Integer)
  date = Column(Date)

  def __repr__(self):
    return '<DailySubscribers(ytchid="%s", subscribers="%d", date="%s")>' % (self.ytchannelid, self.subscribers, str(self.date))

daily19 = DailySubscribers(ytchannelid='upgjr23', subscribers=40, date='2020-05-19')
daily20 = DailySubscribers(ytchannelid='upgjr23', subscribers=40, date='2020-05-20')
print (daily19)
print (daily20)


def process():
  pass

if __name__ == '__main__':
  process()
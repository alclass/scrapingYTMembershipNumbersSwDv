#!/usr/bin/python3
from db.insert_update_subscribers import Session
from db.models_sqlalchemy import Channel
from db.models_sqlalchemy import DailySubscribers

class SubscriberDays:

  def __init__(self):
    self.session = Session()
    self.fetch_all_ytchids()
    self.loop_thru_channels()

  def fetch_all_ytchids(self):
    self.channels = self.session.query(Channel).all()
    print ('Fetched', len(self.channels), 'channels.')

  def loop_thru_channels(self):
    for channel in self.channels:
      self.dailysubs = self.session.query(DailySubscribers).\
        filter(DailySubscribers.ytchannelid==channel.ytchannelid).all()
      print('Channel', channel.nname, 'has', len(self.dailysubs), 'daily subscribers records.')
      if len(self.dailysubs) > 0:
        self.tabulate_subscribers_per_day(channel)

  def tabulate_subscribers_per_day(self, channel):
      days_n_subscribers = []
      for dailysub in self.dailysubs:
        strmonth = str(dailysub.date.month)
        strday   = str(dailysub.date.day)
        mon_day = '%s/%s' %(strday, strmonth)
        day_n_subscriber_tuple = (mon_day, dailysub.subscribers)
        days_n_subscribers.append(day_n_subscriber_tuple)
      days_n_subscribers = sorted(days_n_subscribers, key=lambda x : x[0])
      print(channel.nname, days_n_subscribers)

def process():
  SubscriberDays()

if __name__ == '__main__':
  process()

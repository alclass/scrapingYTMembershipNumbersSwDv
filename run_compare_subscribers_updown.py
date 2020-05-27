#!/usr/bin/python3
import datetime
import scrapeHtmlsMod as scrap
from db.insert_update_subscribers import Session
from db.models_sqlalchemy import Channel
from db.models_sqlalchemy import DailySubscribers

def fetch_all_ytchids():
  session = Session()
  channels = session.query(Channel).all()
  for channel in channels:
    dailysubs = session.query(DailySubscribers).\
      filter(DailySubscribers.ytchannelid==channel.ytchannelid).all()
    numbers = {}
    for dailysub in dailysubs:
      numbers[dailysub.date.day] = dailysub.subscribers
    print(channel.nname, numbers)

def process():
  fetch_all_ytchids()

if __name__ == '__main__':
  process()

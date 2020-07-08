import datetime, json, calendar
# from dateutil import relativedelta # calculate duration between two dates
from models.gen_models.YtVideosPageMod import YtVideosPage
from models.sa_models.ytchannelsubscribers_samodels import YTVideoViewsSA
from models.sa_models.ytchannelsubscribers_samodels import YTVideoItemInfoSA
from models.sa_models.ytchannelsubscribers_samodels import get_all_ytchannelids
from fs.db.sqlalchdb.sqlalchemy_conn import Session
import fs.datefunctions.datefs as dtfs
# import fs.filefunctions.autofinders as finder

beginningStr = '{"gridVideoRenderer":{'
endStr = '}]}}}]}}'

def convert_datetime_to_date(pdatetime):
  pdate = datetime.date(year=pdatetime.year, month=pdatetime.month, day=pdatetime.day)
  return pdate

def monthdelta(date, delta):
  '''
  Ref https://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python

  d = min(date.day, calendar.monthrange(y, m)[1])
      or
  d = min(date.day, [31,
                     29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])

  :param date:
  :param delta:
  :return:
  '''
  m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
  if not m: m = 12
  d = min(date.day, calendar.monthrange(y, m)[1])
  return date.replace(day=d, month=m, year=y)

class VideoItem:

  def __init__(self, ytvideoid, title, calendarDateStr, n_views, durationStr, videopagefilesdatetime, ytchannelid):
    self.ytvideoid = ytvideoid
    self.title = title
    self.calendarDateStr = calendarDateStr
    self.n_views = None; self.treat_views(n_views)
    self.durationStr = durationStr
    self.videopagefilesdatetime = videopagefilesdatetime
    self.ytchannelid = ytchannelid
    self.publishedDate = None # to be calculated
    self.calculate_publishdate()

  def treat_views(self, n_views):
    try:
      word = n_views.strip().split(' ')[0]
      word = word.replace('.','').replace(',','')
      self.n_views = int(word)
    except ValueError:
      self.n_views = 0

  @property
  def videopagefilesdate(self):
    return convert_datetime_to_date(self.videopagefilesdatetime)

  @property
  def duration_in_sec(self):
    return dtfs.transform_hms_into_duration_in_sec(self.durationStr)


  def calculate_publishdate(self):

    self.calendarDateStr = dtfs.ajust_calendardatestr_to_start_with_a_number(self.calendarDateStr)

    if self.calendarDateStr.find('minut') > -1:
      n_min = int(self.calendarDateStr.strip().split(' ')[0])
      publishedTime = self.videopagefilesdatetime - datetime.timedelta(minutes=n_min)
      self.publishedDate = datetime.date(year=publishedTime.year, month=publishedTime.month, day=publishedTime.day)
    elif self.calendarDateStr.find('hora') > -1:
      n_horas = int(self.calendarDateStr.strip().split(' ')[0])
      publishedTime = self.videopagefilesdatetime - datetime.timedelta(hours=n_horas)
      self.publishedDate = datetime.date(year=publishedTime.year, month=publishedTime.month, day=publishedTime.day)
    elif self.calendarDateStr.find('dia') > -1:
      n_dias = int(self.calendarDateStr.strip().split(' ')[0])
      publishedTime = self.videopagefilesdatetime - datetime.timedelta(days=n_dias)
      self.publishedDate = datetime.date(year=publishedTime.year, month=publishedTime.month, day=publishedTime.day)
    elif self.calendarDateStr.find('semana') > -1:
      n_semanas = int(self.calendarDateStr.strip().split(' ')[0])
      publishedTime = self.videopagefilesdatetime - datetime.timedelta(weeks=n_semanas)
      self.publishedDate = convert_datetime_to_date(publishedTime)
    elif self.calendarDateStr.find('mês') > -1 or self.calendarDateStr.find('mes') > -1: # mes for meses
      n_meses = int(self.calendarDateStr.strip().split(' ')[0])
      filesDate = convert_datetime_to_date(self.videopagefilesdatetime)
      self.publishedDate = monthdelta(filesDate, n_meses)
    elif self.calendarDateStr.find('ano') > -1:
      n_anos = int(self.calendarDateStr.strip().split(' ')[0])
      filesDate = convert_datetime_to_date(self.videopagefilesdatetime)
      self.publishedDate = monthdelta(filesDate, n_anos * 12)

  def write_item_to_db_item_n_views(self):
    bool_res = self.write_item_to_db()
    if bool_res:
      print('Written item', self.ytvideoid, self.title)
    else:
      print(' *NOT* Written item', self.ytvideoid, self.title)

    bool_res = self.write_views_to_db()
    if bool_res:
      print('Written views', self.n_views, self.videopagefilesdate)
    else:
      print(' *NOT* Written views', self.n_views, self.videopagefilesdate)

  def write_item_to_db(self):
    session = Session()
    videoitem = session.query(YTVideoItemInfoSA).filter(YTVideoItemInfoSA.ytvideoid==self.ytvideoid).first()
    if videoitem:
      session.close()
      return False
    videoitem = YTVideoItemInfoSA()
    videoitem.ytvideoid = self.ytvideoid
    videoitem.title = self.title
    videoitem.duration_in_sec = self.duration_in_sec
    videoitem.publishdate = self.publishedDate
    videoitem.published_time_ago = self.calendarDateStr
    videoitem.infodate = self.videopagefilesdate
    videoitem.ytchannelid = self.ytchannelid
    session.add(videoitem)
    session.commit()
    session.close()
    return True

  def write_views_to_db(self):
    session = Session()
    vviews = session.query(YTVideoViewsSA).\
      filter(YTVideoViewsSA.ytvideoid==self.ytvideoid).\
      filter(YTVideoViewsSA.infodate==self.videopagefilesdate).\
      first()
    if vviews:
      session.close()
      return False
    vviews = YTVideoViewsSA()
    vviews.ytvideoid = self.ytvideoid
    vviews.views = self.n_views
    vviews.infodate = convert_datetime_to_date(self.videopagefilesdatetime)
    session.add(vviews)
    session.commit()
    session.close()
    return True

  def as_dict(self):
    outdict = {
      'ytvideoid'      : self.ytvideoid,
      'title'          : self.title,
      'calendarDateStr': self.calendarDateStr,
      'publishedDate': self.publishedDate,
      'n_views'        : str(self.n_views),
      'durationStr'    : self.durationStr,
    }
    return outdict

  def __str__(self):
    outstr = '''<VideoItem
    ytvideoid = %(ytvideoid)s
    title = %(title)s
    calendarDateStr = %(calendarDateStr)s
    publishedDate   = %(publishedDate)s
    n_views = %(n_views)s
    durationStr = %(durationStr)s
>''' %self.as_dict()
    return outstr

def drill_down_dict(pdict, videopagefilesdatetime, ytchannelid):
  ytvideoid       = pdict['gridVideoRenderer']['videoId']
  try:
    title           = pdict['gridVideoRenderer']['title']['simpleText']
  except KeyError:
    title = 'No Title'
  try:
    calendarDateStr = pdict['gridVideoRenderer']['publishedTimeText']['simpleText']
  except KeyError:
    calendarDateStr = '1 minut'
  try:
    n_views         = pdict['gridVideoRenderer']['viewCountText']['simpleText']
  except KeyError:
    n_views = '0 v'
  try:
    durationStr     = pdict['gridVideoRenderer']['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text']['simpleText']
  except KeyError:
    durationStr = '0:0'
  vitem = VideoItem(ytvideoid, title, calendarDateStr, n_views, durationStr, videopagefilesdatetime, ytchannelid)
  print(vitem)
  vitem.write_item_to_db_item_n_views()

def extract_videoitems_from_videopage(ytchannelid, refdate):
  ytvideopage = YtVideosPage(ytchannelid, None, refdate)
  if ytvideopage.datedpage_filepath is None:
    print ('Filepath is None for', ytchannelid, ':: returning...' )
    return
  timestamp = ytvideopage.filesdatetime.st_atime
  print (ytvideopage.filesdatetime.st_atime)
  videopagefilesdatetime = datetime.datetime.fromtimestamp(timestamp)
  print (videopagefilesdatetime)

  text = ytvideopage.get_html_text()
  begpos = text.find(beginningStr)
  counter = 0; chunk = ''; lastchunk = ''
  while begpos > -1:
    text = text[ begpos : ]
    endpos = text.find(endStr)
    if endpos > -1:
      lastchunk = chunk = text[ : endpos + len(endStr)]
      # strchunk = chunk
      # chunkline = chunk if len(chunk) < 55 else strchunk[:25] + '...' + strchunk[-25:]
      counter += 1
      try:
        pdict = json.loads(lastchunk)
        drill_down_dict(pdict, videopagefilesdatetime, ytchannelid)
      except json.decoder.JSONDecodeError:
        print ('='*50)
        # TO-DO log it to a file, so that we'll be able to find a flawd videopage file
        print ('=> Failed for', ytvideopage.ytchannelid, ytvideopage.filename)
        print ('='*50)
        continue
    text = text[endpos : ]
    begpos = text.find(beginningStr)

  # pdict = json.loads(lastchunk)
  # print(lastchunk)

def run_all():
  today = datetime.date.today()
  yesterday = today - datetime.timedelta(days=1)
  for ytchannelid in get_all_ytchannelids(): # ytchannelids = finder.get_ytchannelids_on_datefolder(today)
    for refdate in [yesterday, today]:  # dtfs.get_range_date(yesterday, today):
      print ('Rolling', ytchannelid, 'for date', refdate )
      print ('-'*50)
      extract_videoitems_from_videopage(ytchannelid, refdate)

def process():
  '''
  refdate = datetime.date.today()
  ytchannelid = 'ueduardoamoreira'
  ytchannelid = 'uhumbertocostapt'
  extract_videoitems_from_videopage(ytchannelid, refdate)

  :return:
  '''
  run_all()


if __name__ == '__main__':
  process()
#!/usr/bin/python3
import datetime, os
import run_compare_subscribers_updown as comp
import fs.statfunctions.statisticsMod as statmod
import fs.db.SubscriberDaysMod as subsmod

def recompose_date(strdaymonth):
  pp = strdaymonth.split('/')
  refdate = datetime.date(2020, int(pp[1]), int(pp[0]))
  return refdate

def make_statistic_fig_imgsrc_uptodate(days_n_subscribers):
  pass

class HtmlMaker:
  def __init__(self):
    self.comparator = subsmod.SubscriberDays()
    self.make_htmltop()
    self.make_htmlbody()
    self.make_htmlbottom()

  def make_htmltop(self):
    self.html = '''
<html>
  <body>
'''

  def make_htmlbody(self):
    for i, channel in enumerate(self.comparator.channels):
      seq = i + 1
      self.html += '<h3>[%d] %s<h3><br>\n' %(seq, channel.nname)
      dates = map(lambda x : x[0], channel.days_n_subscribers)
      dates = list(dates)
      make_statistic_fig_imgsrc_uptodate(channel.days_n_subscribers)
      refdate = recompose_date(dates[-1])
      blah = 'blah'
      subcribers_list = map(lambda x : x[1], channel.days_n_subscribers)
      subcribers_list = list(subcribers_list)
      mini, maxi, diff, delt = statmod.calc_min_max_dif_del(subcribers_list)
      # self.html += '<img src="%s"><br>\n' %blah # %channel.get_statistic_fig_imgsrc_uptodate(refdate)
      self.html += '<table>'
      self.html += '<tr><th>min</th><th>max</th><th>dif</th><th>del</th></tr>\n'
      self.html += '<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td></tr>\n' \
        %(mini, maxi, diff, delt)
      self.html += '</table><br>\n'

  def make_htmlbottom(self):
    self.html += '''
  </body>
</html>
    '''

  def save_to_conventioned_folder(self):
    currentfolder_abspath = os.path.abspath('.')
    outfilename = 'ztest_channels_with_statistics_imgs.html'
    outfile_abspath = os.path.join(currentfolder_abspath, outfilename)
    fp = open(outfile_abspath, 'w')
    print('Writing file', outfilename)
    fp.write(str(self))
    fp.close()

  def __str__(self):
    return self.html

def process():
  htmlmaker = HtmlMaker()
  print(htmlmaker)
  htmlmaker.save_to_conventioned_folder()

if __name__ == '__main__':
  process()

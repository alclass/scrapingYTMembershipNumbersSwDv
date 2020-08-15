#!/usr/bin/env python3
"""
  docstring
"""
import fs.numberfunctions.statisticsMod as statM
import models.procdb.SubscriberDaysMod as subsM
import fs.filefunctions.pathfunctions as pathfs
import fs.graphics.barchartmod as bar


class HtmlMaker:
  def __init__(self):
    self.html = None
    self.comparator = subsM.SubscriberDays()
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
      self.html += '<h3>[%d] %s (<a href="%s">enlace</a>)<h3><br>\n' % (seq, channel.nname, channel.videospageurl)
      # dates = list(map(lambda x: x[0], channel.days_n_subscribers))
      print(seq, 'Saving png for', channel.nname)
      bar.save_graphic_to_folder(channel)  # ytvideospage
      # make_statistic_fig_imgsrc_uptodate(channel.days_n_subscribers)
      # strefdate = dtfs.get_refdate_from_strdate(dates[-1])
      subcribers_list = map(lambda x: x[1], channel.days_n_subscribers)
      subcribers_list = list(subcribers_list)
      first = subcribers_list[0]
      last = subcribers_list[-1]
      n_data = len(subcribers_list)
      mini, maxi, diff, delt = statM.calc_min_max_dif_del(subcribers_list)
      # %channel.get_statistic_fig_imgsrc_uptodate(refdate)
      self.html += '<img src="./img/%s">%s<br>\n' % (channel.png_filename, channel.nname)
      self.html += '<table border="1">'
      self.html += '<tr><th>n-data</th><th>first</th><th>last</th><th>min</th><th>max</th>' \
                   '<th>dif</th><th>del</th></tr>\n'
      self.html += '<tr><td>%d</td><td>%d</td><td>%d</td><td>%d</td>' \
                   '<td>%d</td><td>%d</td><td>%d</td></tr>\n' \
          % (n_data, first, last, mini, maxi, diff, delt)
      self.html += '</table><br>\n'

  def make_htmlbottom(self):
    self.html += '''
  </body>
</html>
    '''

  def save_to_conventioned_folder(self):
    statichtml_fileabspath = pathfs.get_statichtml_fileabspath()
    statichtml_filename = pathfs.get_statichtml_filename()
    fp = open(statichtml_fileabspath, 'w')
    print('Writing file', statichtml_filename, 'at', statichtml_fileabspath)
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

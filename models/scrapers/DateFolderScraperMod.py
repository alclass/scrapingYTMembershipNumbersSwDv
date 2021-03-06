#!/usr/bin/python3
import json
import fs.datefunctions.datefs as dtfs
from models.scrapers import YtVideoPagesTraversalMod as readmod
from models.scrapers.SubscriberScraperMod import HTMLScraper

class DateFolderScraper:

  def __init__(self, refdate=None):
    self.refdate = dtfs.get_refdate_or_today(refdate)
    # self.strdate is @property
    self.reader = readmod.YtVideoPagesTraversal(refdate)
    self.counter = 0
    # self.scrapingResuls = []
    print ('Please, wait a moment; there are', self.reader.n_of_pages, 'pages to be processed.')
    self.ids_with_subsnumber_not_found = []
    self.id_n_qty_tuplelist = []
    self.scrape_to_inner_vars()

  @property
  def strdate(self):
    return dtfs.get_strdate(self.refdate)

  def scrape_to_inner_vars(self):
    for ytvideopagesobj in self.reader.ytvideopageobj_list:
      self.counter += 1
      scraper = HTMLScraper(ytvideopagesobj)
      qty = scraper.ytvideopageobj.n_subscribers
      if qty is None:
        continue
      ytchid = scraper.ytvideopageobj.ytchannelid
      tupl = (ytchid, qty)
      self.id_n_qty_tuplelist.append(tupl)

  def print_scraping_results(self):
    # for i, subsrecord in enumerate(self.scrapingResuls):
    for i, ytvideopageobj in enumerate(self.reader.ytvideopageobj_list):
      # subsrecord = ytvideopageobj.scrapedrecord
      quant = ytvideopageobj.n_subscribers
      print(i+1, ytvideopageobj.refdate, ytvideopageobj.sname, 'has', quant)
      if quant < 1:
        outmsg = '''
        >>>>>>>>>>> %d <<<<<<<<<<<<<
        ''' %quant
        print (outmsg)

  def saveJson(self):
    outlist = []
    for i, ytvideopageobj in enumerate(self.reader.ytvideopageobj_list):
      dictrecord = ytvideopageobj.as_dict_for_json()
      outlist.append(dictrecord)
    outfilename = self.strdate + ' test.json'
    outfile = open(outfilename, 'w', encoding='utf8')
    outtext = json.dumps(str(outlist))
    outfile.write(outtext)
    outfile.close()

def process():
  #refdate = datetime.infodate(2020,5,26)
  #scraper = HTMLScraper(refdate)
  datescraper = DateFolderScraper()
  datescraper.print_scraping_results()
  print ('len ytvideopageobj_list =', len(datescraper.reader.ytvideopageobj_list))
  print ('len id_n_qty_tuplelist =', len(datescraper.id_n_qty_tuplelist))
  # print ('len ids_with_subsnumber_not_found =', len(datescraper.ids_with_subsnumber_not_found), scraper.ids_with_subsnumber_not_found)

if __name__ == '__main__':
  process()

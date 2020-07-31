
def adhoc_test():
  tupl = find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  level1abspathentries = find_1stlevel_yyyymm_dir_abspaths()
  print('level1abspathentries', level1abspathentries)
  print (tupl)
  dateini_n_dateend = find_dateini_n_dateend_thru_yyyymmdd_level2_folders()
  print ('dateini_n_dateend', dateini_n_dateend)

def test_walk_thru_level2_datenamed_folders():
  level2_foldernames = find_yyyymmdd_level2_foldernames()
  for i, level2_foldername in enumerate(level2_foldernames):
    seq = i+1
    print (seq, level2_foldername)

def test1():
  # lambdajoinabspath = lambda abspath, entry: os.path.join(abspath, entry)
  abspath = '/this/path/is/test'
  entries = ['adfa', 'mkmfkgçsmf', 'oiopipo']
  zipped = list(zip([abspath]*len(entries), entries))
  print ('zipped', zipped)
  absentries = list(map(lambdajoinabspath, zipped)) # abspath, entries
  print('absentries via map-lambda', absentries)
  testpath = lambdajoinabspath ((abspath, 'adfa2'))
  print('testpath', testpath)
  absentries = []
  for e in entries:
    absentry = os.path.join(abspath, e)
    absentries.append(absentry)
  print('absentries via for-loop', absentries)

def test_traversor():
  '''
  filename = '2020-05-22 Eduardo Mo [ueduardoamoreira].html'
  dht = HtmlInDateFolder(filename)
  print('HtmlInDateFolder(filename)', dht)
  '''
  print ("DatedHtmlsTraversor('2020-05-22', '2020-06-05')")
  traversor = DatedHtmlsTraversor('2020-05-22', '2020-06-05')
  print(traversor)
  for i, obj in enumerate(traversor.traverse()):
    seq = i + 1
    print (seq, '==>', obj)

def process():
  test_traversor()
  # test1()
  # adhoc_test()

if __name__ == '__main__':
  process()
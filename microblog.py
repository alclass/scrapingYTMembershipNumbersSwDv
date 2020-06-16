import datetime
from flaskapp import app
'''
export FLASK_APP=microblog.py 
'''
@app.context_processor
def inject_jinjatoday():
  today = datetime.date.today()
  return dict(jinjatoday=today)

# g.count_sa_sessions = 0
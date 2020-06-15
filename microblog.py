import datetime
from flaskapp import app
'''
export FLASK_APP=microblog.py 
'''
@app.context_processor
def inject_today():
  today = datetime.date.today()
  return dict(today=today)
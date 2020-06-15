from flask import render_template, flash, redirect, url_for
from flaskapp import app
from flaskapp.forms import LoginForm
from flaskapp import views

def get_data():
  userdict = {'username': 'Miguel'}
  posts = [
    {
      'author' : {'username': 'Miguel'},
      'body': 'Beautiful day in Portland!',
    },
    {
      'author': {'username': 'Susan'},
      'body': 'The Avengers movie was so cool!',
    },
  ]
  return userdict, posts

@app.route('/')
@app.route('/index')
def index():
  userdict, postsdata = get_data()
  return render_template('index.html', title='Home Page', user=userdict, posts=postsdata)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data
    ))
    redirect(url_for('index'))
  return render_template('login.html', title='Sign In', form=form)

@app.route('/clist')
def ytchannel_lister():
  return views.list_ytchannels_view()

# videos_per_channel
@app.route('/channel/<ytchannelid>/videos/')
def videos_per_channel(ytchannelid):
  return views.videos_per_channel(ytchannelid=ytchannelid)

# ytchannel_summary
@app.route('/channel/<ytchannelid>')
def ytchannel(ytchannelid):
  return views.ytchannel_summary(ytchannelid=ytchannelid)

# views per video
@app.route('/video/<ytvideo>')
def views_per_video(ytvideo):
  return views.views_per_video(ytvideo=ytvideo)



@app.route('/tview')
def testview():
  return 'testview hi'

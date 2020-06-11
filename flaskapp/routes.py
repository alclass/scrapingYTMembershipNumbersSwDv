from flask import render_template, flash, redirect, url_for
from flaskapp import app
from flaskapp.forms import LoginForm

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

def testview():
  return 'hi'
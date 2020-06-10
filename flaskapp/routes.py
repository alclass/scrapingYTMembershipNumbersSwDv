from flask import render_template
from flaskapp import app

html_to_interpolate = '''
<html>
  <head>
    <title>Home Page - Microblog</title>    
  </head>
  <body>
      <h1>Hello, %(username)s!</h1>    
    </body>
</html>
'''

def interpolate():
  userdict = {'username': 'Miguel'}
  html_text = html_to_interpolate %userdict
  return html_text

@app.route('/')
@app.route('/index')
def index():
  userdict = {'username': 'Miguel'}
  return render_template('index.html', title='Home Page', user=userdict) # interpolate() # 'hello, world!'

'''
def adhoc_test():
  print(interpolate())

if __name__ == '__main__':
  adhoc_test()
'''
from flask import Flask
from flask import render_template, redirect, request
from flask import url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
import os
import base64

app = Flask(__name__)
app.config['DEBUG'] = True

# TODO: put these secret keys into separate folders
app.config.update(
  GOOGLE_CLIENT_ID='231222742854-jjqme28vdvmp8ctm4a977dpua8v0hno7.apps.googleusercontent.com',
  GOOGLE_CLIENT_SECRET='76vyRF14oMXxAsigIk23FqAp',
  SECRET_KEY='just a secret key, to confound the bad guys',
  DEBUG=True
)

oauth = OAuth(app)
google = oauth.remote_app(
  'google',
  consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
  consumer_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
  request_token_params={
      'scope': 'https://www.googleapis.com/auth/userinfo.email \
                https://www.googleapis.com/auth/gmail.readonly \
                https://www.googleapis.com/auth/userinfo.profile'
  },
  base_url='https://www.googleapis.com/oauth2/v1/',
  request_token_url=None,
  access_token_method='POST',
  access_token_url='https://accounts.google.com/o/oauth2/token',
  authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@app.route('/')
def index():
  """Return a our landing page."""
  return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

@app.route('/me')
def me():
  if 'google_token' in session:
    me = google.get('userinfo')
    return jsonify({"data": me.data})
  return redirect(url_for('login'))


@app.route('/mail')
def mail():
  ''' Builds a GMAIL API query for macy's emails in the last 6 months.
  Returns a function call asking for the contents of thoseemails.'''
  if 'user_email' in session:
    query = "macy macy's after:2014/9/23"
    url = "https://www.googleapis.com/gmail/v1/users/%s/messages" % session.get('user_email')
    response = google.get(url, data = {"q": query})
    data = response.data
    messages = data["messages"] # messages is a list of dictionaries [{ 'id': '12345', 'threadId': '12345'}, ]
    messages = get_message_body(messages)
    return render_template('mail.html', messages=messages)
  return redirect(url_for('login'))


def get_message_body(messages):
  bodies = []
  url = "https://www.googleapis.com/gmail/v1/users/%s/messages/" % session.get('user_email')
  for m in messages:
    curr_url = url + m["id"]
    mail = google.get(curr_url)
    bodies.append(base64.urlsafe_b64decode(mail.data['payload']['body']['data'].encode('ASCII')))
  return bodies


'''
  OAuth2 flow:
  1. Coupal redirects user to /login
  2. User authenticates itself using Google account info
  3. Google redirects to /authcallback
'''

@app.route('/login')
def login():
  return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/authcallback')
def authorized():
  resp = google.authorized_response()
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
        request.args['error_reason'],
        request.args['error_description']
    )
  session['google_token'] = (resp['access_token'], '')
  session['user_email'] = google.get('userinfo').data['email']
  return redirect(url_for('me'))


@app.route('/logout')
def logout():
  session.pop('google_token', None)
  return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
  return session.get('google_token')


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
# But this app.run() is for local virtual environment (not WSGI) debugging
if __name__ == '__main__':
    app.run(port=8080)

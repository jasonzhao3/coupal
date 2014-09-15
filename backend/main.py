from flask import Flask
from flask import render_template, redirect, request
from gmail_service import build_gmail_service
import gmail_credential, gmail_service, gmail_api
import os


app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a our landing page."""
    return render_template("index.html")

# Callback after gmail auth is executed. 
@app.route('/authcallback')
def authcallback():
	authorization_code = request.args.get('code', 'error')
	credentials = gmail_credential.get_credentials(authorization_code, "200")
	gmail_service = build_gmail_service(credentials)
	return gmail_api.getFirstMessage(gmail_service, "me")

# Haven't implemented user credential's storage. Currently only redirect to gmail auth page.
# Todo: call get_stored_credentials(user_id) first. If credential is not present, raise an 
# exception which redirect user to gmail auth page
@app.route('/auth/gmail')
def gmail_auth():
	return redirect(gmail_credential.get_authorization_url('', '200'))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

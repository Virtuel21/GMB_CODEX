import json
import os

from flask import Flask, redirect, url_for, session, request, render_template
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'change-me')

SCOPES = ['https://www.googleapis.com/auth/business.manage']
CLIENT_SECRETS_FILE = os.environ.get('GOOGLE_CLIENT_SECRETS', 'client_secret.json')

@app.route('/')
def index():
    creds_info = session.get('creds')
    if not creds_info:
        return render_template('login.html')

    creds = Credentials.from_authorized_user_info(json.loads(creds_info), SCOPES)

    account_mgmt = build('mybusinessaccountmanagement', 'v1', credentials=creds)
    accounts = account_mgmt.accounts().list().execute()
    account_name = accounts.get('accounts', [{}])[0].get('name')

    biz_info = build('mybusinessbusinessinformation', 'v1', credentials=creds)
    locations = []
    if account_name:
        resp = biz_info.accounts().locations().list(parent=account_name, readMask='name,title,storefrontAddress').execute()
        locations = resp.get('locations', [])

    return render_template('dashboard.html', locations=locations)

@app.route('/login')
def login():
    if os.path.exists(CLIENT_SECRETS_FILE):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=url_for('oauth2callback', _external=True))
    else:
        client_config = {
            'web': {
                'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
                'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=url_for('oauth2callback', _external=True))
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    if os.path.exists(CLIENT_SECRETS_FILE):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            state=state,
            redirect_uri=url_for('oauth2callback', _external=True))
    else:
        client_config = {
            'web': {
                'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
                'client_secret': os.environ.get('GOOGLE_CLIENT_SECRET'),
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
        }
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            state=state,
            redirect_uri=url_for('oauth2callback', _external=True))

    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    session['creds'] = creds.to_json()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

# ============== CONFIG PARAMETERS
from config import EMAIL
# ============== INTERNAL LIBRARIES
# ============== EXTERNAL LIBRARIES
import httplib2
import os
import base64
from __future__ import print_function
from apiclient import discovery, errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.MIMEText import MIMEText

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GMAIL API Python Quickstart'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                    .execute())
        print("Message Id: " + str(message['id']))
        return message
    except errors.HttpError, error:
        print('An error occurred: ' + str(error))

def sendGmail(mail_to, mail_subject, mail_body):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    sender = EMAIL
    to = mail_to
    subject = mail_subject
    message_text = mail_body
    compose_message = create_message(sender=sender, to=to, subject=subject, message_text=message_text)
    send_message(service = service, user_id='me', message=compose_message)

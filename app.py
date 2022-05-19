from flask import Flask
import os
from twilio.rest import Client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import time

app = Flask(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
#SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


"""Shows basic usage of the Gmail API.
Lists the user's Gmail messages.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time..
if os.path.exists('token.json'):
     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'wcredentials.json', SCOPES)
        creds = flow.run_local_server(port=0)


    # Save the credentials for the next run.
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)
########################################################
        
results = service.users().messages().list(userId='me', labelIds=['INBOX'], q = "is:unread").execute()
messages = results.get('messages', [])
unread_msg_count = len(messages)

while True:
    unread_msg_count

    print("in loop",unread_msg_count)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q = "is:unread").execute()
    messages = results.get('messages', [])
    if len(messages) > unread_msg_count:
        print("in if")
        account_sid = 'ACeb44a0298b6deaadede4ce06127a52fd'
        auth_token = '7eb76f91164dc2c0b9402fc982389ce7'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
                        body=f"_*Sir Jahanzaib*_! You have *{len(messages)}* Unread Emails📧.\nReply With *\"Check\"* to check them.",
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+923168838332'
                    )

        print("Msg Sent!")
        unread_msg_count = len(messages)

    print('out of if lopping',unread_msg_count)
    time.sleep(10)

# sched1 = BackgroundScheduler(daemon=True)
# sched.add_job(new_mail_checker,'interval', seconds=10)
# sched.start()
        
#thread = threading.Thread(target=new_mail_checker)
#p = Process(target=new_mail_checker)
@app.route("/reset")
def reset_unreadMsg():
    global unread_msg_count
    unread_msg_count = 0

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

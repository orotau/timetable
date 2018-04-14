from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import pprint

PERIOD_TEXT = "Period"

# Setup the Calendar API (Boiler Plate)
SCOPES = 'https://www.googleapis.com/auth/calendar' # read / write
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Get all events in the primary calendar
all_events = [] # a list, built up in lots of 250. Each list item is a dict
page_token = None
while True:
    events_lot = service.events().list(calendarId='primary', pageToken=page_token).execute() # a dict
    for event in events_lot["items"]:
        all_events.append(event) 

    page_token = events_lot.get('nextPageToken')
    if page_token is None:
        break

for event in all_events: #list of dictionaries
    if PERIOD_TEXT in event['summary']:
        print(event['start']['dateTime'], event['summary'])

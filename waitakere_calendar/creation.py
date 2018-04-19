from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime, date
import pprint
import numpy as np
import y2018 # can't name a module 2018
import utils
from dateutil.rrule import rrule, DAILY
from itertools import compress, cycle, islice
import iso8601 #http://pyiso8601.readthedocs.io/en/latest/

PERIOD_TEXT = "Period"

# Setup the Calendar API (Boiler Plate)
SCOPES = 'https://www.googleapis.com/auth/calendar' # read / write
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

event = {
  'summary': 'Period 1 - Line 2',
  #'transparency':'transparent', # if you want this to appear Free
  'start': {
    #'date':'2018-04-19',
    'dateTime': '2018-04-19T09:00:00',
    'timeZone': 'Pacific/Auckland',
  },
  'end': {
    #'date':'2018-04-19',
    'dateTime': '2018-04-19T17:00:00',
    'timeZone': 'Pacific/Auckland',
  },
  'reminders': {
    'useDefault':'False',
  },
}

#conferenceDataVersion = 1 removes any conference data (found by trial and error)
event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
pprint.pprint (event)

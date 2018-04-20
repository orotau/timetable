from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pprint
import urllib.parse
import urllib.request
from urllib.error import URLError

PART1_OF_ICS_URL = "https://calendar.google.com/calendar/ical/"
PART3_OF_ICS_URL = "/public/basic.ics"

# Setup the Calendar API (Boiler Plate)
SCOPES = 'https://www.googleapis.com/auth/calendar' # read / write
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# get the ids and names of each calendar
calendars = []

page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token, showHidden=True).execute()
  for calendar_list_entry in calendar_list['items']:
    calendars.append(calendar_list_entry)
    pprint.pprint(calendar_list_entry)
  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    break

# create the .ics url for each calendar and try to access it

# this is an example of a calendar id
'waitakerecollege.school.nz_fpkm359st1lb3a65mjcavt0c1g@group.calendar.google.com'

# this is an example of an .ics url split over 3 lines for clarity
'''
https://calendar.google.com/calendar/ical/waitakerecollege.school.nz
_fpkm359st1lb3a65mjcavt0c1g%40
group.calendar.google.com/public/basic.ics


for calendar in calendars:
    ics_url_parsed = PART1_OF_ICS_URL + urllib.parse.quote(calendar['id']) + PART3_OF_ICS_URL
    request = urllib.request.Request(ics_url_parsed)

    try:
        response = urllib.request.urlopen(request)
    except:
        # unable to reach the .ics file so can't back up
        print("CAN'T BACK UP ", calendar['summary'])
    else:
        print("backing up ", calendar['summary'])
'''

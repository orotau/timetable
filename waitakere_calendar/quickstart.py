from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import pprint
import y2018 # can't name a module 2018
from dateutil.rrule import rrule, DAILY

PERIOD_TEXT = "Period"

# Setup the Calendar API (Boiler Plate)
SCOPES = 'https://www.googleapis.com/auth/calendar' # read / write
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Get all periods in the primary calendar
def get_all_periods_in_primary_calendar():
    all_events = [] # a list, built up in lots of 250. Each list item is a dict
    page_token = None
    while True:
        events_lot = service.events().list(calendarId='primary', pageToken=page_token).execute() # a dict
        for event in events_lot["items"]:
            all_events.append(event) 

        page_token = events_lot.get('nextPageToken')
        if page_token is None:
            break

    periods = [x for x in all_events if PERIOD_TEXT in x['summary']]
    return periods

def get_dates_and_days_for_term(term):
    pass

#for period_event in period_events: #list of dictionaries
#        print(period_event['start']['dateTime'], period_event['summary'])

#print (len(period_events))

if __name__ == '__main__':

    import sys
    import argparse
    import ast
    import pprint

    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # create the parser for the get_all_periods_in_primary_calendar
    get_all_periods_in_primary_calendar_parser = subparsers.add_parser('get_all_periods_in_primary_calendar')
    get_all_periods_in_primary_calendar_parser.set_defaults(function = get_all_periods_in_primary_calendar)

    # parse the arguments
    arguments = parser.parse_args()
    arguments = vars(arguments) #convert from Namespace to dict

    #attempt to extract and then remove the function entry
    try:
        function_to_call = arguments['function'] 
    except KeyError:
        print ("You need a function name. Please type -h to get help")
        sys.exit()
    else:
        #remove the function entry as we are only passing arguments
        del arguments['function']
    
    if arguments:
        #remove any entries that have a value of 'None'
        #We are *assuming* that these are optional
        #We are doing this because we want the function definition to define
        #the defaults (NOT the function call)
        arguments = { k : v for k,v in arguments.items() if v is not None }

        #alter any string 'True' or 'False' to bools
        arguments = { k : ast.literal_eval(v) if v in ['True','False'] else v 
                                              for k,v in arguments.items() }       

    result = function_to_call(**arguments) #note **arguments works fine for empty dict {}
   
    pprint.pprint (result)

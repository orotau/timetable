from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import pprint
import numpy as np
import y2018 # can't name a module 2018
from dateutil.rrule import rrule, DAILY
from itertools import compress, cycle, islice

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

def get_teaching_dates_for_term(term):
    start_date = [x.dayte for x in y2018.tdls if x.term == term][0] # as string
    start_date = datetime.strptime(start_date, '%A %d %B %Y')

    end_date = [x.dayte for x in y2018.tdls if x.term == term][-1] # as string
    end_date = datetime.strptime(end_date, '%A %d %B %Y')

    all_dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

    # as string
    no_school_dates = [x.dayte for x in y2018.tdls if x.term == term and x.line == 0]

    # as datetime object
    no_school_dates = [datetime.strptime(x, '%A %d %B %Y') for x in no_school_dates]

    teaching_dates_filter = np.is_busday(all_dates, holidays=no_school_dates)
    teaching_dates = list(compress(all_dates, teaching_dates_filter))
    return teaching_dates

def get_teaching_dates_and_day_number(term):
    '''
    get teaching dates and day number for term
    '''
    teaching_dates_and_day_number = []
    teaching_dates = get_teaching_dates_for_term(term)
    start_line = [x.line for x in y2018.tdls if x.term == term][0]
    lines = cycle([1, 2, 3, 4, 5, 6]) 
    adjusted_lines = islice(lines, start_line - 1, None)
    for teaching_date in teaching_dates:
        line_to_use = next(adjusted_lines)
        teaching_dates_and_day_number.append((teaching_date, line_to_use))
    return teaching_dates_and_day_number
    

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

    # create the parser for the get_teaching_dates_for_term
    get_teaching_dates_for_term_parser = subparsers.add_parser('get_teaching_dates_for_term')
    get_teaching_dates_for_term_parser.add_argument('term', type=int, choices = [1, 2, 3, 4])
    get_teaching_dates_for_term_parser.set_defaults(function = get_teaching_dates_for_term)

    # create the parser for the get_teaching_dates_and_day_number
    get_teaching_dates_and_day_number_parser = subparsers.add_parser('get_teaching_dates_and_day_number')
    get_teaching_dates_and_day_number_parser.add_argument('term', type=int, choices = [1, 2, 3, 4])
    get_teaching_dates_and_day_number_parser.set_defaults(function = get_teaching_dates_and_day_number)

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

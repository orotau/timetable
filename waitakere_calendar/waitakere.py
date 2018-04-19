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
    start_date = [x.dayte for x in y2018.tdd_ns if x.term == term][0] # as string
    start_date = datetime.strptime(start_date, '%A %d %B %Y')

    end_date = [x.dayte for x in y2018.tdd_ns if x.term == term][-1] # as string
    end_date = datetime.strptime(end_date, '%A %d %B %Y')

    all_dates = list(rrule(DAILY, dtstart=start_date, until=end_date))

    # as string
    no_school_dates = [x.dayte for x in y2018.tdd_ns if x.term == term and x.day_number == 0]

    # as datetime object
    no_school_dates = [datetime.strptime(x, '%A %d %B %Y') for x in no_school_dates]

    teaching_dates_filter = np.is_busday(all_dates, holidays=no_school_dates)
    teaching_dates = list(compress(all_dates, teaching_dates_filter))
    teaching_dates = [x.date() for x in teaching_dates] # convert to dates from datetimes
    return teaching_dates

def get_teaching_dates_and_day_number(term):
    '''
    get teaching dates and day number for term
    '''
    teaching_dates_and_day_number = []
    teaching_dates = get_teaching_dates_for_term(term)

    start_day_number = [x.day_number for x in y2018.tdd_ns if x.term == term][0]
    day_numbers = cycle([1, 2, 3, 4, 5, 6]) 
    adjusted_day_numbers = islice(day_numbers, start_day_number - 1, None)
    for teaching_date in teaching_dates:
        day_number_to_use = next(adjusted_day_numbers)
        teaching_dates_and_day_number.append((teaching_date, day_number_to_use))
    return teaching_dates_and_day_number

def get_periods_for_line(term, line):
    periods_for_line = []
    all_periods = get_all_periods_in_primary_calendar()
    teaching_dates_and_day_number = get_teaching_dates_and_day_number(term)
    for teaching_date, day_number in teaching_dates_and_day_number:
        periods_for_teaching_date = []
        for period in all_periods:
            # get the 5 periods for that teaching_date
            start_datetime = iso8601.parse_date(period['start']['dateTime'])
            start_date = start_datetime.date()
            if start_date == teaching_date:
                periods_for_teaching_date.append(period)
        assert len(periods_for_teaching_date) == 5 # check
        # we have the 5 periods (events in the calendar) for the teaching date
        period_for_line = utils.get_period_for_line(day_number, line)
        if period_for_line is None:
            pass # do nothing as there is no period on that day that covers the line
        else:
            for period in periods_for_teaching_date:
                if period['summary'].endswith(str(period_for_line)):
                    periods_for_line.append(period)
                    break

    periods_for_line.sort(key=lambda e: iso8601.parse_date(e['start']['dateTime']))
    return periods_for_line

def update_color_for_line(term, line):

    '''
    Given the term and the line updates the color of the periods (if required)
    See https://github.com/orotau/timetable/blob/development/google_calendar_event_colors.PNG

    Basically following a rainbow
    Red - Line 1
    Orange - Line 2
    Yellow - Line 3
    Green - Line 4
    Blue - Line 5
    Indigo/Violet - Line 6
    '''

    LINE_COLOR_IDS = {}
    # LINE_COLOR_IDS[1] = "11"    # Tomato
    LINE_COLOR_IDS[1] = "8"    # Graphite (used specifically for me)
    # LINE_COLOR_IDS[2] = "6"      # Tangerine
    LINE_COLOR_IDS[2] = "8"    # Graphite (used specifically for me)
    LINE_COLOR_IDS[3] = "5"      # Banana (Room 2 in 2018)
    LINE_COLOR_IDS[4] = "10"    # Basil (Maths in 2018)
    LINE_COLOR_IDS[5] = "7"      # Peacock (Topic in 2018)
    # LINE_COLOR_IDS[6] = "3"      # Grape
    LINE_COLOR_IDS[6] = "8"    # Graphite (used specifically for me)

    periods_for_line = get_periods_for_line(term, line)
    color_id_to_use = LINE_COLOR_IDS[line]
    
    for period in periods_for_line:
        change_color_id = False
        add_color_id = False
        try:
            if period["colorId"] != color_id_to_use:
                # the colorId exists but we want to change it
                change_color_id = True
        except KeyError:
            # the colorId key does not exist in the event dictionary
            add_color_id = True 
        finally:
            if change_color_id or add_color_id:
                period["colorId"] = color_id_to_use
                updated_event = service.events().update(calendarId='primary', eventId=period['id'], body=period).execute()
    

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

    # create the parser for the get_periods_for_line
    get_periods_for_line_parser = subparsers.add_parser('get_periods_for_line')
    get_periods_for_line_parser.add_argument('term', type=int, choices = [1, 2, 3, 4])
    get_periods_for_line_parser.add_argument('line', type=int, choices = [1, 2, 3, 4, 5, 6])
    get_periods_for_line_parser.set_defaults(function = get_periods_for_line)

    # create the parser for the update_color_for_line
    update_color_for_line_parser = subparsers.add_parser('update_color_for_line')
    update_color_for_line_parser.add_argument('term', type=int, choices = [1, 2, 3, 4])
    update_color_for_line_parser.add_argument('line', type=int, choices = [1, 2, 3, 4, 5, 6])
    update_color_for_line_parser.set_defaults(function = update_color_for_line)

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
   
    pprint.pprint(result)



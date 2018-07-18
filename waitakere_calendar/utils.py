def get_end_day_number(start_day_number, number_of_school_days):
    '''
    given the start day_number and the number of school days returns the end day_number

    The school days *do not* include holidays or weekends

    Here is a breakdown of the possible scenarios

    If number_of_school_days is an exact multiple of 6 then number of days left over = 0
    In this case .....
    Start_Day_Number 1 , End_Day_Number 6
    Start_Day_Number 2 , End_Day_Number 1
    Start_Day_Number 3 , End_Day_Number 2
    Start_Day_Number 4 , End_Day_Number 3
    Start_Day_Number 5 , End_Day_Number 4
    Start_Day_Number 6 , End_Day_Number 5

    If number of days left over = 1
    Start_Day_Number 1 , End_Day_Number 1
    Start_Day_Number 2 , End_Day_Number 2
    Start_Day_Number 3 , End_Day_Number 3
    Start_Day_Number 4 , End_Day_Number 4
    Start_Day_Number 5 , End_Day_Number 5
    Start_Day_Number 6 , End_Day_Number 6

    If number of days left over = 2
    Start_Day_Number 1 , End_Day_Number 2
    Start_Day_Number 2 , End_Day_Number 3
    Start_Day_Number 3 , End_Day_Number 4
    Start_Day_Number 4 , End_Day_Number 5
    Start_Day_Number 5 , End_Day_Number 6
    Start_Day_Number 6 , End_Day_Number 1

    If number of days left over = 3
    Start_Day_Number 1 , End_Day_Number 3
    Start_Day_Number 2 , End_Day_Number 4
    Start_Day_Number 3 , End_Day_Number 5
    Start_Day_Number 4 , End_Day_Number 6
    Start_Day_Number 5 , End_Day_Number 1
    Start_Day_Number 6 , End_Day_Number 2

    If number of days left over = 4
    Start_Day_Number 1 , End_Day_Number 4
    Start_Day_Number 2 , End_Day_Number 5
    Start_Day_Number 3 , End_Day_Number 6
    Start_Day_Number 4 , End_Day_Number 1
    Start_Day_Number 5 , End_Day_Number 2
    Start_Day_Number 6 , End_Day_Number 3

    If number of days left over = 5
    Start_Day_Number 1 , End_Day_Number 5
    Start_Day_Number 2 , End_Day_Number 6
    Start_Day_Number 3 , End_Day_Number 1
    Start_Day_Number 4 , End_Day_Number 2
    Start_Day_Number 5 , End_Day_Number 3
    Start_Day_Number 6 , End_Day_Number 4
'''

    cycles = divmod(number_of_school_days, 6)[0] # not used
    days_left_over = divmod(number_of_school_days, 6)[1]

    if days_left_over == 0:
        days_to_add = 5 # 6 - 1
    else:
        days_to_add = days_left_over - 1

    end_day_number_first_go = start_day_number + days_to_add

    if end_day_number_first_go > 6:
        end_day_number = divmod(end_day_number_first_go, 6)[1]
    else:
        end_day_number = end_day_number_first_go

    return end_day_number

def get_period_for_line(day_number, line_number):
    # given a day number and line number
    # return the period for that line number
    # if no period then return None

    day = {}
    day[1] = (1, 2, 3, 4, 5)
    day[2] = (6, 1, 2, 3, 4)
    day[3] = (5, 6, 1, 2, 3)
    day[4] = (4, 5, 6, 1, 2)
    day[5] = (3, 4, 5, 6, 1)
    day[6] = (2, 3, 4, 5, 6)

    if line_number not in day[day_number]:
        return None
    else:
        return day[day_number].index(line_number) + 1

def get_line_for_period(day_number, period):
    # given a day number and period
    # return the line for that period number

    day = {}
    day[1] = (1, 2, 3, 4, 5)
    day[2] = (6, 1, 2, 3, 4)
    day[3] = (5, 6, 1, 2, 3)
    day[4] = (4, 5, 6, 1, 2)
    day[5] = (3, 4, 5, 6, 1)
    day[6] = (2, 3, 4, 5, 6)

    return day[day_number][period - 1]


def get_color_for_line(line):

    '''
    given the line return the colorid
    See https://github.com/orotau/timetable/blob/development/google_calendar_event_colors.PNG

    Basically following a rainbow but too overwhelming if it is coloured like that
    Consequenty those lines in which I am not teaching are colored Graphite
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

    return LINE_COLOR_IDS[line]

def create_event(summary_text, colorId, start_datetime, end_datetime, new_calendar_id, service):
    event = {
      'summary': summary_text,
      'colorId': colorId,
      #'transparency':'transparent', # if you want this to appear Free
      'start': {
        'dateTime': start_datetime,
        'timeZone': 'Pacific/Auckland',
      },
      'end': {
        'dateTime': end_datetime,
        'timeZone': 'Pacific/Auckland',
      },
      'reminders': {
        'useDefault':'False',
      },
    }

    #conferenceDataVersion = 1 removes any conference data (found by trial and error)
    event = service.events().insert(calendarId=new_calendar_id, body=event, conferenceDataVersion=1).execute()
    return event

def create_all_day_event(summary_text, colorId, dayte, new_calendar_id, service):
    event = {
      'summary': summary_text,
      'colorId': colorId,
      #'transparency':'transparent', # if you want this to appear Free
      'start': {
        'date':dayte,
        'timeZone': 'Pacific/Auckland',
      },
      'end': {
        'date':dayte,
        'timeZone': 'Pacific/Auckland',
      },
      'reminders': {
        'useDefault':'False',
      },
    }

    #conferenceDataVersion = 1 removes any conference data (found by trial and error)
    event = service.events().insert(calendarId=new_calendar_id, body=event, conferenceDataVersion=1).execute()
    return event

import collections
from datetime import datetime
import numpy as np
import utils

'''
The purpose of this module is to contain
details of 
the FIRST teaching date of the term and its associated teaching_day_number
the LAST teaching date of the term and its associated teaching_day_number
for all 4 terms

The non teaching dates (both holidays and otherwise) for each term
'''
teaching_date = collections.namedtuple("teaching_date", "term dayte day_number")
teaching_dates = []

# term 1
teaching_dates.append(teaching_date(1, "Wednesday 07 February 2018", 1))
teaching_dates.append(teaching_date(1, "Friday 13 April 2018", 2))

# term 2
teaching_dates.append(teaching_date(2, "Monday 30 April 2018", 3))
teaching_dates.append(teaching_date(2, "Friday 06 July 2018", 2))

# term 3
teaching_dates.append(teaching_date(3, "Monday 23 July 2018", 3))
teaching_dates.append(teaching_date(3, "Friday 28 September 2018", 3))

# term 4
teaching_dates.append(teaching_date(4, "Monday 15 October 2018", 4))
teaching_dates.append(teaching_date(4, "Monday 10 December 2018", 1))


non_teaching_date = collections.namedtuple("non_teaching_date", "term dayte title")
non_teaching_dates = []

# term 1
non_teaching_dates.append(non_teaching_date(1, "Friday 02 March 2018", "Teacher Professional Learning Day"))
non_teaching_dates.append(non_teaching_date(1, "Friday 30 March 2018", "Good Friday"))
non_teaching_dates.append(non_teaching_date(1, "Monday 02 April 2018", "Easter Monday"))
non_teaching_dates.append(non_teaching_date(1, "Tuesday 03 April 2018", "Easter Tuesday"))

# term 2
non_teaching_dates.append(non_teaching_date(2, "Friday 01 June 2018", "Teacher Only Day"))
non_teaching_dates.append(non_teaching_date(2, "Monday 04 June 2018", "Queens Birthday"))

# term 3
non_teaching_dates.append(non_teaching_date(3, "Monday 03 September 2018", "Mid-Term Break"))

# term 4
non_teaching_dates.append(non_teaching_date(4, "Monday 22 October 2018", "Labour Day"))
non_teaching_dates.append(non_teaching_date(4, "Tuesday 11 December 2018", "Prizegiving"))
non_teaching_dates.append(non_teaching_date(4, "Wednesday 12 December 2018", "Big Day In"))
non_teaching_dates.append(non_teaching_date(4, "Thursday 13 December 2018", "Last Day of Year"))

# check the dates are formatted correctly
for each in teaching_dates:
     datetime.strptime(each.dayte, '%A %d %B %Y')

for each in non_teaching_dates:
     datetime.strptime(each.dayte, '%A %d %B %Y')

# check the end day_number is consistent with the start day_number for each term
for term_counter in [1, 2, 3, 4]:

        non_teaching_dates_for_term = [x.dayte for x in non_teaching_dates if x.term == term_counter] # as strings
        non_teaching_dates_for_term = [datetime.strptime(x, '%A %d %B %Y') for x in non_teaching_dates_for_term]

        # get the number of teaching days (inclusive) between the start of term and the end of term
        start_teaching_date_for_term = [x.dayte for x in teaching_dates if x.term == term_counter][0] # as string
        start_teaching_date_for_term = datetime.strptime(start_teaching_date_for_term, '%A %d %B %Y')

        end_teaching_date_for_term = [x.dayte for x in teaching_dates if x.term == term_counter][-1] # as string
        end_teaching_date_for_term = datetime.strptime(end_teaching_date_for_term, '%A %d %B %Y')

        teaching_days = np.busday_count( start_teaching_date_for_term, end_teaching_date_for_term, holidays = non_teaching_dates_for_term) + 1 # + 1 includes the end date
        print(term_counter, teaching_days)

        start_day_number = [x.day_number for x in teaching_dates if x.term == term_counter][0]
        expected_end_day_number = utils.get_end_day_number(start_day_number, teaching_days)
        actual_end_day_number = [x.day_number for x in teaching_dates if x.term == term_counter][-1]
        assert expected_end_day_number == actual_end_day_number

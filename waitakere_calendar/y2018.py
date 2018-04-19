import collections
from datetime import datetime
import numpy as np
import utils

'''
The purpose of this module is to contain
details of 
the first day of the term and its associated day_number
the last day of the term and its associated day_number
all weekdays where there is no day_number (because no school)

for all 4 terms
'''
tdd_n = collections.namedtuple("tdd_n", "term dayte day_number")

tdd_ns = []

# term 1
tdd_ns.append(tdd_n(1, "Wednesday 07 February 2018", 1))
tdd_ns.append(tdd_n(1, "Friday 02 March 2018", 0))
tdd_ns.append(tdd_n(1, "Friday 30 March 2018", 0))
tdd_ns.append(tdd_n(1, "Monday 02 April 2018", 0))
tdd_ns.append(tdd_n(1, "Tuesday 03 April 2018", 0))
tdd_ns.append(tdd_n(1, "Friday 13 April 2018", 2))

# term 2
tdd_ns.append(tdd_n(2, "Monday 30 April 2018", 3))
tdd_ns.append(tdd_n(2, "Friday 01 June 2018", 0))
tdd_ns.append(tdd_n(2, "Monday 04 June 2018", 0))
tdd_ns.append(tdd_n(2, "Friday 06 July 2018", 2))

# term 3
tdd_ns.append(tdd_n(3, "Monday 23 July 2018", 3))
tdd_ns.append(tdd_n(3, "Monday 03 September 2018", 0))
tdd_ns.append(tdd_n(3, "Friday 28 September 2018", 3))

# term 4
tdd_ns.append(tdd_n(4, "Monday 15 October 2018", 4))
tdd_ns.append(tdd_n(4, "Monday 22 October 2018", 0))
tdd_ns.append(tdd_n(4, "Monday 10 December 2018", 1))


# check the dates are formatted correctly
for each in tdd_ns:
     datetime.strptime(each.dayte, '%A %d %B %Y')

# check the end day_number is consistent with the start day_number for each term
for term_counter in [1, 2, 3, 4]:

        # as string
        no_school_dates = [x.dayte for x in tdd_ns if x.term == term_counter and x.day_number == 0]

        # as datetime object
        no_school_dates = [datetime.strptime(x, '%A %d %B %Y') for x in no_school_dates]

        # print(no_school_dates)

        # get the number of school days (inclusive) between the start of term and the end of term
        start_date = [x.dayte for x in tdd_ns if x.term == term_counter][0] # as string
        start_date = datetime.strptime(start_date, '%A %d %B %Y')

        end_date = [x.dayte for x in tdd_ns if x.term == term_counter][-1] # as string
        end_date = datetime.strptime(end_date, '%A %d %B %Y')

        school_days = np.busday_count( start_date, end_date, holidays = no_school_dates) + 1 # + 1 includes the end date
        print(term_counter, school_days)

        start_day_number = [x.day_number for x in tdd_ns if x.term == term_counter][0]
        expected_end_day_number = utils.get_end_day_number(start_day_number, school_days)
        actual_end_day_number = [x.day_number for x in tdd_ns if x.term == term_counter][-1]
        assert expected_end_day_number == actual_end_day_number

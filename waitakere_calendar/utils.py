def get_end_line(start_line, number_of_school_days):
    '''
    given the start line and the number of school days returns the end line

    The school days *do not* include holidays or weekends

    Here is a breakdown of the possible scenarios

    If number_of_school_days is an exact multiple of 6 then number of days left over = 0
    In this case .....
    Start 1 End 6
    Start 2 End 1
    Start 3 End 2
    Start 4 End 3
    Start 5 End 4
    Start 6 End 5

    If number of days left over = 1
    Start 1 End 1
    Start 2 End 2
    Start 3 End 3
    Start 4 End 4
    Start 5 End 5
    Start 6 End 6

    If number of days left over = 2
    Start 1 End 2
    Start 2 End 3
    Start 3 End 4
    Start 4 End 5
    Start 5 End 6
    Start 6 End 1

    If number of days left over = 3
    Start 1 End 3
    Start 2 End 4
    Start 3 End 5
    Start 4 End 6
    Start 5 End 1
    Start 6 End 2

    If number of days left over = 4
    Start 1 End 4
    Start 2 End 5
    Start 3 End 6
    Start 4 End 1
    Start 5 End 2
    Start 6 End 3

    If number of days left over = 5
    Start 1 End 5
    Start 2 End 6
    Start 3 End 1
    Start 4 End 2
    Start 5 End 3
    Start 6 End 4
'''

    cycles = divmod(number_of_school_days, 6)[0] # not used
    days_left_over = divmod(number_of_school_days, 6)[1]

    if days_left_over == 0:
        days_to_add = 5 # 6 - 1
    else:
        days_to_add = days_left_over - 1

    end_line_first_go = start_line + days_to_add

    if end_line_first_go > 6:
        end_line = divmod(end_line_first_go, 6)[1]
    else:
        end_line = end_line_first_go

    return end_line

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


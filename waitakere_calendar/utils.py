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


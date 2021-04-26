import csv
from datetime import datetime
from datetime import timedelta


def SecondsToTimeConverter(time):
    # If a time is negative, we take a sign and return it later for simpler calc.
    minus = False
    if time.total_seconds() < 0:
        minus = True
        time *= -1

    # Conversion
    total_hours = str(int(time.total_seconds() // 3600))
    residual_minutes = str(int((time.total_seconds() % 3600) // 60))
    residual_seconds = str(int(time.total_seconds() % 60))

    # Add 0/- before number to keep output standard. -3:7:53 -> -03:07:53
    if len(total_hours) == 1:
        total_hours = '0' + total_hours
    if len(residual_minutes) == 1:
        residual_minutes = '0' + residual_minutes
    if len(residual_seconds) == 1:
        residual_seconds = '0' + residual_seconds
    if minus:
        total_hours = '-' + total_hours

    return str(total_hours) + ':' + str(residual_minutes) + ':' + str(residual_seconds)


def SummaryTime(start_day_index, end_day_index, start_week_index, end_week_index,
                i, next_week, input_arr):
    time = input_arr[end_day_index[i]][0] - input_arr[start_day_index[i]][0]
    parameters = ''
    last_working_day_of_week = False
    weekly_working_time = timedelta(hours=0)
    standard_working_time = timedelta(hours=8)

    # Adding parameters
    if input_arr[end_day_index[i]][0].isoweekday() == 6 \
            or input_arr[end_day_index[i]][0].isoweekday() == 7:
        parameters += ' w'
    if time > timedelta(hours=9):
        parameters += ' ot'
    if time < timedelta(hours=6):
        parameters += ' ut'
    if input_arr[end_day_index[i]][1] != 'exit':
        parameters += ' i'
    if end_day_index[i] == start_day_index[i] and input_arr[end_day_index[i]][1] == 'exit':
        parameters += ' i'

    # Sum of time in job for the week
    for k in range(next_week):
        if end_day_index[i] == end_week_index[k]:
            s = start_day_index.index(start_week_index[k])
            last_working_day_of_week = True
            for r in range(s, i + 1):
                weekly_working_time += input_arr[end_day_index[r]][0] - input_arr[start_day_index[r]][0]
            standard_working_time *= i - s + 1
            standard_working_time = weekly_working_time - standard_working_time
            break

    weekly_working_time = SecondsToTimeConverter(weekly_working_time)
    standard_working_time = SecondsToTimeConverter(standard_working_time)

    if last_working_day_of_week:
        time = str(time) + parameters + ' ' + weekly_working_time + ' ' + standard_working_time
    else:
        time = str(time) + parameters
    return time


# Initial operations on the input
with open('input.csv', newline='') as csvfile:
    input_reader = csv.reader(csvfile, delimiter=';')

    next(input_reader)

    input_arr = [r for r in input_reader]

# Clearing the input
for i in range(len(input_arr)):
    input_arr[i][1] = input_arr[i][1].replace('Reader ', '')
    input_arr[i][0] = datetime.fromisoformat(input_arr[i][0].rstrip())

# Redundant row for easiest operations below
input_arr.append((datetime.fromisoformat('1111-11-11 00:00:00'), 'none', 'none'))

start_day_index = [0]
end_day_index = [-1]
next_day = 0
start_week_index = [0]
end_week_index = [-1]
next_week = 0

# Selecting indexes
for i in range(1, len(input_arr)):
    # Select first and last index of the day
    if input_arr[i - 1][0].date() != input_arr[i][0].date():
        start_day_index.append(end_day_index[next_day] + 1)
        end_day_index.append(i - 1)
        next_day += 1

    # Select index indicating first and last day of work in the week
    if input_arr[i - 1][0].isocalendar()[1] != input_arr[i][0].isocalendar()[1] \
            or input_arr[i - 1][0].isocalendar()[0] != input_arr[i][0].isocalendar()[0]:
        start_week_index.append(end_week_index[next_week] + 1)
        end_week_index.append(i - 1)
        next_week += 1

start_day_index.pop(0)
end_day_index.pop(0)
start_week_index.pop(0)
end_week_index.pop(0)

# print(start_day_index)
# print(end_day_index)
# print(start_week_index)
# print(end_week_index)

# Output
with open('result', 'w') as f:
    for i in range(next_day):
        print("Day", input_arr[start_day_index[i]][0].strftime('%Y-%m-%d'), 'Work',
              SummaryTime(start_day_index, end_day_index, start_week_index, end_week_index,
                          i, next_week, input_arr), file=f)

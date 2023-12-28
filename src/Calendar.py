# Example Dates
# print(type(df['Start Datetime'][10]))
#      2024-01-16 11:30:00+00:00 + 2024-01-16 13:30:00+00:00
# -->  2024-01-16  :  [ [11:30:00+00:00-13:30:00+00:00], [... ...] ]

# Algorithm Pseudo-code
# 1) Sort by date  (key)
# 2) Within each date, Sort by times (values)
# 3) Apply merge algo for all members

import os
import pandas as pd
import shelve
from contextlib import closing
# from typing import TypeVar


# Pythonic custom type hint to supercede Haskell arrow scheme
# T = TypeVar('T')


# class Calendar:
#     def __init__(self, csv_files):
#         self.csv_files = csv_files

# Convenience func solely reserved as helper in viewing created shelf on terminal
### sort_shelf :: {} -> {}
def sort_shelf(dic):
    sorted_shelf = {}
    for i, j in dic.items():
        sorted_shelf[i] = sorted(j)
    return sorted_shelf


### make_datetime_shelf :: pd.DataFrame -> shelf -> None
def make_datetime_shelf(df, db):
    for start_datetime, end_datetime in zip(df['Start Datetime'], df['End Datetime']):
        year_month_date = start_datetime[:10]
        # start_end_time  = start_datetime[11:] + '-' + end_datetime[11:]
        start_end_time  = [start_datetime[11:], end_datetime[11:]]

        if year_month_date in db:
            db[year_month_date].append(start_end_time)
        else:
            db[year_month_date] = [start_end_time]


### merge_time_conflict :: [[]] -> [[]]
def merge_time_conflict(intervals):
    while len(intervals) != 0:
        # Sort by start time
        sorted_intervals = sorted(intervals)
        # Initialise merged_intervals with the earliest meeting
        merged_intervals = [sorted_intervals[0]]

        for start_current_interval, end_current_interval in sorted_intervals:
            start_last_merged_interval, end_last_merged_interval = merged_intervals[-1]
            # If the current interval overlaps with the last merged interval, use the
            # later end time of the two to extend interval
            if (end_last_merged_interval >= start_current_interval):
                merged_intervals[-1] = [start_last_merged_interval,
                                       max(end_last_merged_interval,
                                           end_current_interval)]
            else:
                # Add the current interval since it doesn't overlap
                merged_intervals.append([start_current_interval, end_current_interval])

        return merged_intervals


def view_db(db):
    # Now sort linked list values of above dictionary for merge_time_conflict()
    db_sorted = sort_shelf(db)
    dates = list(db_sorted.keys())
    dates.sort()
    for date in dates:
        print(date, db_sorted[date])

def init_db():
    here = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))

    csv_files_Minseok = here('../resources/csv_files/RYUMinseok.csv')
    df1 = pd.read_csv(csv_files_Minseok, names=['Start Datetime', 'End Datetime','Info', 'Classroom'])

    csv_files_Jun = here('../resources/csv_files/ZHANGJun.csv')
    df2 = pd.read_csv(csv_files_Jun, names=['Start Datetime', 'End Datetime','Info', 'Classroom'])

    with closing(shelve.open('members_lessons.db', 'c', writeback=True)) as db:
        # Make dictionary of linked lists (in unsorted JIT order)
        make_datetime_shelf(df1, db)
        make_datetime_shelf(df2, db)
        view_db(db)

def merge_db():
    print("Merge database!")
    with closing(shelve.open('members_lessons.db', 'c', writeback=True)) as db:
        dates = list(db.keys())
        print("Length of dates: ", len(dates))
        for date in dates:
            db[date] = merge_time_conflict(db[date])
            print(date, db[date])
        view_db(db)


if __name__=="__main__":
    init_db()
    merge_db() # DEBUG: Why not printing anything at this stage ???


###########

## Just Minseok
# 2024-03-08 [['10:30:00+00:00', '12:30:00+00:00']]
# 2024-03-11 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-12 [['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']]
# 2024-03-14 [['09:30:00+00:00', '11:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-15 [['10:30:00+00:00', '12:30:00+00:00']]
# 2024-03-18 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-19 [['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']]
# 2024-03-21 [['09:30:00+00:00', '11:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-22 [['10:30:00+00:00', '12:30:00+00:00']]
# 2024-03-25 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-26 [['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']]
# 2024-03-28 [['09:30:00+00:00', '14:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-02-29 [['09:30:00+00:00', '11:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-01 [['10:30:00+00:00', '12:30:00+00:00']]
# 2024-03-04 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['15:00:00+0
#               0:00', '17:00:00+00:00']]
# 2024-03-05 [['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-07 [['09:30:00+00:00', '11:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]

## After adding Jun
# 2024-03-07 [['09:30:00+00:00', '11:30:00+00:00'], ['11:00:00+00:00', '13:00:00+00:00'], ['14:00:00+0
#               0:00', '15:00:00+00:00']]
# 2024-03-08 [['09:00:00+00:00', '11:00:00+00:00'], ['10:30:00+00:00', '12:30:00+00:00'], ['14:00:00+0
#               0:00', '16:00:00+00:00'], ['17:00:00+00:00', '18:00:00+00:00']]
# 2024-03-11 [['09:00:00+00:00', '10:00:00+00:00'], ['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+0
#               0:00', '13:30:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']
#               ]
# 2024-03-12 [['09:00:00+00:00', '12:00:00+00:00'], ['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+0
#               0:00', '16:00:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']
#               ]
# 2024-03-13 [['09:00:00+00:00', '11:00:00+00:00'], ['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+0
#               0:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00']
#               , ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-14 [['09:30:00+00:00', '11:30:00+00:00'], ['11:00:00+00:00', '13:00:00+00:00'], ['14:00:00+0
#               0:00', '15:00:00+00:00']]
# 2024-03-15 [['09:00:00+00:00', '11:00:00+00:00'], ['10:30:00+00:00', '12:30:00+00:00'], ['14:00:00+0
#               0:00', '16:00:00+00:00'], ['17:00:00+00:00', '18:00:00+00:00']]
# 2024-03-18 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-19 [['09:00:00+00:00', '12:00:00+00:00'], ['11:30:00+00:00', '13:30:00+00:00'], ['12:00:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']]
# 2024-03-20 [['09:00:00+00:00', '11:00:00+00:00'], ['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+00:00', '14:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-21 [['09:00:00+00:00', '11:00:00+00:00'], ['09:30:00+00:00', '11:30:00+00:00'], ['11:00:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-22 [['09:00:00+00:00', '11:00:00+00:00'], ['10:30:00+00:00', '12:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['17:00:00+00:00', '18:00:00+00:00']]
# 2024-03-25 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-26 [['09:00:00+00:00', '12:00:00+00:00'], ['11:30:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+00:00', '18:00:00+00:00']]
# 2024-03-27 [['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['13:00:00+00:00', '15:00:00+00:00'], ['15:00:00+00:00', '17:00:00+00:00']]
# 2024-03-28 [['09:30:00+00:00', '14:30:00+00:00'], ['11:00:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]

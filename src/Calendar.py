# Example Dates
# print(type(df['Start Datetime'][10]))
#      2024-01-16 11:30:00+00:00 + 2024-01-16 13:30:00+00:00
# -->  2024-01-16  :  [ [11:30:00+00:00-13:30:00+00:00], [... ...] ]

# Algorithm Pseudo-code
# 1) Sort by date  (key)
# 2) Within each date, Sort by times (values)
# 3) Apply merge algo for all members

import pandas as pd
import shelve
from contextlib import closing
# from typing import TypeVar


# T = TypeVar('T')


# Convenience func solely reserved for viewing created shelf on terminal
### sort_shelf :: {} -> {}
def sort_shelf(dic):
    sorted_shelf = {}
    for i, j in dic.items():
        sorted_shelf[i] = sorted(j)
    return sorted_shelf


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



def main():
    csv_files_Minseok = 'resources/csv_files/RYUMinseok.csv'
    df = pd.read_csv(csv_files_Minseok, names=['Start Datetime', 'End Datetime','Info', 'Classroom'])
    #df.to_csv('save_new_eg_file.csv')

    with closing(shelve.open('mydict.db', 'c', writeback=True)) as db:
        # Make dictionary of linked lists (in unsorted JIT order)
        make_datetime_shelf(df, db)

        # Now sort linked list values of above dictionary for merge_time_conflict()
        db_sorted = sort_shelf(db)
        dates = list(db_sorted.keys())
        dates.sort()
        for date in dates:
            print(date, db_sorted[date])


if __name__=="__main__":
    main()
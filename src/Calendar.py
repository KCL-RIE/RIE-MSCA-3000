'''
File Name    : Calendar.py
Author       : Minseok Ryu
Date Created : 25/12/2023
Version      : 1.2
Purpose      : Module handling interval merging

Algorithm Pseudo-code
1) Sort by date  (key)
2) Within each date, Sort by times (values)
3) Apply merge algo for all members
'''


import os
import pandas as pd
import shelve
from contextlib import closing


class Calendar:
    '''
    Collection of database handling methods for merging and viewing intervals.
    '''
    def __init__(self, csv_folder, mode='ALL'):
        '''
        Constructor.

        :param csv_folder: Directory pointing to where CSV files stored
        :param mode:      'ALL', 'ADMIN', or 'MANUAL'
        '''
        self.csv_folder = csv_folder
        self.mode       = mode


    def _sort_shelf(self, dic):
        '''
        _sort_shelf :: {} -> {}

        Convenience func solely reserved as helper in viewing created shelf on terminal.

        :param dic: Unsorted dictionary
        :return:    Sorted dictionary
        '''
        sorted_shelf = {}
        for i, j in dic.items():
            sorted_shelf[i] = sorted(j)
        return sorted_shelf

    def _make_datetime_shelf(self, df, db):
        '''
        _make_datetime_shelf :: pd.DataFrame -> shelf -> None

        Creates shelf database.

        :param df: CSV file data
        :param db: Shelf database
        :return:   Database of data : intervals
        '''
        for start_datetime, end_datetime in zip(df['Start Datetime'], df['End Datetime']):
            year_month_date =  start_datetime[:10]
            start_end_time  = [start_datetime[11:], end_datetime[11:]]

            if year_month_date in db:
                db[year_month_date].append(start_end_time)
            else:
                db[year_month_date] = [start_end_time]

    def _merge_time_conflict(self, intervals):
        '''
        merge_time_conflict :: [[]] -> [[]]

        Union of intervals.

        :param intervals: Start and End pair per participant's lecture / tutorial
        :return:          Merged intervals
        '''
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

    def _init_db_helper(self, df, db_name):
        '''
        _init_db_helper :: pd.DataFrame -> None

        Make dictionary of linked lists (in unsorted JIT order).

        :param df:      Start and End pair per participant's lecture / tutorial
        :param db_name: e.g 'members_lessons.db'
        :return:        Shelf created
        '''
        with closing(shelve.open(db_name, 'c', writeback=True)) as db:
            self._make_datetime_shelf(df, db)
            # self.console_view_db(db) # DEBUG MODE ONLY


    def init_db(self):
        '''
        init_db :: None -> None

        Wrapper around shelf database creation.
        '''
        if self.mode == 'ALL':
            self.init_db_all()
        elif self.mode == 'ADMIN':
            self.init_db_admin()
        elif self.mode == 'MANUAL':
            self.init_db_manual()
        else:
            print("ERROR: MODE NOT EXIST!")

    def init_db_all(self):
        '''
        init_db_all :: None -> None

        ./
        '''
        for dirpath, dirnames, filenames in os.walk(self.csv_folder):
            for filename in filenames:
                if filename.endswith('.csv'):
                    with open(os.path.join(dirpath, filename)) as f:
                        df = pd.read_csv(f, names=['Start Datetime', 'End Datetime','Info', 'Classroom'])
                        self._init_db_helper(df, 'members_lessons.db')

    def init_db_admin(self):
        '''
        init_db_admin :: None -> None

        ./
        '''
        pass

    def init_db_manual(self):
        '''
        init_db_manual :: None -> None

        ./
        '''
        pass


    def merge_db(self):
        '''
        merge_db :: None -> None

        Wrapper around interval merging.
        '''
        if self.mode == 'ALL':
            self.merge_db_all()
        elif self.mode == 'ADMIN':
            self.merge_db_admin()
        elif self.mode == 'MANUAL':
            self.merge_db_manual()
        else:
            print("ERROR: MODE NOT EXIST!")

    def merge_db_all(self):
        '''
        merge_db_all :: None -> None

        ./
        '''
        with closing(shelve.open('members_lessons.db', 'c', writeback=True)) as db:
            dates = list(db.keys())
            print("Length of dates: ", len(dates))
            for date in dates:
                db[date] = self.merge_time_conflict(db[date])
                # DEBUG MODE ONLY
                # print(date, db[date])

            # DEBUG MODE ONLY
            self.console_view_db(db)

    def merge_db_admin(self):
        '''
        merge_db_admin :: None -> None

        ./
        '''
        pass

    def merge_db_manual(self):
        '''
        merge_db_manual :: None -> None

        ./
        '''
        pass


    def console_view_db(self, db):
        '''
        console_view_db :: shelf -> None

        Display line-by-line console output of shelf database
        '''
        # Now sort linked list values of given shelf dict for merge_time_conflict()
        db_sorted = self._sort_shelf(db)
        dates = list(db_sorted.keys())
        dates.sort()
        for date in dates:
            print(date, db_sorted[date])


if __name__=="__main__":
    # TIP: https://pieriantraining.com/iterate-over-files-in-directory-using-python/
    fullpath_from_relpath = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
    csv_folder = fullpath_from_relpath('../resources/csv_files/')

    ca = Calendar(csv_folder)
    ca.init_db_all()
    ca.merge_db()


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

## After merging Minseok and Jun
# 2024-03-07 [['09:30:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-08 [['09:00:00+00:00', '12:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['17:00:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-11 [['09:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['14:00:00+0
#               0:00', '17:00:00+00:00']]
# 2024-03-12 [['09:00:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-13 [['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+00:00', '17:00:00+00:00']]
# 2024-03-14 [['09:30:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-15 [['09:00:00+00:00', '12:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['17:00:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-18 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['14:00:00+0
#               0:00', '17:00:00+00:00']]
# 2024-03-19 [['09:00:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-20 [['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+00:00', '17:00:00+00:00']]
# 2024-03-21 [['09:00:00+00:00', '13:00:00+00:00'], ['14:00:00+00:00', '15:00:00+00:00']]
# 2024-03-22 [['09:00:00+00:00', '12:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['17:00:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-25 [['10:00:00+00:00', '11:30:00+00:00'], ['12:30:00+00:00', '13:30:00+00:00'], ['14:00:00+0
#               0:00', '17:00:00+00:00']]
# 2024-03-26 [['09:00:00+00:00', '13:30:00+00:00'], ['14:00:00+00:00', '16:00:00+00:00'], ['16:30:00+0
#               0:00', '18:00:00+00:00']]
# 2024-03-27 [['09:00:00+00:00', '12:00:00+00:00'], ['13:00:00+00:00', '17:00:00+00:00']]
# 2024-03-28 [['09:30:00+00:00', '15:00:00+00:00']]
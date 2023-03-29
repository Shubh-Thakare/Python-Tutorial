# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:54:27 2020

@author: KESHAV KORHALE
"""

import sys
from numpy import empty
from program_1_dictionary_generation_and_filling import DictGeneration

class DataWrangling:

    """
       Checking of raw data and correcting it if something incorrct is
       found. There are 3 types of check for given data, first one is
       "count check" which gives information about missing values,
       second is "range check" which gives information about given data
       is within range or not. and third one is "duplicate check" which
       gives idea about some data is duplicate or not. and try to
       correct that with the help of appropriate method.
    """

    def __init__(self):

        # import class "Dict_Generation()"
        self.dictgeneration = DictGeneration()
        self.dict_main = self.dictgeneration.dict_main_()
        self.station_name = list(self.dict_main.keys())
        self.columnes = list(self.dict_main[self.station_name[0]].columns)

    def count_check(self):

        """To check some missing values are present or not."""

        # Decision matrix for count check.
        count_d_mat = empty(shape=[417, 14], dtype=int)
        length = 0

        for j in range(len(self.columnes)):
            for i in range(len(self.station_name)):
                row = self.station_name[i]
                df_column = self.dict_main[row][self.columnes[j]]
                df_column = df_column.drop(index='YRS')
                # count total values in column
                frequency = df_column.count()

                if 0 < frequency < 12:
                    length = length + 1
                    count_d_mat[i, j] = 0
                    print(self.station_name[i], "'s\t", self.columnes[j],
                          "column count is:\t", frequency)
                    sys.exit("Imputation of Data is required for",
                             "the above data")
                else:
                    count_d_mat[i, j] = 1

        #np.set_printoptions(threshold=np.inf)
        print("Count Decision matrix is as follows:\n")
        print(count_d_mat, "\n")
        print("\nNo of values of 'count' from 1 to 11 is :\t ", length, "\n")

        if length != 0:
            print("some missing values in ", length, " columns")
            sys.exit(" Imputation of Data is required for the given data")
        else:
            print("No missing values in given data for count_check\n")

    def range_check(self):

        """ To check some values are out of range or not. """

        # Decision matrix for range check.
        range_d_mat = empty(shape=[417, 14, 12], dtype=int)
        length = 0

        for i in range(417):

            for j in range(len(self.columnes)):

                row = self.station_name[i]
                df_column = self.dict_main[row][self.columnes[j]]
                df_column = df_column.drop(index='YRS')
                frequency = df_column.count()

                if any(self.columnes[j] == x for x in ['AC1', 'AC2', 'LC1',
                                                       'LC2']):

                    for k in range(12):
                        if 0 <= df_column[k] <= 8:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, " ,VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Cloud data is out of range")

                elif any(self.columnes[j] == x for x in ['DT1', 'DT2', 'HTM',
                                                         'LTM']):

                    for k in range(12):
                        if -89.2 <= df_column[k] <= 56.7:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, " ,VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Temperature data is out of",
                                     "range")

                elif any(self.columnes[j] == x for x in ['RH1', 'RH2']):

                    for k in range(12):
                        if 0.36 <= df_column[k] <= 100:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, " ,VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Relative humidity data is",
                                     "out of range")

                elif any(self.columnes[j] == x for x in ['AP1', 'AP2']):

                    for k in range(12):
                        if 310 <= df_column[k] <= 1083.8:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, " ,VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Atmospheric pressure data",
                                     "is out of range")

                elif any(self.columnes[j] == x for x in ['RFL']):

                    for k in range(12):
                        if 0 <= df_column[k] <= 26470:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, " ,VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Rainfall data is out of",
                                     "range")

                else:

                    for k in range(12):
                        if 0 <= df_column[k] <= 408:
                            range_d_mat[i, j, k] = 1
                        elif frequency == 0:
                            range_d_mat[i, j, k] = 1
                        else:
                            range_d_mat[i, j, k] = 0
                            length = length + 1
                            print(self.station_name[i], "\t", self.columnes[j],
                                  "\t ROW NO: ", k+1, ",VALUE:\t",
                                  df_column[k])
                            sys.exit("Above Input Wind speed data is out of",
                                     " range")

        #np.set_printoptions(threshold=np.inf)
        print("Range Decision matrix is as follows:\n")
        print(range_d_mat, "\n")
        print("\nNumber of values out of range is :\t ", length, "\n")

    def duplicate_check(self):

        """To check some dataframes, columns and rows are
           duplicated or not.
        """

        length_of_dup1 = 0
        # Decision matrix for duplicate check of dataframe.
        dup1_d_mat = empty(shape=[417, 417], dtype=int)

        for i in range(len(self.station_name)):
            row = self.station_name[i]
            df_of_i = self.dict_main[row]
            for j in range(len(self.station_name)):
                col = self.station_name[j]
                df_of_j = self.dict_main[col]
                if i == j:
                    dup1_d_mat[i, j] = 1
                elif df_of_i.equals(df_of_j):
                    dup1_d_mat[i, j] = 0
                    length_of_dup1 = length_of_dup1 + 1
                    print(self.station_name[j], "'s Dataframe is same as",
                          self.station_name[j], "'s Dataframe")
                    sys.exit("Delete the above duplicate dataframe.",
                             self.station_name[j], "'s Dataframe")
                else:
                    dup1_d_mat[i, j] = 1

        #np.set_printoptions(threshold=np.inf)
        print("Duplicate Dataframe's Decision matrix is as follows:\n")
        print("\n", dup1_d_mat, "\n")
        print("no_of_duplicate_dataframe : \t", length_of_dup1, "\n")


        # second case:check of duplications of columns in each stations

        length_of_dup2 = 0
        # Decision matrix for duplicate check of columns.
        dup2_d_mat = empty(shape=[417, 14, 14], dtype=int)

        for i in range(417):
            for j in range(len(self.columnes)):
                #row= station_name[i]
                df_j = self.dict_main[self.station_name[i]][self.columnes[j]]
                #df_column=df_column.drop(index='YRS')
                frequency = df_j.count()
                for k in range(len(self.columnes)):
                    # Renaming of variable to avoid maximum line length
                    dict_main = self.dict_main
                    df_k = dict_main[self.station_name[i]][self.columnes[k]]
                    if j == k:
                        dup2_d_mat[i, j, k] = 1
                    elif frequency == 0:
                        dup2_d_mat[i, j, k] = 1
                    elif df_j.equals(df_k):
                        dup2_d_mat[i, j, k] = 0
                        length_of_dup2 = length_of_dup2 + 1
                        print(self.station_name[i], "'s \t", self.columnes[j],
                              " column is same as", self.columnes[k],
                              "column\n")
                        #sys.exit("Above two columns are similar,"
                        #         "check that in database and correct it")
                    else:
                        dup2_d_mat[i, j, k] = 1

        #np.set_printoptions(threshold=np.inf)
        print("Duplicate column's Decision matrix is as follows:\n")
        print(dup2_d_mat, "\n")
        print("no_of_duplicate_column : \t", length_of_dup2, "\n")


        ## Third case :check of duplications of rows in each stations

        rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                "SEP", "OCT", "NOV", "DEC"]
        length_of_dup3 = 0
        # Decision matrix for duplicate check of rows.
        dup3_d_mat = empty(shape=[417, 12, 12], dtype=int)

        for i, name in enumerate(self.station_name):
            dff = self.dict_main[name]
            for j, month in enumerate(rows):
                frequency = dff.loc[month].count()
                for k, dup_month in enumerate(rows):
                    if j == k:
                        dup3_d_mat[i, j, k] = 1
                    elif frequency == 0:
                        dup3_d_mat[i, j, k] = 1
                    elif dff.loc[month].equals(dff.loc[dup_month]):
                        dup3_d_mat[i, j, k] = 0
                        length_of_dup3 = length_of_dup3 + 1
                        print(name, "'s \t", month, " row is same as",
                              dup_month, "row")
                        sys.exit("Above two rows are similar, check that",
                                 "in database and correct it")
                    else:
                        dup3_d_mat[i, j, k] = 1

        #np.set_printoptions(threshold=np.inf)
        print("Duplicate row's Decision matrix is as follows:\n")
        print(dup3_d_mat, "\n")
        print("no_of_duplicate_rows : \t", length_of_dup3, "\n")

if __name__ == "__main__":

    Wrangle = DataWrangling()
    Wrangle.count_check()
    Wrangle.range_check()
    Wrangle.duplicate_check()

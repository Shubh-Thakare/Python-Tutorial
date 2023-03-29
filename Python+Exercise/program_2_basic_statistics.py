# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:30:39 2020

@author: KESHAV KORHALE
"""
import pandas as pd
from tabulate import tabulate
from numpy import empty, append, zeros
from program_1_dictionary_generation_and_filling import DictGeneration
#import numpy as np

class BasicStatistics:
    """
        Creation of dataframe "No_of_yrs_df" and 3d array "final_array"
        of Basic Statistics."No_of_yrs_df" Dataframe gives information
        about number of station's data available for each year of every
        given property."final_array" gives information about Basic
        Statistics such as count, mean, standard deviation, min,
        median, max of every property of each station.
    """

    def __init__(self):

        # creating dataframe of project_data
        self.project_df = pd.read_csv("../Data/Project_File.csv", header=None)
        # creating dataframe of station_info_data
        self.station_df = pd.read_csv("../Template/Project_station_info.csv")
        # list of "weather stations" name
        self.station_name = self.station_df["Station name"].tolist()
        self.rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                     "SEP", "OCT", "NOV", "DEC", "YRS"]   # list of month name
         # list of property name as given below
        self.columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2",
                        "AC1", "AC2", "LC1", "LC2", "RFL", "WSD"]
        # import class "DictGeneration()"
        self.dictgeneration = DictGeneration()
        # Define "self.dict_main" from import class "DictGeneration()"
        self.dict_main = self.dictgeneration.dict_main_()

    def station_count_for_each_year(self):

        """
           returns "No_of_yrs_df" dataframe which consist of "years
           number" from 0 to 30  as row and "property name" as column.
        """
        # The below list will consist of lists of each property's total
        # no. of station count for year from 0 to 30.
        final_list_counts = []
    # The below list's elements will use for comparing with "YRS" value.
        no_of_yrs_list = [float(i) for i in range(1, 31)]

        for j in self.columns:
            # Creating list with starting value of each element as 0
            count_list = [0 for i in range(0, 31)]
            for i in range(417):
                ind = self.station_name[i]
                for k in range(0, 30):
                    if self.dict_main[ind].loc['YRS'][j] == no_of_yrs_list[k]:
                        count_list[k+1] = count_list[k+1]+1

            # To get the no.of stations for 0 years
            count_list[0] = 417-sum(count_list)
         # Every count_list in loop for each property j in self.columns.
            final_list_counts.append(count_list)

        main_rows = ["00", "01", "02", "03", "04", "05", "06", "07", "08",
                     "09"]
        rows = [str(i) for i in range(10, 31)]
        main_rows.extend(rows)
        rows = [i + "_yrs" for i in main_rows]

        dict_of_yrs = {}          # Dictionary for creating dataframe
        for i in range(14):
            col = self.columns[i]
            dict_of_yrs[col] = {}
            for j in range(31):
                row = rows[j]
                dict_of_yrs[col][row] = final_list_counts[i][j]

     # "no_of_yrs_df" Dataframe is created from "dict_of_yrs" Dictionary
        no_of_yrs_df = pd.DataFrame(dict_of_yrs)
        return no_of_yrs_df

    def basic_stat(self):

        """
           returns "final_array" which is 3d array, this array consist
           of Basic statistics of every property of each station.
        """

        main_array = empty(shape=[0, 417, 6])
        for j in self.columns:
            dict_df = {}          # Dictionary for creating dataframe
            for i in range(417):
                # Station name as key of dictionary
                st_i = self.station_name[i]
                dict_df[st_i] = {}
                for k in range(6):
                    df_column = self.dict_main[st_i][j]
         # "YRS" is eliminated from "df_column" to get basic stat.
                    df_column = df_column.drop(index='YRS')
                    dict_df[st_i][k] = df_column.describe(percentiles=[0.5])[k]
            # Dictionary converted into Dataframe
            dff = pd.DataFrame(dict_df).T
            # Dataframe converted into numpy array
            df_to_array = dff.to_numpy()
            reshape_array = df_to_array.reshape(1, 417, 6)
            main_array = append(main_array, reshape_array, axis=0)

        final_array = zeros(shape=(6, 417, 14))
        for i in range(6):
            for j in range(417):
                for k in range(14):
                    # Reshape of main array to final array
                    final_array[i, j, k] = round(main_array[k, j, i], 3)
        return final_array

if __name__ == "__main__":

    Stat_ = BasicStatistics()
    yrs_df = Stat_.station_count_for_each_year()
    #print(dict_of_yrs_df)
    print("\nStation_count_for_each_year for each property is as follows:\n")
    print(tabulate(yrs_df, headers=Stat_.columns, tablefmt='fancy_grid',
                   disable_numparse=True))
    Final_array = Stat_.basic_stat()
    print("\n Final array is as follows:\t\n", Final_array)

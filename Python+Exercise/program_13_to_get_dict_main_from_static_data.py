# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 07:04:03 2020

@author: KESHAV KORHALE
"""

import pandas as pd
from tabulate import tabulate

class DictGeneration:
    """
        Creation of dictionary, station name (weather station) as
        "key" and Dataframe as "value" of dictionary.
        Dataframe consist of property name as columns and month name as
        rows. Dataframe filled it's data from "Project_File.csv"
    """

    def __init__(self):

        # creating dataframe of project_data
        self.project_df = pd.read_csv("../run/Static_form_of_data.csv",
                                      index_col="station_name")
        self.station_df = self.project_df[["Latitude", "Longitude",
                                           "Absolute elevation",
                                           "Distance from Coast"]]

        #self.station_df.to_csv("../Template/Updated_Project_station_info.csv")
        self.station_name = list(self.project_df.index)
        self.rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                     "SEP", "OCT", "NOV", "DEC", "YRS"] # list of month name
        # list of property name as given below
        self.columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2",
                        "AC1", "AC2", "LC1", "LC2", "RFL", "WSD"]

    def dict_main_(self):


        """ Creating the main dictionary whose "key" is station name and
        "value" is dataframe and this dataframe is filled from the
        'Final_Project_File.csv' file. """

        dict_main = {}                           # Main dictionary

        for i in range(len(self.station_name)):

            dict_sub = {}         # Dictionary for creating dataframe
            key = self.station_name[i]
            for j in range(len(self.rows)):
                row = self.rows[j]
                dict_sub[row] = {}
                for k in range(len(self.columns)):
                    col = self.columns[k]
                    dict_sub[row][col] = self.project_df[col+ "_"+row][key]

            # Filled Dataframe is created from "dict_sub" Dictionary
            dict_sub_df = pd.DataFrame(dict_sub).T
            # Filled Dataframe assign as value for given station in main
            # dictionary
            dict_main[key] = dict_sub_df

        return dict_main

if __name__ == "__main__":

    Dict_Gen = DictGeneration()
    Station_name = Dict_Gen.station_name
    Dict_main = Dict_Gen.dict_main_()

    for m, n in enumerate(Station_name):
        print("Filled Dataframe for {} station is as follows".format(n))
        print("\nSTATION NAME\t: ", n, ",\t\tSERIAL NO\t:", m+1, "\n")
        print(tabulate(Dict_main[n], headers=Dict_Gen.columns,
                       tablefmt='fancy_grid'))
        print("\n")

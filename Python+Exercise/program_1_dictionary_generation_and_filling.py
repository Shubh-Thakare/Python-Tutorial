# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 13:02:03 2020

@author: KESHAV KORHALE
"""

import pandas as pd
from tabulate import tabulate

class DictGeneration:
    """
        Creation of empty dictionary, station name (weather station) as
        "key" and Dataframe as "value" of dictionary.
        Dataframe consist of property name as columns and month name as
        rows. Dataframe filled it's data from "Project_File.csv"
    """

    def __init__(self):

        # creating dataframe of project_data
        self.project_df = pd.read_csv("../Data/Project_File.csv", header=None)
        # creating dataframe of station_info_data
        self.station_df = pd.read_csv("../Template/Project_station_info.csv")
        # list of "weather stations"
        self.station_name = self.station_df["Station name"].tolist()
        self.rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                     "SEP", "OCT", "NOV", "DEC", "YRS"] # list of month name
        # list of property name as given below
        self.columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2"
                        , "AC1", "AC2", "LC1", "LC2", "RFL", "WSD"]

    def empty_dict(self):

        """
           Creating the empty dictionary whose "keys" are station names and
           whose "value" is empty Dataframe
        """

        dict_a = {}            # Dictionary for creating dataframe.

        for i in self.rows:
            dict_a[i] = {}
            for j in self.columns:
                dict_a[i][j] = 'NA'    # Assign every value as "NA".

        # Empty Dataframe created from dict_a Dictionary.
        dict_a_df = pd.DataFrame(dict_a).T
        empty_dict = {}            # Creating main empty dictionary
        for i in self.station_name:
            empty_dict[i] = dict_a_df
        return empty_dict

    def dict_main_(self):

        """
            Creating the main dictionary whose "key" is station name and
            "value" is dataframe and this dataframe is filled from the
            'Final_Project_File.csv' file.
        """

        dict_main = {}                           # Main dictionary

        for i in range(417):
            dict_sub = {}         # Dictionary for creating dataframe
            for j in range(1, 14):
                row = self.rows[j-1]
                dict_sub[row] = {}
                for k in range(1, 15):
                    col = self.columns[k-1]
                    dict_sub[row][col] = float(self.project_df[k][(17*i)+j])
            # Filled Dataframe is created from "dict_sub" Dictionary
            dict_sub_df = pd.DataFrame(dict_sub).T
            # Filled Dataframe assign as value for given station in main
            # dictionary
            dict_main[self.project_df[0][(17*i)]] = dict_sub_df


        return dict_main


if __name__ == "__main__":

    Dict_Gen = DictGeneration()
    Station_name = Dict_Gen.station_name
    Empty_dict = Dict_Gen.empty_dict()
    Dict_main = Dict_Gen.dict_main_()

    for m, n in enumerate(Station_name):
        print("Empty Dataframe for {} station is as follows".format(n))
        print("\nSTATION NAME\t: ", n, ",\t\tSERIAL NO\t:", m+1, "\n")
        print(tabulate(Empty_dict[n], headers=Dict_Gen.columns,
                       tablefmt='fancy_grid'))
        print("\n")

    for m, n in enumerate(Station_name):
        print("Filled Dataframe for {} station is as follows".format(n))
        print("\nSTATION NAME\t: ", n, ",\t\tSERIAL NO\t:", m+1, "\n")
        print(tabulate(Dict_main[n], headers=Dict_Gen.columns,
                       tablefmt='fancy_grid'))
        print("\n")

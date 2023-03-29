# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:18:04 2020

@author: KESHAV KORHALE
"""

import pandas as pd
from numpy import  array, zeros, round

class SpatialInterpolation:

    def __init__(self, datafile, stationfile):

        # creating dataframe of project datafile.
        self.project_df = pd.read_csv("../Data/"+datafile +".csv", header=None)
        # creating dataframe of station_info_data
        self.station_info_df = pd.read_csv("../Template/" + stationfile
                                           + ".csv", index_col="Station name")
        self.rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                     "SEP", "OCT", "NOV", "DEC", "YRS"]
        # list of property name
        self.columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2",
                        "AC1", "AC2", "LC1", "LC2", "RFL", "WSD"]


    def main_dict(self):


        """ Creating the main dictionary whose "key" is station name
            and "value" is dataframe and this dataframe is filled from
             the datafile.
        """

        self.dict_main = {}          # Main dictionary

        for i in range(417):
            dict_sub = {}      # Dictionary for creating dataframe
            for j in range(1, 14):
                row = self.rows[j-1]
                dict_sub[row] = {}
                for k in range(1, 15):
                    col = self.columns[k-1]
                    dict_sub[row][col] = float(self.project_df[k][(17*i)+j])
            # Filled Dataframe is created from "dict_sub" Dictionary
            dict_sub_df = pd.DataFrame(dict_sub).T
# Filled Dataframe is value for corresponding station in main dictionary
            self.dict_main[self.project_df[0][(17*i)]] = dict_sub_df

    def conversion_to_numpy_array(self, property_, month):

        """
           Given data is in dataframe, for further use it require to
           convert into numpy array format and before that the station
           whose data is avaiable for less span of time is rejected and
           remaining data is converted into array format.
        """
        # list of "weather stations"
        self.station_name = list(self.dict_main.keys())
        y_list = []
        rejected_stations = []
        # Renaming of variable to avoid maximum line  length
        stn = self.station_name

        for i in range(417):
            if self.dict_main[stn[i]][property_]["YRS"] > 24:

                y_list.append(self.dict_main[stn[i]][property_][month])
            else:
                rejected_stations.append(self.station_name[i])


        #  Drop the Stations whose data is for less than 25 years
        self.x_df = self.station_info_df.drop(index=rejected_stations)

        # Station data format converted to array from dataframe.
        self.x_array = self.x_df.to_numpy()
        self.final_x = round(self.x_array, decimals=2)
         # Property data format converted to array from dataframe.
        self.final_y = array(y_list)

    def normalize(self, property_, x_train, y_train, x_test, y_test):

        """ Normalization of data """

        self.norm_train_x = zeros(x_train.shape)
        self.norm_train_y = zeros(y_train.shape)
        self.norm_test_x = zeros(x_test.shape)
        self.norm_test_y = zeros(y_test.shape)
        lat_max, long_max, elev_max, coast_max = self.final_x.max(axis=0)
        y_max = self.final_y.max(axis=0)

        if any(property_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
            # Temperature data converted from celcius to kelvin.
            y_max = y_max + 273

        for i in range(len(x_train)):
            self.norm_train_x[i][0] = x_train[i][0]/lat_max
            self.norm_train_x[i][1] = x_train[i][1]/long_max
            self.norm_train_x[i][2] = x_train[i][2]/elev_max
            self.norm_train_x[i][3] = x_train[i][3]/coast_max
            if any(property_ == x for x in ['DT1', 'DT2', 'HT', 'LTM']):
                self.norm_train_y[i] = (y_train[i]+273)/y_max
            else:
                self.norm_train_y[i] = (y_train[i])/y_max

        for i in range(len(x_test)):
            self.norm_test_x[i][0] = x_test[i][0]/lat_max
            self.norm_test_x[i][1] = x_test[i][1]/long_max
            self.norm_test_x[i][2] = x_test[i][2]/elev_max
            self.norm_test_x[i][3] = x_test[i][3]/coast_max
            if any(property_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
                self.norm_test_y[i] = (y_test[i]+273)/y_max
            else:
                self.norm_test_y[i] = y_test[i]/y_max

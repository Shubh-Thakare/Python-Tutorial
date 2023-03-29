# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 07:15:31 2020

@author: KESHAV KORHALE
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

class GeoSpatialPlotting:

    """Geospatial Mapping of Weather Stations"""

    def __init__(self, datafile, stationfile):

        self.project_df = pd.read_csv("../Data/"+datafile+ ".csv",
                                      header=None)
        self.station_info_df = pd.read_csv("../Template/" + stationfile +".csv"
                                           , index_col="Station name")
        self.rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG",
                     "SEP", "OCT", "NOV", "DEC", "YRS"]
        # list of property name is given below
        self.columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2",
                        "AC1", "AC2", "LC1", "LC2", "RFL", "WSD"]


    def main_dict(self):

        """
           Creating the main dictionary whose "key" is station name and
           "value" is dataframe and this dataframe is filled from
           self.project_df
        """

        self.dict_main = {}
        for i in range(417):
            dict_sub = {}
            for j in range(1, 14):
                row = self.rows[j-1]
                dict_sub[row] = {}
                for k in range(1, 15):
                    col = self.columns[k-1]
                    dict_sub[row][col] = float(self.project_df[k][(17*i)+j])
            dict_sub_df = pd.DataFrame(dict_sub).T
            self.dict_main[self.project_df[0][(17*i)]] = dict_sub_df

    def station_segregation(self, property_):

        """
           Segregation of stations on the basis of how many years of
           data available for given station
        """

        below5 = {}
        below10 = {}
        below15 = {}
        below20 = {}
        below25 = {}


        station_name = list(self.dict_main.keys())

        self.list05 = []
        self.list10 = []
        self.list15 = []
        self.list20 = []
        self.list25 = []
        self.accepted_stations = []

        for i in range(417):
            if self.dict_main[station_name[i]][property_]["YRS"] > 24:
                self.accepted_stations.append(station_name[i])
            elif self.dict_main[station_name[i]][property_]["YRS"] > 19:
                self.list25.append(station_name[i])
            elif self.dict_main[station_name[i]][property_]["YRS"] > 14:
                self.list20.append(station_name[i])
            elif self.dict_main[station_name[i]][property_]["YRS"] > 9:
                self.list15.append(station_name[i])
            elif self.dict_main[station_name[i]][property_]["YRS"] > 4:
                self.list10.append(station_name[i])
            else:
                self.list05.append(station_name[i])


        for i in range(len(self.list05)):
            below5[self.list05[i]] = {}
        for i in range(len(self.list10)):
            below10[self.list10[i]] = {}
        for i in range(len(self.list15)):
            below15[self.list15[i]] = {}
        for i in range(len(self.list20)):
            below20[self.list20[i]] = {}
        for i in range(len(self.list25)):
            below25[self.list25[i]] = {}

        # Renaming of variable to avoid maximum line length
        dff = self.station_info_df
        for i in range(len(self.list05)):
            below5[self.list05[i]]["lat"] = dff["Latitude"][self.list05[i]]
            below5[self.list05[i]]["long"] = dff["Longitude"][self.list05[i]]
        for i in range(len(self.list10)):
            below10[self.list10[i]]["lat"] = dff["Latitude"][self.list10[i]]
            below10[self.list10[i]]["long"] = dff["Longitude"][self.list10[i]]
        for i in range(len(self.list15)):
            below15[self.list15[i]]["lat"] = dff["Latitude"][self.list15[i]]
            below15[self.list15[i]]["long"] = dff["Longitude"][self.list15[i]]
        for i in range(len(self.list20)):
            below20[self.list20[i]]["lat"] = dff["Latitude"][self.list20[i]]
            below20[self.list20[i]]["long"] = dff["Longitude"][self.list20[i]]
        for i in range(len(self.list25)):
            below25[self.list25[i]]["lat"] = dff["Latitude"][self.list25[i]]
            below25[self.list25[i]]["long"] = dff["Longitude"][self.list25[i]]

        self.below5 = pd.DataFrame(below5).T
        self.below10 = pd.DataFrame(below10).T
        self.below15 = pd.DataFrame(below15).T
        self.below20 = pd.DataFrame(below20).T
        self.below25 = pd.DataFrame(below25).T

    def stations_dropped(self):

        """
            The station whose data is available for less than 24 years
            are seperated from "StationInfo_DF" dataframe.
        """

        self.droper = []
        self.droper = self.list25.copy()
        self.droper.extend(self.list20)
        self.droper.extend(self.list15)
        self.droper.extend(self.list10)
        self.droper.extend(self.list05)

        # The below dataframe consist of only stations whose data is
        # available for more than 24 years.
        self.stationinfo_dropped_df = self.station_info_df.drop(self.droper
                                                                , axis=0)

    def geospatial_plot(self):

        """
           Plotting of stations location on map and differentiate them
           on the basis of how many years of data available for given
           station
        """

        # List of latitude values for accepted_stations
        lati = list(self.stationinfo_dropped_df.iloc[:, 0])
        # List of longitude values for accepted_stations
        longi = list(self.stationinfo_dropped_df.iloc[:, 1])

        world = gpd.read_file(r"..\Data\India_SHP\INDIA.shp")

        accepted_stations = pd.DataFrame({'Latitude': lati, 'Longitude': longi})
        station25 = pd.DataFrame({'Latitude': list(self.below25.lat),
                                  'Longitude': list(self.below25.long)})
        station20 = pd.DataFrame({'Latitude': list(self.below20.lat),
                                  'Longitude': list(self.below20.long)})
        station15 = pd.DataFrame({'Latitude': list(self.below15.lat),
                                  'Longitude': list(self.below15.long)})
        #station10 = pd.DataFrame({'Latitude': list(self.below10.lat),
        #                          'Longitude': list(self.below10.long)})
        station05 = pd.DataFrame({'Latitude': list(self.below5.lat),
                                  'Longitude': list(self.below5.long)})

        # Renaming of variable to avoid maximum line length
        acp_sta = accepted_stations
        geometry = gpd.points_from_xy(acp_sta.Longitude, acp_sta.Latitude)
        gdf_accepted = gpd.GeoDataFrame(accepted_stations, geometry=geometry)
        geometry = gpd.points_from_xy(station25.Longitude, station25.Latitude)
        gdf_25 = gpd.GeoDataFrame(station25, geometry=geometry)
        geometry = gpd.points_from_xy(station20.Longitude, station20.Latitude)
        gdf_20 = gpd.GeoDataFrame(station20, geometry=geometry)
        geometry = gpd.points_from_xy(station15.Longitude, station15.Latitude)
        gdf_15 = gpd.GeoDataFrame(station15, geometry=geometry)
        #geometry = gpd.points_from_xy(station10.Longitude, station10.Latitude)
        #gdf_10 = gpd.GeoDataFrame(station10, geometry=geometry)
        geometry = gpd.points_from_xy(station05.Longitude, station05.Latitude)
        gdf_05 = gpd.GeoDataFrame(station05, geometry=geometry)


        axx = world.plot(color='grey', edgecolor='black', figsize=(12, 18))

        gdf_accepted.plot(ax=axx, markersize=11, color="red", marker="o",
                          label="Accepted Weather Stations")
        gdf_25.plot(ax=axx, markersize=11, color="blue", marker="o",
                    label="years between 20 to 25")
        gdf_20.plot(ax=axx, markersize=11, color="yellow", marker="o",
                    label="years between 15 to 20")
        gdf_15.plot(ax=axx, markersize=11, color="green", marker="o",
                    label="years between 10 to 15")
        #gdf_10.plot(ax=axx, markersize=11, color="magenta", marker="o",
        #            label="years between 05 to 10")
        gdf_05.plot(ax=axx, markersize=11, color="orange", marker="o",
                    label="years between 00 to 05")


        plt.legend(prop={'size':12})
        # plt.savefig("../run/Graded_Weather_Stations.png", dpi = 500)
        plt.show()


if __name__ == "__main__":


    STATION_FILE = "Updated_Project_station_info"
    DATAFILE = "Project_File"
    PROPERTY_ = "DT1"
    print("\nGeospatial Mapping of Weather Stations is as follows  :\n")
    geoplot = GeoSpatialPlotting(DATAFILE, STATION_FILE)
    geoplot.main_dict()
    geoplot.station_segregation(PROPERTY_)
    geoplot.stations_dropped()
    geoplot.geospatial_plot()

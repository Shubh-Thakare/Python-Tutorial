# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:37:52 2020

@author: KESHAV KORHALE
"""

import pandas as pd

class CorrectionOfStationInfoFile:

    """
         Lat long in given file is in degree minute form and it require
         in decimal form for further purposes then conversion to
         decimal form of lat long is done by this class.
    """

    def __init__(self):

        # Creating dataframe of station_info_data
        data = pd.read_csv("../Template/Project_station_info.csv")
        self.station_name = data["Station name"].tolist()
        self.data = pd.read_csv("../Template/Project_station_info.csv",
                                index_col="Station name")
        self.data = self.data.drop(columns=["Index No.",
                                            "Elevation of wind instrument"])

    def degree_to_decimal(self):

        """A function that convert degree minute values into decimal"""

        for i in self.station_name:
            # Seperate only Degree value from latitude
            deg = float(self.data.loc[i]["Latitude"][:2])
       # Seperate minute value from latitude and convert it into decimal
            minute_to_decimal = float(self.data.loc[i]["Latitude"][3:])/60
            # Sum of degree and  "minute_to_decimal" value
            self.data.at[i, "Latitude"] = round(deg + minute_to_decimal, 2)
        for i in self.station_name:
            # Seperate only Degree value from Longitude
            deg = float(self.data.loc[i]["Longitude"][:2])
      # Seperate minute value from Longitude and convert it into decimal
            minute_to_decimal = float(self.data.loc[i]["Longitude"][3:])/60
            # Sum of degree and  "minute_to_decimal" value
            self.data.at[i, "Longitude"] = round(deg + minute_to_decimal, 2)

        self.data.to_csv("../Template/Updated_Project_station_info.csv")
        return self.data

if __name__ == "__main__":

    correction = CorrectionOfStationInfoFile()
    Deg_to_Decimal = correction.degree_to_decimal()
    print("\nConverted data written to file[Updated_Project_station_info.csv]",
          "in the Template directory \n")
    updated_file = Deg_to_Decimal
    print("Updated data is as follows:\n", updated_file)

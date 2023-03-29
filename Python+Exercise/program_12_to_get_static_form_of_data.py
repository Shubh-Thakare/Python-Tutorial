# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 12:48:56 2020

@author: KESHAV KORHALE
"""
import pandas as pd

# Input data files
project_df = pd.read_csv("../Data/Project_File.csv", header=None)
data = pd.read_csv("../Template/Updated_Project_station_info.csv")

station_name = data["Station name"].tolist()
rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
        "NOV", "DEC", "YRS"]
columns = ["AP1", "AP2", "DT1", "DT2", "HTM", "LTM", "RH1", "RH2", "AC1",
           "AC2", "LC1", "LC2", "RFL", "WSD"]
StationInfo_DF = pd.read_csv("../Template/Updated_Project_station_info.csv",
                             index_col="Station name")

dict_sub = {}
for i in range(417):
    row = station_name[i]
    dict_sub[row] = {}
    for j in range(13):
        month = rows[j]
        for k in range(14):
            prop = columns[k]
            dict_sub[row][prop+"_"+month] = float(project_df[k+1][(17*i)+j+1])
dict_sub_df = pd.DataFrame(dict_sub).T
final_df = StationInfo_DF.merge(dict_sub_df, left_index=True, right_index=True)
final_df = final_df.reset_index()
final_df = final_df.rename(columns={"index":"station_name"})
final_df = final_df.set_index(["station_name"])

print(final_df)
# final_df.to_csv("../run/Static_form_of_data.csv")

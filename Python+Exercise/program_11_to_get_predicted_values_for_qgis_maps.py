# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:14:48 2020

@author: KESHAV KORHALE
"""

import pandas as pd
from numpy import  array, zeros
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from program_6_spatial_interpolation_skeleton import SpatialInterpolation

STATION_FILE = "Station_info_for_prediction"  # Input data file
StationInfo_DF = pd.read_csv("../Template/" + STATION_FILE +
                             ".csv", index_col="Station name")

X_array = StationInfo_DF.to_numpy()
norm_X_array = zeros(X_array.shape)
lat_max, long_max, Elev_max, Coast_max = X_array.max(axis=0)

for i in range(len(X_array)):
    norm_X_array[i][0] = X_array[i][0]/lat_max
    norm_X_array[i][1] = X_array[i][1]/long_max
    norm_X_array[i][2] = X_array[i][2]/Elev_max
    norm_X_array[i][3] = X_array[i][3]/Coast_max
StationInfo_DF = StationInfo_DF.reset_index()

PROPERTY_ = "WSD"    # Name of property
rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
        "NOV", "DEC"]
prefix = ["_01_", "_02_", "_03_", "_04_", "_05_", "_06_", "_07_", "_08_",
          "_09_", "_10_", "_11_", "_12_"]
HYPERPARAMETER_FILE = "Windspeed_Hyperparameters_detail.csv"
df = pd.read_csv("../Run/Hyper_parameters/"+HYPERPARAMETER_FILE)
df = df.set_index(['property', 'month'])
df = df.drop("No_of_Support_Vectors", axis=1)
df[["epsilon"]] = df[["epsilon"]].round(8)
df[["E_In", "E_Out"]] = df[["E_In", "E_Out"]].round(2)
columns = ['property', 'month', 'kernel', 'gamma', 'C', 'epsilon', 'E_In',
           'E_Out', 'Train_data_size', 'Test_data_size']

for j in range(len(rows)):
    STATION_FILE = "Updated_Project_station_info"  # Input data file
    DATA_FILE = "Project_File"

    MONTH = rows[j]
    s_p = SpatialInterpolation(DATA_FILE, STATION_FILE)
    C = df["C"][PROPERTY_][MONTH]
    epsilon = df["epsilon"][PROPERTY_][MONTH]

    algo_obj = SVR(kernel='rbf', gamma="scale", C=C, epsilon=epsilon)

    s_p.main_dict()                  # Main Dictionary is imported
    s_p.conversion_to_numpy_array(PROPERTY_, MONTH)
    # Data splitted into train and test
    x_train, x_test, y_train, y_test = train_test_split(s_p.final_x,
                                                        s_p.final_y,
                                                        test_size=0.205,
                                                        random_state=0)
    Y_MAX = s_p.final_y.max(axis=0)
     # Normalization of splitted data
    s_p.normalize(PROPERTY_, x_train, y_train, x_test, y_test)

    # Training whole data
    algo_obj.fit(s_p.norm_train_x, s_p.norm_train_y)

    # Predication on final data
    norm_PTrain_Y_whole = array(algo_obj.predict(norm_X_array))

    PTrain_Y_whole = []
    for i in range(len(norm_PTrain_Y_whole)):

        if any(PROPERTY_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
            PTrain_Y_whole.append((norm_PTrain_Y_whole[i]*Y_MAX) - 273)

        else:
            PTrain_Y_whole.append(norm_PTrain_Y_whole[i]*Y_MAX)


    dff = pd.DataFrame({"PTrain_"+PROPERTY_: PTrain_Y_whole})
    dff[["PTrain_"+PROPERTY_]] = dff[["PTrain_"+PROPERTY_]].round(2)
    train = StationInfo_DF[["Latitude", "Longitude"]]
    final_dataframe = train.join(dff)
    print(final_dataframe)
    final_dataframe.to_csv("../Run/QGIS files for maps/"+ PROPERTY_+"/"
                           +prefix[j]+ PROPERTY_ + "_" + MONTH +
                           "_qgis_file.csv", index=False)
    print(MONTH)

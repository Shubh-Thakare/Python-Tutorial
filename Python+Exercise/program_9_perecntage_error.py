# -*- coding: utf-8 -*-
"""
Created on Sun May 24 08:52:01 2020

@author: KESHAV KORHALE
"""

from math import sqrt
import pandas as pd
from sklearn.svm import SVR
from numpy import array, zeros
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from program_6_spatial_interpolation_skeleton import SpatialInterpolation

HYPERPARAMETER_FILE = "Windspeed_Hyperparameters_detail.csv"
df = pd.read_csv("../Run/Hyper_parameters/"+HYPERPARAMETER_FILE)
df = df.set_index(['property', 'month'])
PROPERTY_ = "WSD"
rows = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT",
        "NOV", "DEC"]
E_In_percent = []
E_Out_percent = []

for j in rows:
    STATION_FILE = "Updated_Project_station_info"  # Input data file
    DATA_FILE = "Project_File"
    MONTH = j
    s_p = SpatialInterpolation(DATA_FILE, STATION_FILE)
    C = df["C"][PROPERTY_][j]
    epsilon = df["epsilon"][PROPERTY_][j]
    STATION_FILE = "Updated_Project_station_info"  # Input data file
    DATA_FILE = "Project_File"
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

    # Predication on train data
    s_p.norm_ptrain_y_whole = array(algo_obj.predict(s_p.norm_train_x))

    train_y_whole = []
    ptrain_y_whole = []

    print("Train values and their predicated values is as follows:\n")

    if any(PROPERTY_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
        In_Diff = zeros(len(s_p.norm_ptrain_y_whole))
        IN_SUM = 0
        for i in range(len(s_p.norm_train_y)):

            train_y_whole.append((s_p.norm_train_y[i]*Y_MAX - 273))
            ptrain_y_whole.append((s_p.norm_ptrain_y_whole[i]*Y_MAX - 273))
            if s_p.norm_train_y[i] == 0:
                In_Diff[i] = 0
            else:
                In_Diff[i] = (abs((s_p.norm_ptrain_y_whole[i]*Y_MAX) -
                                  (s_p.norm_train_y[i]*Y_MAX)))
                In_Diff[i] = (In_Diff[i] / s_p.norm_train_y[i]*Y_MAX)*100
            IN_SUM = IN_SUM + In_Diff[i]
        E_In_Percentage = IN_SUM / len(ptrain_y_whole)
        E_In_percent.append(E_In_Percentage)
        print("E_In_Percentage of ", MONTH, " :  ", E_In_Percentage)

    else:
        In_Diff = zeros(len(s_p.norm_ptrain_y_whole))
        IN_SUM = 0
        for i in range(len(s_p.norm_train_y)):

            train_y_whole.append(s_p.norm_train_y[i]*Y_MAX)
            ptrain_y_whole.append(s_p.norm_ptrain_y_whole[i]*Y_MAX)
            if s_p.norm_train_y[i] == 0:
                In_Diff[i] = 0
            else:
                In_Diff[i] = (abs((s_p.norm_ptrain_y_whole[i]*Y_MAX -
                                   (s_p.norm_train_y[i]*Y_MAX))))
                In_Diff[i] = (In_Diff[i] /(s_p.norm_train_y[i]*Y_MAX))*100

            IN_SUM += In_Diff[i]
        E_In_Percentage = IN_SUM / len(ptrain_y_whole)
        E_In_percent.append(E_In_Percentage)
        print("E_In_Percentage of ", MONTH, ":  ", E_In_Percentage)

    # In sample error
    e_in = mean_squared_error(train_y_whole, ptrain_y_whole)
    e_in = sqrt(e_in)
    print("\nIn sample error\t\tE_In\t:\t", e_in, "\n")

     # Predication on test data
    s_p.norm_ptest_y_whole = array(algo_obj.predict(s_p.norm_test_x))

    test_y_whole = []
    ptest_y_whole = []

    # print("Test values and their predicated values is as follows:\n")


    if any(PROPERTY_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
        Out_Diff = zeros(len(s_p.norm_ptest_y_whole))
        OUT_SUM = 0
        for i in range(len(s_p.norm_test_x)):

            test_y_whole.append(s_p.norm_test_y[i]*Y_MAX - 273)
            ptest_y_whole.append(s_p.norm_ptest_y_whole[i]*Y_MAX -273)
            if s_p.norm_test_y[i] == 0:
                Out_Diff[i] = 0
            else:
                Out_Diff[i] = (abs((s_p.norm_ptest_y_whole[i]*Y_MAX -
                                    (s_p.norm_test_y[i]*Y_MAX))))
                Out_Diff[i] = (Out_Diff[i] /
                               (s_p.norm_test_y[i]*Y_MAX))*100
            OUT_SUM += Out_Diff[i]
        E_Out_Percentage = OUT_SUM / len(ptest_y_whole)
        E_Out_percent.append(E_Out_Percentage)
        print("E_Out_Percentage of ", MONTH, ":  ", E_Out_Percentage)
    else:
        Out_Diff = zeros(len(s_p.norm_ptest_y_whole))
        OUT_SUM = 0
        for i in range(len(s_p.norm_test_x)):

            test_y_whole.append(s_p.norm_test_y[i]*Y_MAX)
            ptest_y_whole.append(s_p.norm_ptest_y_whole[i]*Y_MAX)
            if s_p.norm_test_y[i] == 0:
                Out_Diff[i] = 0
            else:
                Out_Diff[i] = abs((s_p.norm_ptest_y_whole[i]*Y_MAX -
                                   (s_p.norm_test_y[i]*Y_MAX)))
                Out_Diff[i] = (Out_Diff[i] / (s_p.norm_test_y[i]*Y_MAX))*100
            OUT_SUM += Out_Diff[i]
        E_Out_Percentage = OUT_SUM / len(ptest_y_whole)
        E_Out_percent.append(E_Out_Percentage)
        print("E_Out_Percentage of ", MONTH, ":  ", E_Out_Percentage)

    # Out of sample error
    E_Out = mean_squared_error(test_y_whole, ptest_y_whole)
    E_Out = sqrt(E_Out)
    print("\nOut of sample error\tE_Out\t:\t", E_Out, "\n")
df = df.reset_index()
E_In_df = pd.DataFrame({"E_In_%": E_In_percent})
E_In_df[["E_In_%"]] = E_In_df[["E_In_%"]].round(2)
E_Out_df = pd.DataFrame({"E_Out_%": E_Out_percent})
E_Out_df[["E_Out_%"]] = E_Out_df[["E_Out_%"]].round(2)
print(E_In_df, "\n")
print(E_Out_df)
## Run the below code only if there is no percentage error available in
## hyperparameter csv file
# dff = df.join(E_In_df)
# final_dataframe = dff.join(E_Out_df)
# print(final_dataframe)
# final_dataframe.to_csv("../Run/Hyper_parameters/"+Hyperparameter_file,
#                        index=False)

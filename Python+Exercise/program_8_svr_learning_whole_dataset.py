# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:26:03 2020

@author: KESHAV KORHALE
"""

from math import sqrt
import pandas as pd
from sklearn.svm import SVR
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from program_6_spatial_interpolation_skeleton import SpatialInterpolation

if __name__ == "__main__":

    STATION_FILE = "Updated_Project_station_info"  # Input data file
    DATA_FILE = "Project_File"    # Output data file
    PROPERTY_ = "LC2"
    MONTH = "DEC"

    # import class SpatialInterpolation
    s_p = SpatialInterpolation(DATA_FILE, STATION_FILE)
    EPSILON = 0.1
    C = 13
    algo_obj = SVR(kernel='rbf', gamma="scale", C=C, epsilon=EPSILON)

    s_p.main_dict()           # Main Dictionary is imported
    s_p.conversion_to_numpy_array(PROPERTY_, MONTH)
    # Data splitted into train and test
    x_train, x_test, y_train, y_test = train_test_split(s_p.final_x,
                                                        s_p.final_y,
                                                        test_size=0.205,
                                                        random_state=0)
    # Normalization of splitted data
    s_p.normalize(PROPERTY_, x_train, y_train, x_test, y_test)

    # Training whole data
    algo_obj.fit(s_p.norm_train_x, s_p.norm_train_y)
    print(len(y_train))
    print(len(y_test))
    print(algo_obj.n_support_)

    # Predication on train data
    s_p.norm_ptrain_y_whole = array(algo_obj.predict(s_p.norm_train_x))

    train_y_whole = []
    ptrain_y_whole = []

    print("Train values and their predicated values is as follows:\n")

    for i in range(len(s_p.norm_train_y)):
        if any(PROPERTY_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
            print(round((s_p.norm_train_y[i]*s_p.final_y.max(axis=0)) -
                        273, 3),
                  "\t", round((s_p.norm_ptrain_y_whole[i]*
                               s_p.final_y.max(axis=0)) - 273, 3))
            train_y_whole.append((s_p.norm_train_y[i]*
                                  s_p.final_y.max(axis=0)) - 273)
            ptrain_y_whole.append((s_p.norm_ptrain_y_whole[i]*
                                   s_p.final_y.max(axis=0)) - 273)

        else:
            print(round((s_p.norm_train_y[i]*s_p.final_y.max(axis=0)), 3),
                  "\t", round((s_p.norm_ptrain_y_whole[i]*
                               s_p.final_y.max(axis=0)), 3))
            train_y_whole.append(s_p.norm_train_y[i]*s_p.final_y.max(axis=0))
            ptrain_y_whole.append(s_p.norm_ptrain_y_whole[i]
                                  *s_p.final_y.max(axis=0))

    # In sample error
    e_in = mean_squared_error(train_y_whole, ptrain_y_whole)
    e_in = sqrt(e_in)
    print("\nIn sample error\t\tE_In\t:\t", e_in, "\n")

    # Predication on test data
    s_p.norm_ptest_y_whole = array(algo_obj.predict(s_p.norm_test_x))

    test_y_whole = []
    ptest_y_whole = []

    # print("Test values and their predicated values is as follows:\n")

    for i in range(len(s_p.norm_test_y)):

        if any(PROPERTY_ == x for x in ['DT1', 'DT2', 'HTM', 'LTM']):
            print(round((s_p.norm_test_y[i]*s_p.final_y.max(axis=0)) - 273, 3),
                  "\t", round((s_p.norm_ptest_y_whole[i]*
                               s_p.final_y.max(axis=0)) - 273, 3))
            test_y_whole.append(s_p.norm_test_y[i]*s_p.final_y.max(axis=0) -
                                273)
            ptest_y_whole.append(s_p.norm_ptest_y_whole[i]*
                                 s_p.final_y.max(axis=0) -273)
        else:
            print(round((s_p.norm_test_y[i]*s_p.final_y.max(axis=0)), 3), "\t",
                  round((s_p.norm_ptest_y_whole[i]*
                         s_p.final_y.max(axis=0)), 3))
            test_y_whole.append(s_p.norm_test_y[i]*s_p.final_y.max(axis=0))
            ptest_y_whole.append(s_p.norm_ptest_y_whole[i]*
                                 s_p.final_y.max(axis=0))
    print(s_p.final_y.min(axis=0))
    print(s_p.final_y.max(axis=0))

    # Out of sample error
    e_out = mean_squared_error(test_y_whole, ptest_y_whole)
    e_out = sqrt(e_out)
    print("\nOut of sample error\tE_Out\t:\t", e_out, "\n")

    ## Plotting of train data and their predicted values

    print("\nPlot of train data and their predicted values\n")
    fig = plt.figure(figsize=(24, 12))
    ax = plt.axes()
    list_1 = [x for x in range(1, len(train_y_whole)+1)]
    ax.plot(list_1, train_y_whole, 'p-', label='Train_Y_whole')
    ax.plot(list_1, ptrain_y_whole, 'p-', label='PTrain_Y_whole')
    ax.set_xlabel('Stations', fontsize=20)
    ax.set_ylabel('Clouds amounts in oktas of sky', fontsize=20)
    ax.set_ylim(0, 9)
    ax.legend(fontsize=0)
    ax.grid()
    plt.title("Train_Data_Plot", fontsize=24)
    plt.show()
    plt.close()

    ## Plotting of test data and their predicted values

    print("\nPlot of test data and their predicted values\n")
    fig = plt.figure(figsize=(18, 12))
    ax = plt.axes()
    list_1 = [x for x in range(1, len(test_y_whole)+1)]
    ax.plot(list_1, test_y_whole, 'p-', label='Test_X_whole')
    ax.plot(list_1, ptest_y_whole, 'p-', label='PTest_Y_whole')
    ax.set_xlabel('Stations', fontsize=20)
    ax.set_ylabel('Clouds amounts in oktas of sky', fontsize=20)
    ax.set_ylim(0, 9)
    ax.legend(fontsize=20)
    ax.grid()
    plt.title("Test_Data_Plot", fontsize=24)
    plt.show()
    plt.close()

    # Record maintainance of Hyperparameters

    df = pd.read_csv("../Run/Hyper_parameters/" +
                     "Low_clouds_evening_Hyperparameters_detail.csv")
    Data = [{'property':PROPERTY_, 'month': MONTH, 'kernel':'rbf',
             'gamma':"scale", 'C': C, 'epsilon': EPSILON, 'E_In':  e_in,
             'E_Out':e_out, 'No_of_Support_Vectors': algo_obj.n_support_,
             'Train_data_size': len(y_train), 'Test_data_size':len(y_test)}]
    df = df.append(Data)
    df = df.set_index(['property', 'month'])
    print(df)
    # df.to_csv("../Run/Hyper_parameters/" +
    #           "Low_clouds_evening_Hyperparameters_detail.csv")

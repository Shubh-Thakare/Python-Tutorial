# -*- coding: utf-8 -*-
"""
Created on Fri May  1 17:16:35 2020

@author: KESHAV KORHALE
"""

from numpy import arange
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.metrics import make_scorer, mean_squared_error
from sklearn.model_selection import GridSearchCV
from program_6_spatial_interpolation_skeleton import SpatialInterpolation

if __name__ == "__main__":


    STATION_FILE = "Updated_Project_station_info"  # Input data file
    DATA_FILE = "Project_File"    # Output data file
    PROPERTY_ = "LC2"
    MONTH = "DEC"

    # import class SpatialInterpolation
    s_p = SpatialInterpolation(DATA_FILE, STATION_FILE)

    s_p.main_dict()           # Main Dictionary is imported
    s_p.conversion_to_numpy_array(PROPERTY_, MONTH)
    # Data splitted into train and test
    x_train, x_test, y_train, y_test = train_test_split(s_p.final_x,
                                                        s_p.final_y,
                                                        test_size=0.205,
                                                        random_state=0)
    # Normalization of splitted data
    s_p.normalize(PROPERTY_, x_train, y_train, x_test, y_test)

    # To select the best parameter: minimum of mean_squared_error
    scorer = make_scorer(mean_squared_error, greater_is_better=False)

    # To fit the data use of SVR method
    svr = SVR(kernel='rbf', gamma='scale')

    c_range = list(arange(1, 50, 1))
    # Checking with different values of c
    # c_range=list(arange(14.5,15.5,0.1))
    # c_range = [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2]
    # c_range = [1.111,1.112,1.113,1.114,1.115,1.116,1.117,1.118]
    # c_range = [1.23,1.245,1.25,1.255,1.27,1.28]
    # c_range = list(arange(1,10,0.5))
    # c_range = [1.89,1.895,1.885]
    epsilon_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    # Checking with different values of epsilon
    # epsilon_range = list(arange(0.1,0.22 ,0.02))
    # epsilon_range = [0.0009695,0.0009699, 0.00097,0.000971, 0.00097005,
    #                  0.0009701,0.000985,0.00099,0.001]
    # epsilon_range = [0.0001,0.0002,0.0003,0.0004,0.0005,0.0006,0.0007,0.0008,
    #                  0.0009,0.001,0.0011,0.0012]
    # epsilon_range = [0.0013,0.0014,0.00145,0.0015,0.0016,0.0017,
    #                     0.0018,0.0019,0.002,0.0021,0.0022]
    # epsilon_range = [0.00144,0.00145,0.00146]

    param_grid = dict(epsilon=epsilon_range, C=c_range)
    # GridsearchCV method to get the best parameters of model.
    grid = GridSearchCV(svr, param_grid, cv=10, scoring=scorer)

    grid.fit(s_p.norm_train_x, s_p.norm_train_y)
    print(pd.DataFrame(grid.cv_results_)[["params", "mean_test_score",
                                          "rank_test_score"]])
    print("\nBest_score :\t", grid.best_score_)
    print("Best Parameters :\t", grid.best_params_, "\n")
 
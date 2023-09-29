import pandas as pd
import numpy as np
from helpers import Database
from helpers import bayesianPlayerStatsBeta
import random
import datetime
from helpers import standardizeTeamName
from helpers import monthToInt
from scipy.stats import t
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
from numpy.linalg import inv
import math
import pickle
import scipy.stats

def predictions(league):
    predictions = []
    train_pred = []
    train = pd.read_csv("./csv_data/" + league + "/train.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    xCols = []
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "_GP" not in col):
            xCols.append(col)
    y_train = train["Actual Spread"]
    y_test = test["Actual Spread"]
    test_OpenSpreads = test["Open Spread"]
    test_CloseSpreads = test["Close Spread"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    for p in model.predict(X_test):
        predictions.append(p)
    test["Predicted Spread"] = predictions
    for p in model.predict(X_train):
        train_pred.append(p)
    ones = []
    for i in range(len(X_train.index)):
        ones.append(1)
    X_train["Intercept"] = ones
    ones = []
    for i in range(len(X_test.index)):
        ones.append(1)
    X_test["Intercept"] = ones
    tAwayOpen = []
    tAwayClose = []
    openCoverProb = []
    closeCoverProb = []
    spredd = []
    for i in range(len(predictions)):
        sPred = math.sqrt(mean_squared_error(y_train, train_pred) + np.matmul(np.matmul(X_test.to_numpy()[i],mean_squared_error(y_train, train_pred)*inv(np.matmul(np.transpose(X_train.to_numpy()),X_train.to_numpy()))), np.transpose(X_test.to_numpy()[i])))
        if (predictions[i] < test_OpenSpreads[i]):
            tAwayOpen.append(abs(predictions[i] - test_OpenSpreads[i])/sPred)
            openCoverProb.append(t.cdf(x=abs(predictions[i] - test_OpenSpreads[i])/sPred, df=len(y_train) - len(xCols)))
        else:
            tAwayOpen.append(0-abs(predictions[i] - test_OpenSpreads[i])/sPred)
            openCoverProb.append(t.cdf(x=0-abs(predictions[i] - test_OpenSpreads[i])/sPred, df=len(y_train) - len(xCols)))
        if (predictions[i] < test_CloseSpreads[i]):
            tAwayClose.append(abs(predictions[i] - test_CloseSpreads[i])/sPred)
            closeCoverProb.append(t.cdf(x=abs(predictions[i] - test_CloseSpreads[i])/sPred, df=len(y_train) - len(xCols)))
        else:
            tAwayClose.append(0-abs(predictions[i] - test_CloseSpreads[i])/sPred)
            closeCoverProb.append(t.cdf(x=0-abs(predictions[i] - test_CloseSpreads[i])/sPred, df=len(y_train) - len(xCols)))
        spredd.append(sPred)
    test["T Away Open"] = tAwayOpen
    test["T Away Close"] = tAwayClose
    test["S Pred"] = spredd
    test["Predict Home Open Cover"] = openCoverProb
    test["Predict Home Close Cover"] = closeCoverProb

    homeOpenCover = []
    homeCloseCover = []
    for index, row in test.iterrows():
        if (row["Away Score"] - row["Home Score"] < row["Open Spread"]):
            homeOpenCover.append(1)
        elif (row["Away Score"] - row["Home Score"] > row["Open Spread"]):
            homeOpenCover.append(0)
        else:
            homeOpenCover.append(np.nan)
        if (row["Away Score"] - row["Home Score"] < row["Close Spread"]):
            homeCloseCover.append(1)
        elif (row["Away Score"] - row["Home Score"] > row["Close Spread"]):
            homeCloseCover.append(0)
        else:
            homeCloseCover.append(np.nan)
    test["Home Open Cover"] = homeOpenCover
    test["Home Close Cover"] = homeCloseCover
    #
    for x in [train, test]:
        homeBookRtg = []
        homeWin = []
        for index, row in x.iterrows():
            if (row["Home Open ML"] != 1):
                homeBookRtg.append(-np.log(row["Home Open ML"] - 1))
            else:
                homeBookRtg.append(10)
            if (row["Home Score"] > row["Away Score"]):
                homeWin.append(1)
            else:
                homeWin.append(0)
        x["Home Win"] = homeWin
        x["Home Book Rtg"] = homeBookRtg
    train = train.dropna()
    test = test.dropna()


    pred = []
    y_train = train["Home Win"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LogisticRegression(max_iter = 100000, C = 3)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            pred.append(p[1])
        else:
            pred.append(p[0])
    test["Predict Home Win"] = pred
    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)

def aggregateModelPredictions(league):
    predictions = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    xCols = []
    for col in train.columns:
        if (("gsf" in col or "pfc" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Spread"]
    y_test = test["Actual Spread"]
    test_OpenSpreads = test["Open Spread"]
    test_CloseSpreads = test["Close Spread"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    for p in model.predict(X_test):
        predictions.append(p)
    test["Player Model Predicted Spread"] = predictions

    predictions = []
    xCols = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "P_" not in col and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Spread"]
    y_test = test["Actual Spread"]
    test_OpenSpreads = test["Open Spread"]
    test_CloseSpreads = test["Close Spread"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    for p in model.predict(X_test):
        predictions.append(p)
    test["Team Model Predicted Spread"] = predictions

    predictions = []
    xCols = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    for col in train.columns:
        if (("gsf" in col or "pfc" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Total"]
    y_test = test["Actual Total"]
    test_OpenTotals = test["Open Total"]
    test_CloseTotals = test["Close Total"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    for p in model.predict(X_test):
        predictions.append(p)
    test["Player Model Predicted Total"] = predictions


    predictions = []
    xCols = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Total"]
    y_test = test["Actual Total"]
    test_OpenTotals = test["Open Total"]
    test_CloseTotals = test["Close Total"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LinearRegression()
    model.fit(X = X_train, y = y_train)
    for p in model.predict(X_test):
        predictions.append(p)
    test["Team Model Predicted Total"] = predictions


    homeOpenCover = []
    homeCloseCover = []
    openOver = []
    closeOver = []
    for index, row in test.iterrows():
        if (row["Away Score"] - row["Home Score"] < row["Open Spread"]):
            homeOpenCover.append(1)
        elif (row["Away Score"] - row["Home Score"] > row["Open Spread"]):
            homeOpenCover.append(0)
        else:
            homeOpenCover.append(np.nan)
        if (row["Away Score"] - row["Home Score"] < row["Close Spread"]):
            homeCloseCover.append(1)
        elif (row["Away Score"] - row["Home Score"] > row["Close Spread"]):
            homeCloseCover.append(0)
        else:
            homeCloseCover.append(np.nan)
        if (row["Away Score"] + row["Home Score"] > row["Open Total"]):
            openOver.append(1)
        elif (row["Away Score"] + row["Home Score"] < row["Open Total"]):
            openOver.append(0)
        else:
            openOver.append(np.nan)
        if (row["Away Score"] + row["Home Score"] > row["Close Total"]):
            closeOver.append(1)
        elif (row["Away Score"] + row["Home Score"] < row["Close Total"]):
            closeOver.append(0)
        else:
            closeOver.append(np.nan)
    test["Home Open Cover"] = homeOpenCover
    test["Home Close Cover"] = homeCloseCover
    test["Open Over"] = openOver
    test["Close Over"] = closeOver
    #
    for x in [train, test]:
        homeBookRtg = []
        homeWin = []
        for index, row in x.iterrows():
            if (row["Home Open ML"] != 1):
                homeBookRtg.append(-np.log(row["Home Open ML"] - 1))
            else:
                homeBookRtg.append(10)
            if (row["Home Score"] > row["Away Score"]):
                homeWin.append(1)
            else:
                homeWin.append(0)
        x["Home Win"] = homeWin
        x["Home Book Rtg"] = homeBookRtg
    train = train.dropna()
    test = test.dropna()

    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)

import pandas as pd
import numpy as np
import datetime

def amToDec(odds):
    if (odds > 0):
        return (odds/100 + 1)
    else:
        return (100/abs(odds) + 1)

def kellyStake(p, decOdds, kellyDiv, cap = 0.05):
    if ((p - (1 - p)/(decOdds - 1)) / kellyDiv > cap):
        return (cap)
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def simulateKellyBets(bankroll, kellyDiv, lineType, league):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    totalBets = 0
    for index, row in pred.iterrows():
        if (row["Home " + lineType + " ML"] == 1 or row["Away " + lineType + " ML"] == 1):
            myEdge.append(np.nan)
            actEdge.append(np.nan)
            continue
        if (row["Predict Home Win"] > 1 / row["Home " + lineType + " ML"]):
            if (row["Predict Home Win"] - 1 / row["Home " + lineType + " ML"] < 0.1):
                myEdge.append(np.nan)
                actEdge.append(np.nan)
                continue
            totalBets += 1
            myEdge.append(row["Predict Home Win"] - 1 / row["Home " + lineType + " ML"])
            actEdge.append(row["Home Win"] - 1 / row["Home " + lineType + " ML"])
            if (row["Home Win"] == 1):
                bankroll += bankroll * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"], kellyDiv) * (row["Home " + lineType + " ML"] - 1)
                netSum += baseBR * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"], kellyDiv) * (row["Home " + lineType + " ML"] - 1)
            elif (row["Home Win"] == 0):
                bankroll -= bankroll * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"], kellyDiv)
                netSum -= baseBR * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"], kellyDiv)
        elif (1 - row["Predict Home Win"] > 1 / row["Away " + lineType + " ML"]):
            if (1 - row["Predict Home Win"] - 1 / row["Away " + lineType + " ML"] < 0.1):
                myEdge.append(np.nan)
                actEdge.append(np.nan)
                continue
            totalBets += 1
            myEdge.append(1 - row["Predict Home Win"] - 1 / row["Away " + lineType + " ML"])
            actEdge.append(1 - row["Home Win"] - 1 / row["Away " + lineType + " ML"])
            if (row["Home Win"] == 0):
                bankroll += bankroll * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"], kellyDiv) * (row["Away " + lineType + " ML"] - 1)
                netSum += baseBR * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"], kellyDiv) * (row["Away " + lineType + " ML"] - 1)
            elif (row["Home Win"] == 1):
                bankroll -= bankroll * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"], kellyDiv)
                netSum -= baseBR * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"], kellyDiv)
        else:
            myEdge.append(np.nan)
            actEdge.append(np.nan)
    print (bankroll)
    pred["My Edge"] = myEdge
    pred["Actual Edge"] = actEdge
    pred.to_csv("./csv_data/" + league + "/predictions.csv", index = False)
    print(netSum, totalBets, netSum / totalBets)

def analyzeMyLines(league, betType):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    cats = ["Small Edge","Mid Edge","Large Edge","Larger Edge","Early Over","Mid Over","End Over","Early Under","Mid Under","End Under","Home","Away","On Large Home Fav","Against Large Home Fav","On Small Home Fav","Against Small Home Fav","On Large Away Fav","Against Large Away Fav","On Small Away Fav","Against Small Away Fav"]
    tests = ["Open", "Close", "CLV"]
    dict = {}
    for i in cats:
        for j in tests:
            dict[i + " " + j] = []
    for index, row in pred.iterrows():
        if (row["H_GP"] <= 10 and row["Predicted " + betType] - row["Open " + betType] > 5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Early Over CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Early Over CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Early Over Open"].append(1)
                else:
                    dict["Early Over Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Early Over Open"].append(1)
                else:
                    dict["Early Over Open"].append(0)
        elif (row["H_GP"] <= 20 and row["Predicted " + betType] - row["Open " + betType] > 5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Mid Over CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Mid Over CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Mid Over Open"].append(1)
                else:
                    dict["Mid Over Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Mid Over Open"].append(1)
                else:
                    dict["Mid Over Open"].append(0)
        elif (row["Predicted " + betType] - row["Open " + betType] > 5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["End Over CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["End Over CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["End Over Open"].append(1)
                else:
                    dict["End Over Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["End Over Open"].append(1)
                else:
                    dict["End Over Open"].append(0)
        if (row["H_GP"] <= 10 and row["Predicted " + betType] - row["Open " + betType] < -5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Early Under CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Early Under CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Early Under Open"].append(1)
                else:
                    dict["Early Under Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Early Under Open"].append(1)
                else:
                    dict["Early Under Open"].append(0)
        elif (row["H_GP"] <= 20 and row["Predicted " + betType] - row["Open " + betType] < -5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Mid Under CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Mid Under CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Mid Under Open"].append(1)
                else:
                    dict["Mid Under Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Mid Under Open"].append(1)
                else:
                    dict["Mid Under Open"].append(0)
        elif (row["Predicted " + betType] - row["Open " + betType] < -5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["End Under CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["End Under CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["End Under Open"].append(1)
                else:
                    dict["End Under Open"].append(0)
            else:
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["End Under Open"].append(1)
                else:
                    dict["End Under Open"].append(0)
        #EDGES
        if (abs(row["Predicted " + betType] - row["Open " + betType]) < 3.5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Small Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Small Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Small Edge Open"].append(1)
                else:
                    dict["Small Edge Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Small Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Small Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Small Edge Open"].append(1)
                else:
                    dict["Small Edge Open"].append(0)
        elif (abs(row["Predicted " + betType] - row["Open " + betType]) < 5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Mid Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Mid Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Mid Edge Open"].append(1)
                else:
                    dict["Mid Edge Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Mid Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Mid Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Mid Edge Open"].append(1)
                else:
                    dict["Mid Edge Open"].append(0)
        elif (abs(row["Predicted " + betType] - row["Open " + betType]) < 7.5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Large Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Large Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Large Edge Open"].append(1)
                else:
                    dict["Large Edge Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Large Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Large Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Large Edge Open"].append(1)
                else:
                    dict["Large Edge Open"].append(0)
        elif (abs(row["Predicted " + betType] - row["Open " + betType]) < 12.5):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Larger Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Larger Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Larger Edge Open"].append(1)
                else:
                    dict["Larger Edge Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Larger Edge CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Larger Edge CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Larger Edge Open"].append(1)
                else:
                    dict["Larger Edge Open"].append(0)
        if (abs(row["Predicted " + betType] - row["Close " + betType]) < 3.5):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Small Edge Close"].append(1)
                else:
                    dict["Small Edge Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Small Edge Close"].append(1)
                else:
                    dict["Small Edge Close"].append(0)
        elif (abs(row["Predicted " + betType] - row["Close " + betType]) < 5):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Mid Edge Close"].append(1)
                else:
                    dict["Mid Edge Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Mid Edge Close"].append(1)
                else:
                    dict["Mid Edge Close"].append(0)
        elif (abs(row["Predicted " + betType] - row["Close " + betType]) < 7.5):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Large Edge Close"].append(1)
                else:
                    dict["Large Edge Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Large Edge Close"].append(1)
                else:
                    dict["Large Edge Close"].append(0)
        elif (abs(row["Predicted " + betType] - row["Close " + betType]) < 12.5):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Larger Edge Close"].append(1)
                else:
                    dict["Larger Edge Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Larger Edge Close"].append(1)
                else:
                    dict["Larger Edge Close"].append(0)
        #HOME, AWAY
        if (row["Predicted " + betType] < row["Open " + betType] and abs(row["Predicted " + betType] - row["Open " + betType]) > 5):
            if (row["Close " + betType] < row["Open " + betType]):
                dict["Home CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
            else:
                dict["Home CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
            if (row["Actual " + betType] < row["Open " + betType]):
                dict["Home Open"].append(1)
            else:
                dict["Home Open"].append(0)
        elif (abs(row["Predicted " + betType] - row["Open " + betType]) > 5):
            if (row["Close " + betType] > row["Open " + betType]):
                dict["Away CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
            else:
                dict["Away CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
            if (row["Actual " + betType] > row["Open " + betType]):
                dict["Away Open"].append(1)
            else:
                dict["Away Open"].append(0)
        if (row["Predicted " + betType] < row["Close " + betType]):
            if (row["Actual " + betType] < row["Close " + betType]):
                dict["Home Close"].append(1)
            else:
                dict["Home Close"].append(0)
        else:
            if (row["Actual " + betType] > row["Close " + betType]):
                dict["Away Close"].append(1)
            else:
                dict["Away Close"].append(0)
        #SIZE OF FAVORITE
        if (row["Open " + betType] <= -10):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["On Large Home Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["On Large Home Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["On Large Home Fav Open"].append(1)
                else:
                    dict["On Large Home Fav Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Against Large Home Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Against Large Home Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Against Large Home Fav Open"].append(1)
                else:
                    dict["Against Large Home Fav Open"].append(0)
        elif (row["Open " + betType] < 0):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["On Small Home Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["On Small Home Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["On Small Home Fav Open"].append(1)
                else:
                    dict["On Small Home Fav Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["Against Small Home Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Against Small Home Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["Against Small Home Fav Open"].append(1)
                else:
                    dict["Against Small Home Fav Open"].append(0)
        elif (row["Open " + betType] < 10):
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Against Small Away Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Against Small Away Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Against Small Away Fav Open"].append(1)
                else:
                    dict["Against Small Away Fav Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["On Small Away Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["On Small Away Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["On Small Away Fav Open"].append(1)
                else:
                    dict["On Small Away Fav Open"].append(0)
        else:
            if (row["Predicted " + betType] < row["Open " + betType]):
                if (row["Close " + betType] < row["Open " + betType]):
                    dict["Against Large Away Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["Against Large Away Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] < row["Open " + betType]):
                    dict["Against Large Away Fav Open"].append(1)
                else:
                    dict["Against Large Away Fav Open"].append(0)
            else:
                if (row["Close " + betType] > row["Open " + betType]):
                    dict["On Large Away Fav CLV"].append(abs(row["Close " + betType] - row["Open " + betType]))
                else:
                    dict["On Large Away Fav CLV"].append(0 - abs(row["Close " + betType] - row["Open " + betType]))
                if (row["Actual " + betType] > row["Open " + betType]):
                    dict["On Large Away Fav Open"].append(1)
                else:
                    dict["On Large Away Fav Open"].append(0)

        if (row["Close " + betType] <= -10):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["On Large Home Fav Close"].append(1)
                else:
                    dict["On Large Home Fav Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Against Large Home Fav Close"].append(1)
                else:
                    dict["Against Large Home Fav Close"].append(0)
        elif (row["Close " + betType] < 0):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["On Small Home Fav Close"].append(1)
                else:
                    dict["On Small Home Fav Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["Against Small Home Fav Close"].append(1)
                else:
                    dict["Against Small Home Fav Close"].append(0)
        elif (row["Close " + betType] < 10):
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Against Small Away Fav Close"].append(1)
                else:
                    dict["Against Small Away Fav Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["On Small Away Fav Close"].append(1)
                else:
                    dict["On Small Away Fav Close"].append(0)
        else:
            if (row["Predicted " + betType] < row["Close " + betType]):
                if (row["Actual " + betType] < row["Close " + betType]):
                    dict["Against Large Away Fav Close"].append(1)
                else:
                    dict["Against Large Away Fav Close"].append(0)
            else:
                if (row["Actual " + betType] > row["Close " + betType]):
                    dict["On Large Away Fav Close"].append(1)
                else:
                    dict["On Large Away Fav Close"].append(0)
    print ("<2 points vs Open:", np.average(dict["Small Edge Open"]), "N:", len(dict["Small Edge Open"]))
    print ("2-5 points vs Open:", np.average(dict["Mid Edge Open"]), "N:", len(dict["Mid Edge Open"]))
    print ("5-7.5 points vs Open:", np.average(dict["Large Edge Open"]), "N:", len(dict["Large Edge Open"]))
    print ("7.5-12.5 points vs Open:", np.average(dict["Larger Edge Open"]), "N:", len(dict["Larger Edge Open"]))
    print ("<2 points vs Close:", np.average(dict["Small Edge Close"]), "N:", len(dict["Small Edge Close"]))
    print ("2-5 points vs Close:", np.average(dict["Mid Edge Close"]), "N:", len(dict["Mid Edge Close"]))
    print ("5-7.5 points vs Close:", np.average(dict["Large Edge Close"]), "N:", len(dict["Large Edge Close"]))
    print ("7.5-12.5 points vs Close:", np.average(dict["Larger Edge Close"]), "N:", len(dict["Larger Edge Close"]))
    print ("<2 points CLV:", np.average(dict["Small Edge CLV"]), "N:", len(dict["Small Edge CLV"]))
    print ("2-5 points CLV:", np.average(dict["Mid Edge CLV"]), "N:", len(dict["Mid Edge CLV"]))
    print ("5-7.5 points CLV:", np.average(dict["Large Edge CLV"]), "N:", len(dict["Large Edge CLV"]))
    print ("7.5-12.5 points CLV:", np.average(dict["Larger Edge CLV"]), "N:", len(dict["Larger Edge CLV"]))
    print ("Early Season Over:", np.average(dict["Early Over Open"]), len(dict["Early Over Open"]))
    print ("Mid Season Over:", np.average(dict["Mid Over Open"]), len(dict["Mid Over Open"]))
    print ("End Season Over:", np.average(dict["End Over Open"]), len(dict["End Over Open"]))
    print ("Early Season Under:", np.average(dict["Early Under Open"]), len(dict["Early Under Open"]))
    print ("Mid Season Under:", np.average(dict["Mid Under Open"]), len(dict["Mid Under Open"]))
    print ("End Season Under:", np.average(dict["End Under Open"]), len(dict["End Under Open"]))
    print ("Home vs Open:", np.average(dict["Home Open"]), len(dict["Home Open"]))
    print ("Home vs Close:", np.average(dict["Home Close"]), len(dict["Home Close"]))
    print ("Home CLV:", np.average(dict["Home CLV"]), len(dict["Home CLV"]))
    print ("Away vs Open:", np.average(dict["Away Open"]), len(dict["Away Open"]))
    print ("Away vs Close:", np.average(dict["Away Close"]), len(dict["Away Close"]))
    print ("Away CLV:", np.average(dict["Away CLV"]), len(dict["Away CLV"]))
    # print ("On Large Home Fav Open:", np.average(dict["On Large Home Fav Open"]), len(dict["On Large Home Fav Open"]))
    # print ("On Large Home Fav Close:", np.average(dict["On Large Home Fav Close"]), len(dict["On Large Home Fav Close"]))
    # print ("On Large Home Fav CLV:", np.average(dict["On Large Home Fav CLV"]), len(dict["On Large Home Fav CLV"]))
    # print ("On Small Home Fav Open:", np.average(dict["On Small Home Fav Open"]), len(dict["On Small Home Fav Open"]))
    # print ("On Small Home Fav Close:", np.average(dict["On Small Home Fav Close"]), len(dict["On Small Home Fav Close"]))
    # print ("On Small Home Fav CLV:", np.average(dict["On Small Home Fav CLV"]), len(dict["On Small Home Fav CLV"]))
    # print ("On Small Away Fav Open:", np.average(dict["On Small Away Fav Open"]), len(dict["On Small Away Fav Open"]))
    # print ("On Small Away Fav Close:", np.average(dict["On Small Away Fav Close"]), len(dict["On Small Away Fav Close"]))
    # print ("On Small Away Fav CLV:", np.average(dict["On Small Away Fav CLV"]), len(dict["On Small Away Fav CLV"]))
    # print ("On Large Away Fav Open:", np.average(dict["On Large Away Fav Open"]), len(dict["On Large Away Fav Open"]))
    # print ("On Large Away Fav Close:", np.average(dict["On Large Away Fav Close"]), len(dict["On Large Away Fav Close"]))
    # print ("On Large Away Fav CLV:", np.average(dict["On Large Away Fav CLV"]), len(dict["On Large Away Fav CLV"]))
    # print ("Against Large Home Fav Open:", np.average(dict["Against Large Home Fav Open"]), len(dict["Against Large Home Fav Open"]))
    # print ("Against Large Home Fav Close:", np.average(dict["Against Large Home Fav Close"]), len(dict["Against Large Home Fav Close"]))
    # print ("Against Large Home Fav CLV:", np.average(dict["Against Large Home Fav CLV"]), len(dict["Against Large Home Fav CLV"]))
    # print ("Against Small Home Fav Open:", np.average(dict["Against Small Home Fav Open"]), len(dict["Against Small Home Fav Open"]))
    # print ("Against Small Home Fav Close:", np.average(dict["Against Small Home Fav Close"]), len(dict["Against Small Home Fav Close"]))
    # print ("Against Small Home Fav CLV:", np.average(dict["Against Small Home Fav CLV"]), len(dict["Against Small Home Fav CLV"]))
    # print ("Against Small Away Fav Open:", np.average(dict["Against Small Away Fav Open"]), len(dict["Against Small Away Fav Open"]))
    # print ("Against Small Away Fav Close:", np.average(dict["Against Small Away Fav Close"]), len(dict["Against Small Away Fav Close"]))
    # print ("Against Small Away Fav CLV:", np.average(dict["Against Small Away Fav CLV"]), len(dict["Against Small Away Fav CLV"]))
    # print ("Against Large Away Fav Open:", np.average(dict["Against Large Away Fav Open"]), len(dict["Against Large Away Fav Open"]))
    # print ("Against Large Away Fav Close:", np.average(dict["Against Large Away Fav Close"]), len(dict["Against Large Away Fav Close"]))
    # print ("Against Large Away Fav CLV:", np.average(dict["Against Large Away Fav CLV"]), len(dict["Against Large Away Fav CLV"]))

def kellySpreadBets(bankroll, kellyDiv, lineType, league, uf = 0):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    totalBets = 0
    for index, row in pred.iterrows():
        if (abs(row["Predicted Spread"] - row["Open Spread"]) < 3.5 or abs(row["Predicted Spread"] - row["Open Spread"]) > 7.5):
            myEdge.append(np.nan)
            actEdge.append(np.nan)
            continue
        elif (row["Predict Home " + lineType + " Cover"] > 1 / row["Home " + lineType + " Spread Odds"]):
            totalBets += 1
            myEdge.append(row["Predict Home " + lineType + " Cover"] - 1 / row["Home " + lineType + " Spread Odds"])
            actEdge.append(row["Home " + lineType + " Cover"] - 1 / row["Home " + lineType + " Spread Odds"])
            if (row["Away Score"] - row["Home Score"] < row[lineType + " Spread"] - uf):
                bankroll += bankroll * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"], kellyDiv) * (row["Home " + lineType + " Spread Odds"] - 1)
                netSum += baseBR * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"], kellyDiv) * (row["Home " + lineType + " Spread Odds"] - 1)
            elif (row["Away Score"] - row["Home Score"] > row[lineType + " Spread"] - uf):
                bankroll -= bankroll * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"], kellyDiv)
                netSum -= baseBR * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"], kellyDiv)
        elif (1 - row["Predict Home " + lineType + " Cover"] > 1 / row["Away " + lineType + " Spread Odds"]):
            totalBets += 1
            myEdge.append(1 - row["Predict Home " + lineType + " Cover"] - 1 / row["Away " + lineType + " Spread Odds"])
            actEdge.append(1 - row["Home " + lineType + " Cover"] - 1 / row["Away " + lineType + " Spread Odds"])
            if (row["Away Score"] - row["Home Score"] > row[lineType + " Spread"] + uf):
                bankroll += bankroll * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"], kellyDiv) * (row["Away " + lineType + " Spread Odds"] - 1)
                netSum += baseBR * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"], kellyDiv) * (row["Away " + lineType + " Spread Odds"] - 1)
            elif (row["Away Score"] - row["Home Score"] < row[lineType + " Spread"] + uf):
                bankroll -= bankroll * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"], kellyDiv)
                netSum -= baseBR * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"], kellyDiv)
        else:
            myEdge.append(np.nan)
            actEdge.append(np.nan)
    print (bankroll)
    pred["My Edge"] = myEdge
    pred["Actual Edge"] = actEdge
    pred.to_csv("./csv_data/" + league + "/predictions.csv", index = False)
    print(netSum, totalBets, netSum / totalBets)

def betWithLines(bankroll, league):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    netSum = 0
    preBR = bankroll
    totalBets = 0
    for index, row in pred.iterrows():
        if (abs(row["Predicted Spread"] - row["Open Spread"]) < 2):
            pass
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 5):
            continue
            totalBets += 1
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Actual Spread"] < row["Open Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
            else:
                if (row["Actual Spread"] > row["Open Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 7.5):
            totalBets += 1
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Actual Spread"] < row["Open Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
            else:
                if (row["Actual Spread"] > row["Open Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 12.5):
            totalBets += 1
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Actual Spread"] < row["Open Spread"]):
                    bankroll += bankroll*0.03*0.9
                    netSum += preBR*0.03*0.9
                else:
                    bankroll -= bankroll*0.03
                    netSum -= preBR*0.03
            else:
                if (row["Actual Spread"] > row["Open Spread"]):
                    bankroll += bankroll*0.03*0.9
                    netSum += preBR*0.03*0.9
                else:
                    bankroll -= bankroll*0.03
                    netSum -= preBR*0.03
    print ("Opening Lines Ending BR:", bankroll)
    print("Opening Lines Misc Info:", netSum, totalBets, netSum / totalBets)

    netSum = 0
    totalBets = 0
    bankroll = preBR
    for index, row in pred.iterrows():
        if (abs(row["Predicted Spread"] - row["Close Spread"]) < 2):
            pass
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 5):
            continue
            totalBets += 1
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 10):
            totalBets += 1
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    bankroll += bankroll*0.01*0.9
                    netSum += preBR*0.01*0.9
                else:
                    bankroll -= bankroll*0.01
                    netSum -= preBR*0.01
        else:
            totalBets += 1
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    bankroll += bankroll*0.03*0.9
                    netSum += preBR*0.03*0.9
                else:
                    bankroll -= bankroll*0.03
                    netSum -= preBR*0.03
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    bankroll += bankroll*0.03*0.9
                    netSum += preBR*0.03*0.9
                else:
                    bankroll -= bankroll*0.03
                    netSum -= preBR*0.03
    print ("Closing Lines Ending BR:", bankroll)
    print("Closing Lines Misc Info:", netSum, totalBets, netSum / totalBets)

def agreeAnalysis(league, betType):
    predPlayer = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    predTeam = pd.read_csv("./csv_data/" + league + "/backup/predictions.csv", encoding = "ISO-8859-1")
    player = []
    team = []
    agree = []
    indToVisit = []
    for i in range(len(predTeam.index)):
        indToVisit.append(i)
    for index, row in predPlayer.iterrows():
        for i in indToVisit:
            if (row["Home"] == predTeam.at[i, "Home"] and row["Away"] == predTeam.at[i, "Away"] and row["Date"] == predTeam.at[i, "Date"]):
                indToVisit.remove(i)
                if (abs(row["Predicted " + betType] - row["Open " + betType]) > 5 and abs(predTeam.at[i, "Predicted " + betType] - row["Open " + betType]) > 5):
                    if (row["Predicted " + betType] < row["Open " + betType] and predTeam.at[i, "Predicted " + betType] < row["Open " + betType]):
                        if (row["Actual " + betType] < row["Open " + betType]):
                            agree.append(1)
                            player.append(1)
                            team.append(1)
                        elif (row["Actual " + betType] >row["Open " + betType]):
                            agree.append(0)
                            player.append(0)
                            team.append(0)
                    elif (row["Predicted " + betType] > row["Open " + betType] and predTeam.at[i, "Predicted " + betType] > row["Open " + betType]):
                        if (row["Actual " + betType] >row["Open " + betType]):
                            agree.append(1)
                            player.append(1)
                            team.append(1)
                        elif (row["Actual " + betType] < row["Open " + betType]):
                            agree.append(0)
                            player.append(0)
                            team.append(0)
                    elif (row["Predicted " + betType] > row["Open " + betType] and predTeam.at[i, "Predicted " + betType] < row["Open " + betType]):
                        if (row["Actual " + betType] > row["Open " + betType]):
                            player.append(1)
                            team.append(0)
                        elif (row["Actual " + betType] < row["Open " + betType]):
                            player.append(0)
                            team.append(1)
                    elif (row["Predicted " + betType] < row["Open " + betType] and predTeam.at[i, "Predicted " + betType] > row["Open " + betType]):
                        if (row["Actual " + betType] > row["Open " + betType]):
                            player.append(0)
                            team.append(1)
                        elif (row["Actual " + betType] < row["Open " + betType]):
                            player.append(1)
                            team.append(0)
                elif (abs(row["Predicted " + betType] - row["Open " + betType]) > 5):
                    if (row["Predicted " + betType] < row["Open " + betType]):
                        if (row["Actual " + betType] < row["Open " + betType]):
                            player.append(1)
                        elif (row["Actual " + betType] >row["Open " + betType]):
                            player.append(0)
                    else:
                        if (row["Actual " + betType] < row["Open " + betType]):
                            player.append(0)
                        elif (row["Actual " + betType] >row["Open " + betType]):
                            player.append(1)
                elif (abs(predTeam.at[i, "Predicted " + betType] - row["Open " + betType]) > 5):
                    if (predTeam.at[i, "Predicted " + betType] < row["Open " + betType]):
                        if (row["Actual " + betType] < row["Open " + betType]):
                            team.append(1)
                        elif (row["Actual " + betType] >row["Open " + betType]):
                            team.append(0)
                    else:
                        if (row["Actual " + betType] < row["Open " + betType]):
                            team.append(0)
                        elif (row["Actual " + betType] >row["Open " + betType]):
                            team.append(1)
                break
    print ("TEAM MODEL:", np.average(team), len(team))
    print ("PLAYER MODEL:", np.average(player), len(player))
    print ("AGREE MODEL:", np.average(agree), len(agree))

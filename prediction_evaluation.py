import pandas as pd
import numpy as np
import datetime

def amToDec(odds):
    if (odds > 0):
        return (odds/100 + 1)
    else:
        return (100/abs(odds) + 1)

def kellyStake(p, decOdds):
    return (p - (1 - p)/(decOdds - 1))

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
            myEdge.append(np.nan)
            actEdge.append(np.nan)
            continue
            totalBets += 1
            myEdge.append(row["Predict Home Win"] - 1 / row["Home " + lineType + " ML"])
            actEdge.append(row["Home Win"] - 1 / row["Home " + lineType + " ML"])
            if (row["Home Win"] == 1):
                bankroll += bankroll * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"]) * (row["Home " + lineType + " ML"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"]) * (row["Home " + lineType + " ML"] - 1) / kellyDiv
            elif (row["Home Win"] == 0):
                bankroll -= bankroll * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"]) / kellyDiv
                netSum -= baseBR * kellyStake(row["Predict Home Win"], row["Home " + lineType + " ML"]) / kellyDiv
        elif (1 - row["Predict Home Win"] > 1 / row["Away " + lineType + " ML"] and 1 - row["Predict Home Win"] - 1 / row["Away " + lineType + " ML"] < 0.375):
            totalBets += 1
            myEdge.append(1 - row["Predict Home Win"] - 1 / row["Away " + lineType + " ML"])
            actEdge.append(1 - row["Home Win"] - 1 / row["Away " + lineType + " ML"])
            if (row["Home Win"] == 0):
                bankroll += bankroll * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"]) * (row["Away " + lineType + " ML"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"]) * (row["Away " + lineType + " ML"] - 1) / kellyDiv
            elif (row["Home Win"] == 1):
                bankroll -= bankroll * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"]) / kellyDiv
                netSum -= baseBR * kellyStake(1 - row["Predict Home Win"], row["Away " + lineType + " ML"]) / kellyDiv
        else:
            myEdge.append(np.nan)
            actEdge.append(np.nan)
    print (bankroll)
    pred["My Edge"] = myEdge
    pred["Actual Edge"] = actEdge
    pred.to_csv("./csv_data/" + league + "/predictions.csv", index = False)
    print(netSum, totalBets, netSum / totalBets)

def analyzeMyLines(league):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    smallOpen = []
    midOpen = []
    largeOpen = []
    largerOpen = []
    smallClose = []
    midClose = []
    largeClose = []
    largerClose = []
    smallClv = []
    midClv = []
    largeClv = []
    largerClv = []
    for index, row in pred.iterrows():
        if (abs(row["Predicted Spread"] - row["Open Spread"]) < 2):
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Close Spread"] < row["Open Spread"]):
                    smallClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    smallClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] < row["Open Spread"]):
                    smallOpen.append(1)
                else:
                    smallOpen.append(0)
            else:
                if (row["Close Spread"] > row["Open Spread"]):
                    smallClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    smallClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] > row["Open Spread"]):
                    smallOpen.append(1)
                else:
                    smallOpen.append(0)
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 5):
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Close Spread"] < row["Open Spread"]):
                    midClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    midClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] < row["Open Spread"]):
                    midOpen.append(1)
                else:
                    midOpen.append(0)
            else:
                if (row["Close Spread"] > row["Open Spread"]):
                    midClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    midClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] > row["Open Spread"]):
                    midOpen.append(1)
                else:
                    midOpen.append(0)
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 7.5):
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Close Spread"] < row["Open Spread"]):
                    largeClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    largeClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] < row["Open Spread"]):
                    largeOpen.append(1)
                else:
                    largeOpen.append(0)
            else:
                if (row["Close Spread"] > row["Open Spread"]):
                    largeClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    largeClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] > row["Open Spread"]):
                    largeOpen.append(1)
                else:
                    largeOpen.append(0)
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 12.5):
            if (row["Predicted Spread"] < row["Open Spread"]):
                if (row["Close Spread"] < row["Open Spread"]):
                    largerClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    largerClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] < row["Open Spread"]):
                    largerOpen.append(1)
                else:
                    largerOpen.append(0)
            else:
                if (row["Close Spread"] > row["Open Spread"]):
                    largerClv.append(abs(row["Close Spread"] - row["Open Spread"]))
                else:
                    largerClv.append(0 - abs(row["Close Spread"] - row["Open Spread"]))
                if (row["Actual Spread"] > row["Open Spread"]):
                    largerOpen.append(1)
                else:
                    largerOpen.append(0)
        else:
            pass




        if (abs(row["Predicted Spread"] - row["Close Spread"]) < 2):
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    smallClose.append(1)
                else:
                    smallClose.append(0)
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    smallClose.append(1)
                else:
                    smallClose.append(0)
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 5):
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    midClose.append(1)
                else:
                    midClose.append(0)
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    midClose.append(1)
                else:
                    midClose.append(0)
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 7.5):
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    largeClose.append(1)
                else:
                    largeClose.append(0)
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    largeClose.append(1)
                else:
                    largeClose.append(0)
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 12.5):
            if (row["Predicted Spread"] < row["Close Spread"]):
                if (row["Actual Spread"] < row["Close Spread"]):
                    largerClose.append(1)
                else:
                    largerClose.append(0)
            else:
                if (row["Actual Spread"] > row["Close Spread"]):
                    largerClose.append(1)
                else:
                    largerClose.append(0)
    print ("<2 points vs Open:", np.average(smallOpen), "N:", len(smallOpen))
    print ("2-5 points vs Open:", np.average(midOpen), "N:", len(midOpen))
    print ("5-7.5 points vs Open:", np.average(largeOpen), "N:", len(largeOpen))
    print ("7.5-12.5 points vs Open:", np.average(largerOpen), "N:", len(largerOpen))
    print ("<2 points vs Close:", np.average(smallClose), "N:", len(smallClose))
    print ("2-5 points vs Close:", np.average(midClose), "N:", len(midClose))
    print ("5-7.5 points vs Close:", np.average(largeClose), "N:", len(largeClose))
    print ("7.5-12.5 points vs Close:", np.average(largerClose), "N:", len(largerClose))
    print ("<2 points CLV:", np.average(smallClv), "N:", len(smallClv))
    print ("2-5 points CLV:", np.average(midClv), "N:", len(midClv))
    print ("5-7.5 points CLV:", np.average(largeClv), "N:", len(largeClv))
    print ("7.5-12.5 points CLV:", np.average(largerClv), "N:", len(largerClv))

def kellySpreadBets(bankroll, kellyDiv, lineType, league):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    totalBets = 0
    for index, row in pred.iterrows():
        if (row["Predict Home " + lineType + " Cover"] > 1 / row["Home " + lineType + " Spread Odds"]):
            totalBets += 1
            myEdge.append(row["Predict Home " + lineType + " Cover"] - 1 / row["Home " + lineType + " Spread Odds"])
            actEdge.append(row["Home " + lineType + " Cover"] - 1 / row["Home " + lineType + " Spread Odds"])
            if (row["Home " + lineType + " Cover"] == 1):
                bankroll += bankroll * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"]) * (row["Home " + lineType + " Spread Odds"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"]) * (row["Home " + lineType + " Spread Odds"] - 1) / kellyDiv
            elif (row["Home " + lineType + " Cover"] == 0):
                bankroll -= bankroll * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"]) / kellyDiv
                netSum -= baseBR * kellyStake(row["Predict Home " + lineType + " Cover"], row["Home " + lineType + " Spread Odds"]) / kellyDiv
        elif (1 - row["Predict Home " + lineType + " Cover"] > 1 / row["Away " + lineType + " Spread Odds"]):
            totalBets += 1
            myEdge.append(1 - row["Predict Home " + lineType + " Cover"] - 1 / row["Away " + lineType + " Spread Odds"])
            actEdge.append(1 - row["Home " + lineType + " Cover"] - 1 / row["Away " + lineType + " Spread Odds"])
            if (row["Home " + lineType + " Cover"] == 0):
                bankroll += bankroll * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"]) * (row["Away " + lineType + " Spread Odds"] - 1) / kellyDiv
                netSum += baseBR * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"]) * (row["Away " + lineType + " Spread Odds"] - 1) / kellyDiv
            elif (row["Home " + lineType + " Cover"] == 1):
                bankroll -= bankroll * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"]) / kellyDiv
                netSum -= baseBR * kellyStake(1 - row["Predict Home " + lineType + " Cover"], row["Away " + lineType + " Spread Odds"]) / kellyDiv
        else:
            myEdge.append(np.nan)
            actEdge.append(np.nan)
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

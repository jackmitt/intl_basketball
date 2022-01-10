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

def simulateKellyBets(bankroll, kellyDiv = 1, league = "Spain", preCovid = False):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    totalBets = 0
    stop = False
    for index, row in pred.iterrows():
        if (row["Date"].split("/")[2] == "2020" and row["Date"].split("/")[0] == "3" and preCovid):
            stop = True
        if (stop):
            myEdge.append(np.nan)
            actEdge.append(np.nan)
            continue
        if (row["Home Prob"] > 1 / amToDec(row["Home ML"])):
            totalBets += 1
            myEdge.append(row["Home Prob"] - 1 / amToDec(row["Home ML"]))
            actEdge.append(row["Home Win"] - 1 / amToDec(row["Home ML"]))
            if (row["Home Win"] == 1):
                bankroll += bankroll * kellyStake(row["Home Prob"], amToDec(row["Home ML"])) * (amToDec(row["Home ML"]) - 1) / kellyDiv
                netSum += baseBR * kellyStake(row["Home Prob"], amToDec(row["Home ML"])) * (amToDec(row["Home ML"]) - 1) / kellyDiv
            elif (row["Home Win"] == 0):
                bankroll -= bankroll * kellyStake(row["Home Prob"], amToDec(row["Home ML"])) / kellyDiv
                netSum -= baseBR * kellyStake(row["Home Prob"], amToDec(row["Home ML"])) / kellyDiv
        elif (1 - row["Home Prob"] > 1 / amToDec(row["Away ML"])):
            totalBets += 1
            myEdge.append(1 - row["Home Prob"] - 1 / amToDec(row["Away ML"]))
            actEdge.append(1 - row["Home Win"] - 1 / amToDec(row["Away ML"]))
            if (row["Home Win"] == 0):
                bankroll += bankroll * kellyStake(1 - row["Home Prob"], amToDec(row["Away ML"])) * (amToDec(row["Away ML"]) - 1) / kellyDiv
                netSum += baseBR * kellyStake(1 - row["Home Prob"], amToDec(row["Away ML"])) * (amToDec(row["Away ML"]) - 1) / kellyDiv
            elif (row["Home Win"] == 1):
                bankroll -= bankroll * kellyStake(1 - row["Home Prob"], amToDec(row["Away ML"])) / kellyDiv
                netSum -= baseBR * kellyStake(1 - row["Home Prob"], amToDec(row["Away ML"])) / kellyDiv
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
        elif (abs(row["Predicted Spread"] - row["Open Spread"]) < 10):
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
        else:
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
        elif (abs(row["Predicted Spread"] - row["Close Spread"]) < 10):
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
        else:
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
    print ("5-10 points vs Open:", np.average(largeOpen), "N:", len(largeOpen))
    print (">10 points vs Open:", np.average(largerOpen), "N:", len(largerOpen))
    print ("<2 points vs Close:", np.average(smallClose), "N:", len(smallClose))
    print ("2-5 points vs Close:", np.average(midClose), "N:", len(midClose))
    print ("5-10 points vs Close:", np.average(largeClose), "N:", len(largeClose))
    print (">10 points vs Close:", np.average(largerClose), "N:", len(largerClose))
    print ("<2 points CLV:", np.average(smallClv), "N:", len(smallClv))
    print ("2-5 points CLV:", np.average(midClv), "N:", len(midClv))
    print ("5-10 points CLV:", np.average(largeClv), "N:", len(largeClv))
    print (">10 points CLV:", np.average(largerClv), "N:", len(largerClv))

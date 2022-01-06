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

def simulateKellyBets(bankroll, kellyDiv = 1, league = "Spain"):
    pred = pd.read_csv("./csv_data/" + league + "/predictions.csv", encoding = "ISO-8859-1")
    baseBR = bankroll
    netSum = 0
    myEdge = []
    actEdge = []
    totalBets = 0
    for index, row in pred.iterrows():
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

import pandas as pd
import numpy as np
from helpers import Database
import datetime
from helpers import standardizeTeamName
from helpers import monthToInt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

#for oddsportal - obsolete
def combine_lines_and_stats(league):
    stats = pd.read_csv("./csv_data/" + league + "/gameStats.csv", encoding = "ISO-8859-1")
    odds = pd.read_csv("./csv_data/" + league + "/bettingLines.csv", encoding = "ISO-8859-1")
    A = Database(["Season","Date","Home","Away","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","Home Score","Away Score"])
    for i, r in stats.iterrows():
        found = False
        print (i)
        for index, row in odds.iterrows():
            if (standardizeTeamName(row["Home"]) == r["Home"] and standardizeTeamName(row["Away"]) == r["Away"] and abs(datetime.date(int(row["Date"].split()[3].split(",")[0]), monthToInt(row["Date"].split()[2]), int(row["Date"].split()[1])) - datetime.date(int(r["Date"].split("-")[0]), int(r["Date"].split("-")[1]), int(r["Date"].split("-")[2]))).days <= 1):
                A.addCellToRow(row["Season"])
                A.addCellToRow(r["Date"])
                A.addCellToRow(r["Home"])
                A.addCellToRow(r["Away"])
                A.addCellToRow(r["h_ORtg"])
                A.addCellToRow(r["a_ORtg"])
                A.addCellToRow(r["h_eFG%"])
                A.addCellToRow(r["a_eFG%"])
                A.addCellToRow(r["h_TO%"])
                A.addCellToRow(r["a_TO%"])
                A.addCellToRow(r["h_OR%"])
                A.addCellToRow(r["a_OR%"])
                A.addCellToRow(r["h_FTR"])
                A.addCellToRow(r["a_FTR"])
                A.addCellToRow(r["h_FIC"])
                A.addCellToRow(r["a_FIC"])
                A.addCellToRow(row["Home ML"])
                A.addCellToRow(row["Away ML"])
                A.addCellToRow(standardizeTeamName(row["Favorite"]))
                A.addCellToRow(row["Spread"])
                A.addCellToRow(row["Home Spread Odds"])
                A.addCellToRow(row["Away Spread Odds"])
                A.addCellToRow(row["Home Score"])
                A.addCellToRow(row["Away Score"])
                A.appendRow()
                found = True
                break
        if (not found):
            A.addCellToRow(np.nan)
            A.addCellToRow(r["Date"])
            A.addCellToRow(r["Home"])
            A.addCellToRow(r["Away"])
            A.addCellToRow(r["h_ORtg"])
            A.addCellToRow(r["a_ORtg"])
            A.addCellToRow(r["h_eFG%"])
            A.addCellToRow(r["a_eFG%"])
            A.addCellToRow(r["h_TO%"])
            A.addCellToRow(r["a_TO%"])
            A.addCellToRow(r["h_OR%"])
            A.addCellToRow(r["a_OR%"])
            A.addCellToRow(r["h_FTR"])
            A.addCellToRow(r["a_FTR"])
            A.addCellToRow(r["h_FIC"])
            A.addCellToRow(r["a_FIC"])
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.appendRow()
    A.dictToCsv("./csv_data/" + league + "/combined.csv")

#for spreads
def combine_spreads_and_stats(league):
    stats = pd.read_csv("./csv_data/" + league + "/gameStats.csv", encoding = "ISO-8859-1")
    odds = pd.read_csv("./csv_data/" + league + "/spreads.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","Open Spread","Home Open Spread Odds","Away Open Spread Odds","Close Spread","Home Close Spread Odds","Away Close Spread Odds","Home Score","Away Score"])
    for i, r in stats.iterrows():
        found = False
        print (i)
        for index, row in odds.iterrows():
            try:
                if ("/" in row["Date"]):
                    oddsDate = datetime.date(int(row["Date"].split("/")[2]), int(row["Date"].split("/")[1]), int(row["Date"].split("/")[0]))
                else:
                    oddsDate = datetime.date(int(row["Date"].split("-")[2]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[0]))
            except:
                continue
            if (r["Home"] in standardizeTeamName(row["Home"], league) and r["Away"] in standardizeTeamName(row["Away"], league) and abs(oddsDate - datetime.date(int(r["Date"].split("-")[0]), int(r["Date"].split("-")[1]), int(r["Date"].split("-")[2]))).days <= 1):
                A.addCellToRow(r["Date"])
                A.addCellToRow(standardizeTeamName(row["Home"], league))
                A.addCellToRow(standardizeTeamName(row["Away"], league))
                A.addCellToRow(r["h_ORtg"])
                A.addCellToRow(r["a_ORtg"])
                A.addCellToRow(r["h_eFG%"])
                A.addCellToRow(r["a_eFG%"])
                A.addCellToRow(r["h_TO%"])
                A.addCellToRow(r["a_TO%"])
                A.addCellToRow(r["h_OR%"])
                A.addCellToRow(r["a_OR%"])
                A.addCellToRow(r["h_FTR"])
                A.addCellToRow(r["a_FTR"])
                A.addCellToRow(r["h_FIC"])
                A.addCellToRow(r["a_FIC"])
                A.addCellToRow(row["Open Spread"])
                A.addCellToRow(row["Home Open Spread Odds"])
                A.addCellToRow(row["Away Open Spread Odds"])
                A.addCellToRow(row["Close Spread"])
                A.addCellToRow(row["Home Close Spread Odds"])
                A.addCellToRow(row["Away Close Spread Odds"])
                A.addCellToRow(row["Home Score"])
                A.addCellToRow(row["Away Score"])
                A.appendRow()
                found = True
                break
        if (not found):
            A.addCellToRow(r["Date"])
            A.addCellToRow(r["Home"])
            A.addCellToRow(r["Away"])
            A.addCellToRow(r["h_ORtg"])
            A.addCellToRow(r["a_ORtg"])
            A.addCellToRow(r["h_eFG%"])
            A.addCellToRow(r["a_eFG%"])
            A.addCellToRow(r["h_TO%"])
            A.addCellToRow(r["a_TO%"])
            A.addCellToRow(r["h_OR%"])
            A.addCellToRow(r["a_OR%"])
            A.addCellToRow(r["h_FTR"])
            A.addCellToRow(r["a_FTR"])
            A.addCellToRow(r["h_FIC"])
            A.addCellToRow(r["a_FIC"])
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.appendRow()
    A.dictToCsv("./csv_data/" + league + "/combined.csv")

def preMatchAverages(league):
    stats = pd.read_csv("./csv_data/" + league + "/combined.csv", encoding = "ISO-8859-1")
    A = Database(["Season","Date","Home","Away","H_GP","A_GP","H_ORtg","A_ORtg","H_DRtg","A_DRtg","H_eFG%","A_eFG%","H_DeFG%","A_DeFG%","H_TO%","A_TO%","H_DTO%","A_DTO%","H_OR%","A_OR%","H_DOR%","A_DOR%","H_FTR","A_FTR","H_DFTR","A_DFTR","H_FIC","A_FIC","H_DFIC","A_DFIC","F_H_ORtg","F_A_ORtg","F_H_DRtg","F_A_DRtg","F_H_eFG%","F_A_eFG%","F_H_DeFG%","F_A_DeFG%","F_H_TO%","F_A_TO%","F_H_DTO%","F_A_DTO%","F_H_OR%","F_A_OR%","F_H_DOR%","F_A_DOR%","F_H_FTR","F_A_FTR","F_H_DFTR","F_A_DFTR","F_H_FIC","F_A_FIC","F_H_DFIC","F_A_DFIC","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","Home Score","Away Score"])
    for index, row in stats.iterrows():
        print (index)
        if (np.isnan(row["Spread"])):
            continue
        if (index == 0 or row["Season"] != stats.at[index-1,"Season"]):
            seasonDict = {}
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"adj_ORtg":[],"adj_DRtg":[],"adj_eFG%":[],"adj_DeFG%":[],"adj_TO%":[],"adj_DTO%":[],"adj_OR%":[],"adj_DOR%":[],"adj_FTR":[],"adj_DFTR":[],"adj_FIC":[],"adj_DFIC":[],"GP":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"adj_ORtg":[],"adj_DRtg":[],"adj_eFG%":[],"adj_DeFG%":[],"adj_TO%":[],"adj_DTO%":[],"adj_OR%":[],"adj_DOR%":[],"adj_FTR":[],"adj_DFTR":[],"adj_FIC":[],"adj_DFIC":[],"GP":0}
        if (seasonDict[row["Away"]]["GP"] >= 5 and seasonDict[row["Home"]]["GP"] >= 5):
            A.addCellToRow(row["Season"])
            A.addCellToRow(row["Date"])
            A.addCellToRow(row["Home"])
            A.addCellToRow(row["Away"])
            A.addCellToRow(seasonDict[row["Home"]]["GP"])
            A.addCellToRow(seasonDict[row["Away"]]["GP"])
            A.addCellToRow(np.average(seasonDict[row["Home"]]["ORtg"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["ORtg"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DRtg"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["eFG%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["eFG%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DeFG%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DeFG%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DTO%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DTO%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["OR%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["OR%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DOR%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DOR%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["FTR"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["FTR"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DFTR"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DFTR"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["FIC"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["FIC"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DFIC"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DFIC"]))

            A.addCellToRow(np.average(seasonDict[row["Home"]]["ORtg"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["ORtg"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DRtg"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DRtg"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["eFG%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["eFG%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DeFG%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DeFG%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["TO%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["TO%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DTO%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DTO%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["OR%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["OR%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DOR%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DOR%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["FTR"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["FTR"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DFTR"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DFTR"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["FIC"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["FIC"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["DFIC"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["DFIC"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))

            #seems like these adjusted stats suck - but why
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_ORtg"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_ORtg"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DRtg"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DRtg"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_eFG%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_eFG%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DeFG%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DeFG%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_TO%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_TO%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DTO%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DTO%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_OR%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_OR%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DOR%"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DOR%"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_FTR"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_FTR"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DFTR"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DFTR"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_FIC"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_FIC"]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DFIC"]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DFIC"]))
            #
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_ORtg"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_ORtg"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DRtg"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DRtg"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_eFG%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_eFG%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DeFG%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DeFG%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_TO%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_TO%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DTO%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DTO%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_OR%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_OR%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DOR%"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DOR%"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_FTR"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_FTR"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DFTR"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DFTR"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_FIC"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_FIC"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Home"]]["adj_DFIC"][seasonDict[row["Home"]]["GP"] - 5:seasonDict[row["Home"]]["GP"]]))
            # A.addCellToRow(np.average(seasonDict[row["Away"]]["adj_DFIC"][seasonDict[row["Away"]]["GP"] - 5:seasonDict[row["Away"]]["GP"]]))

            A.addCellToRow(row["Home ML"])
            A.addCellToRow(row["Away ML"])
            A.addCellToRow(row["Favorite"])
            A.addCellToRow(row["Spread"])
            A.addCellToRow(row["Home Spread Odds"])
            A.addCellToRow(row["Away Spread Odds"])
            A.addCellToRow(row["Home Score"])
            A.addCellToRow(row["Away Score"])
            A.appendRow()
        seasonDict[row["Home"]]["ORtg"].append(row["h_ORtg"])
        seasonDict[row["Away"]]["ORtg"].append(row["a_ORtg"])
        seasonDict[row["Home"]]["DRtg"].append(row["a_ORtg"])
        seasonDict[row["Away"]]["DRtg"].append(row["h_ORtg"])
        seasonDict[row["Home"]]["eFG%"].append(row["h_eFG%"])
        seasonDict[row["Away"]]["eFG%"].append(row["a_eFG%"])
        seasonDict[row["Home"]]["DeFG%"].append(row["a_eFG%"])
        seasonDict[row["Away"]]["DeFG%"].append(row["h_eFG%"])
        seasonDict[row["Home"]]["TO%"].append(row["h_TO%"])
        seasonDict[row["Away"]]["TO%"].append(row["a_TO%"])
        seasonDict[row["Home"]]["DTO%"].append(row["a_TO%"])
        seasonDict[row["Away"]]["DTO%"].append(row["h_TO%"])
        seasonDict[row["Home"]]["OR%"].append(row["h_OR%"])
        seasonDict[row["Away"]]["OR%"].append(row["a_OR%"])
        seasonDict[row["Home"]]["DOR%"].append(row["a_OR%"])
        seasonDict[row["Away"]]["DOR%"].append(row["h_OR%"])
        seasonDict[row["Home"]]["FTR"].append(row["h_FTR"])
        seasonDict[row["Away"]]["FTR"].append(row["a_FTR"])
        seasonDict[row["Home"]]["DFTR"].append(row["a_FTR"])
        seasonDict[row["Away"]]["DFTR"].append(row["h_FTR"])
        seasonDict[row["Home"]]["FIC"].append(row["h_FIC"])
        seasonDict[row["Away"]]["FIC"].append(row["a_FIC"])
        seasonDict[row["Home"]]["DFIC"].append(row["a_FIC"])
        seasonDict[row["Away"]]["DFIC"].append(row["h_FIC"])

        #maybe should use priors for this in the future
        # default_h_rtg = stats["h_ORtg"].mean()
        # default_a_rtg = stats["a_ORtg"].mean()
        # default_h_eFG = stats["h_eFG%"].mean()
        # default_a_eFG = stats["a_eFG%"].mean()
        # default_h_to = stats["h_TO%"].mean()
        # default_a_to = stats["a_TO%"].mean()
        # default_h_or = stats["h_OR%"].mean()
        # default_a_or = stats["a_OR%"].mean()
        # default_h_ftr = stats["h_FTR"].mean()
        # default_a_ftr = stats["a_FTR"].mean()
        # default_h_fic = stats["h_FIC"].mean()
        # default_a_fic = stats["a_FIC"].mean()
        # if (seasonDict[row["Home"]]["GP"] > 2):
        #     seasonDict[row["Home"]]["adj_ORtg"].append(row["h_ORtg"] - np.average(seasonDict[row["Away"]]["DRtg"]))
        #     seasonDict[row["Away"]]["adj_ORtg"].append(row["a_ORtg"] - np.average(seasonDict[row["Home"]]["DRtg"]))
        #     seasonDict[row["Home"]]["adj_DRtg"].append(row["a_ORtg"] - np.average(seasonDict[row["Away"]]["ORtg"]))
        #     seasonDict[row["Away"]]["adj_DRtg"].append(row["h_ORtg"] - np.average(seasonDict[row["Home"]]["ORtg"]))
        #     seasonDict[row["Home"]]["adj_eFG%"].append(row["h_eFG%"] - np.average(seasonDict[row["Away"]]["DeFG%"]))
        #     seasonDict[row["Away"]]["adj_eFG%"].append(row["a_eFG%"] - np.average(seasonDict[row["Home"]]["DeFG%"]))
        #     seasonDict[row["Home"]]["adj_DeFG%"].append(row["a_eFG%"] - np.average(seasonDict[row["Away"]]["eFG%"]))
        #     seasonDict[row["Away"]]["adj_DeFG%"].append(row["h_eFG%"] - np.average(seasonDict[row["Home"]]["eFG%"]))
        #     seasonDict[row["Home"]]["adj_TO%"].append(row["h_TO%"] - np.average(seasonDict[row["Away"]]["DTO%"]))
        #     seasonDict[row["Away"]]["adj_TO%"].append(row["a_TO%"] - np.average(seasonDict[row["Home"]]["DTO%"]))
        #     seasonDict[row["Home"]]["adj_DTO%"].append(row["a_TO%"] - np.average(seasonDict[row["Away"]]["TO%"]))
        #     seasonDict[row["Away"]]["adj_DTO%"].append(row["h_TO%"] - np.average(seasonDict[row["Home"]]["TO%"]))
        #     seasonDict[row["Home"]]["adj_OR%"].append(row["h_OR%"] - np.average(seasonDict[row["Away"]]["DOR%"]))
        #     seasonDict[row["Away"]]["adj_OR%"].append(row["a_OR%"] - np.average(seasonDict[row["Home"]]["DOR%"]))
        #     seasonDict[row["Home"]]["adj_DOR%"].append(row["a_OR%"] - np.average(seasonDict[row["Away"]]["OR%"]))
        #     seasonDict[row["Away"]]["adj_DOR%"].append(row["h_OR%"] - np.average(seasonDict[row["Home"]]["OR%"]))
        #     seasonDict[row["Home"]]["adj_FTR"].append(row["h_FTR"] - np.average(seasonDict[row["Away"]]["DFTR"]))
        #     seasonDict[row["Away"]]["adj_FTR"].append(row["a_FTR"] - np.average(seasonDict[row["Home"]]["DFTR"]))
        #     seasonDict[row["Home"]]["adj_DFTR"].append(row["a_FTR"] - np.average(seasonDict[row["Away"]]["FTR"]))
        #     seasonDict[row["Away"]]["adj_DFTR"].append(row["h_FTR"] - np.average(seasonDict[row["Home"]]["FTR"]))
        #     seasonDict[row["Home"]]["adj_FIC"].append(row["h_FIC"] - np.average(seasonDict[row["Away"]]["DFIC"]))
        #     seasonDict[row["Away"]]["adj_FIC"].append(row["a_FIC"] - np.average(seasonDict[row["Home"]]["DFIC"]))
        #     seasonDict[row["Home"]]["adj_DFIC"].append(row["a_FIC"] - np.average(seasonDict[row["Away"]]["FIC"]))
        #     seasonDict[row["Away"]]["adj_DFIC"].append(row["h_FIC"] - np.average(seasonDict[row["Home"]]["FIC"]))
        # else:
        #     seasonDict[row["Home"]]["adj_ORtg"].append(row["h_ORtg"] - default_h_rtg)
        #     seasonDict[row["Away"]]["adj_ORtg"].append(row["a_ORtg"] - default_a_rtg)
        #     seasonDict[row["Home"]]["adj_DRtg"].append(row["a_ORtg"] - default_a_rtg)
        #     seasonDict[row["Away"]]["adj_DRtg"].append(row["h_ORtg"] - default_h_rtg)
        #     seasonDict[row["Home"]]["adj_eFG%"].append(row["h_eFG%"] - default_h_eFG)
        #     seasonDict[row["Away"]]["adj_eFG%"].append(row["a_eFG%"] - default_a_eFG)
        #     seasonDict[row["Home"]]["adj_DeFG%"].append(row["a_eFG%"] - default_a_eFG)
        #     seasonDict[row["Away"]]["adj_DeFG%"].append(row["h_eFG%"] - default_h_eFG)
        #     seasonDict[row["Home"]]["adj_TO%"].append(row["h_TO%"] - default_h_to)
        #     seasonDict[row["Away"]]["adj_TO%"].append(row["a_TO%"] - default_a_to)
        #     seasonDict[row["Home"]]["adj_DTO%"].append(row["a_TO%"] - default_a_to)
        #     seasonDict[row["Away"]]["adj_DTO%"].append(row["h_TO%"] - default_h_to)
        #     seasonDict[row["Home"]]["adj_OR%"].append(row["h_OR%"] - default_h_or)
        #     seasonDict[row["Away"]]["adj_OR%"].append(row["a_OR%"] - default_a_or)
        #     seasonDict[row["Home"]]["adj_DOR%"].append(row["a_OR%"] - default_a_or)
        #     seasonDict[row["Away"]]["adj_DOR%"].append(row["h_OR%"] - default_h_or)
        #     seasonDict[row["Home"]]["adj_FTR"].append(row["h_FTR"] - default_h_ftr)
        #     seasonDict[row["Away"]]["adj_FTR"].append(row["a_FTR"] - default_a_ftr)
        #     seasonDict[row["Home"]]["adj_DFTR"].append(row["a_FTR"] - default_a_ftr)
        #     seasonDict[row["Away"]]["adj_DFTR"].append(row["h_FTR"] - default_h_ftr)
        #     seasonDict[row["Home"]]["adj_FIC"].append(row["h_FIC"] - default_h_fic)
        #     seasonDict[row["Away"]]["adj_FIC"].append(row["a_FIC"] - default_a_fic)
        #     seasonDict[row["Home"]]["adj_DFIC"].append(row["a_FIC"] - default_a_fic)
        #     seasonDict[row["Away"]]["adj_DFIC"].append(row["h_FIC"] - default_h_fic)

        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1

    A.dictToCsv("./csv_data/" + league + "/preMatchAverages.csv")

def train_test_split(league):
    data = pd.read_csv("./csv_data/" + league + "/preMatchAverages.csv", encoding = "ISO-8859-1")
    hw = []
    for index, row in data.iterrows():
        if (row["Home Score"] > row["Away Score"]):
            hw.append(1)
        else:
            hw.append(0)
    data["Home Win"] = hw
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        if (row["Season"] == "2017/2018"):
            test = True
        if (test):
            testRows.append(index)
        else:
            trainRows.append(index)
    data.iloc[trainRows].to_csv("./csv_data/" + league + "/train.csv", index = False)
    data.iloc[testRows].to_csv("./csv_data/" + league + "/test.csv", index = False)

def predictions(league):
    predictions = []
    train = pd.read_csv("./csv_data/" + league + "/train.csv", encoding = "ISO-8859-1")
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1")
    xCols = []
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "_GP" not in col):
            xCols.append(col)
    y_train = train["Home Win"]
    scaler = StandardScaler()
    X_train = pd.DataFrame(train, columns = xCols)
    X_train[xCols] = scaler.fit_transform(X_train[xCols])
    X_test = pd.DataFrame(test, columns = xCols)
    X_test[xCols] = scaler.transform(X_test[xCols])
    model = LogisticRegression(max_iter = 100000, C = 99999999999)
    model.fit(X = X_train, y = y_train)
    for p in model.predict_proba(X_test):
        if (model.classes_[1] == 1):
            predictions.append(p[1])
        else:
            predictions.append(p[0])
    test["Home Prob"] = predictions

    test.to_csv("./csv_data/" + league + "/predictions.csv", index = False)

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

def checkTeamNames(league):
    odds = pd.read_csv("./csv_data/" + league + "/spreads.csv", encoding = "ISO-8859-1")
    for index, row in odds.iterrows():
        try:
            if ("ERROR" in standardizeTeamName(row["Home"], league)):
                print (standardizeTeamName(row["Home"], league))
        except:
            continue

#for spreads and totals
def combine_spreads_and_stats(league, imputeScoresFromBackup = True):
    stats = pd.read_csv("./csv_data/" + league + "/gameStatsNew.csv", encoding = "ISO-8859-1")
    if (imputeScoresFromBackup):
        backup = pd.read_csv("./csv_data/" + league + "/backup/combined.csv", encoding = "ISO-8859-1")
        stats["Home Score"] = backup["Home Score"]
        stats["Away Score"] = backup["Away Score"]
        stats["Home"] = backup["Home"]
        stats["Away"] = backup["Away"]
    odds = pd.read_csv("./csv_data/" + league + "/spreads.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","Poss","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","Home Open ML","Away Open ML","Home Close ML","Away Close ML","Open Spread","Home Open Spread Odds","Away Open Spread Odds","Close Spread","Home Close Spread Odds","Away Close Spread Odds","Open Total","Home Open Total Odds","Away Open Total Odds","Close Total","Home Close Total Odds","Away Close Total Odds","Home Score","Away Score"])
    for a in ["h_","a_"]:
        for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                for d in ["name","seconds","FGM-A","3PM-A","FTM-A","FIC","OReb","DReb","Ast","PF","STL","TO","BLK","PTS"]:
                    A.addColumn(a + b + c + d)
    for i, r in stats.iterrows():
        found = False
        print (i)
        if (int(r["Date"].split("-")[0]) < 2017):
            A.addCellToRow(r["Date"])
            A.addCellToRow(r["Home"])
            A.addCellToRow(r["Away"])
            A.addCellToRow(r["Poss"])
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
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(r["Home Score"])
            A.addCellToRow(r["Away Score"])
            for a in ["h_","a_"]:
                for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
                    for c in ["pg_","sg_","sf_","pf_","c_"]:
                        for d in ["name","seconds","FGM-A","3PM-A","FTM-A","FIC","OReb","DReb","Ast","PF","STL","TO","BLK","PTS"]:
                            A.addCellToRow(r[a + b + c + d])
            A.appendRow()
            continue
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
                A.addCellToRow(r["Poss"])
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
                A.addCellToRow(row["Home Open ML"])
                A.addCellToRow(row["Away Open ML"])
                A.addCellToRow(row["Home Close ML"])
                A.addCellToRow(row["Away Close ML"])
                A.addCellToRow(row["Open Spread"])
                A.addCellToRow(row["Home Open Spread Odds"])
                A.addCellToRow(row["Away Open Spread Odds"])
                A.addCellToRow(row["Close Spread"])
                A.addCellToRow(row["Home Close Spread Odds"])
                A.addCellToRow(row["Away Close Spread Odds"])
                A.addCellToRow(row["Open Total"])
                A.addCellToRow(row["Home Open Total Odds"])
                A.addCellToRow(row["Away Open Total Odds"])
                A.addCellToRow(row["Close Total"])
                A.addCellToRow(row["Home Close Total Odds"])
                A.addCellToRow(row["Away Close Total Odds"])
                A.addCellToRow(row["Home Score"])
                A.addCellToRow(row["Away Score"])
                for a in ["h_","a_"]:
                    for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
                        for c in ["pg_","sg_","sf_","pf_","c_"]:
                            for d in ["name","seconds","FGM-A","3PM-A","FTM-A","FIC","OReb","DReb","Ast","PF","STL","TO","BLK","PTS"]:
                                A.addCellToRow(r[a + b + c + d])
                A.appendRow()
                found = True
                break
        if (not found):
            A.addCellToRow(r["Date"])
            A.addCellToRow(r["Home"])
            A.addCellToRow(r["Away"])
            A.addCellToRow(r["Poss"])
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
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(r["Home Score"])
            A.addCellToRow(r["Away Score"])
            for a in ["h_","a_"]:
                for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
                    for c in ["pg_","sg_","sf_","pf_","c_"]:
                        for d in ["name","seconds","FGM-A","3PM-A","FTM-A","FIC","OReb","DReb","Ast","PF","STL","TO","BLK","PTS"]:
                            A.addCellToRow(r[a + b + c + d])
            A.appendRow()
    A.dictToCsv("./csv_data/" + league + "/combined.csv")

#did this to merge totals that were scraped only for 2017 and later - last function assumes the betting data is available going back to 2014
def tempAddTotalsFromBackupCombined(league):
    stats = pd.read_csv("./csv_data/" + league + "/backup/combined.csv", encoding = "ISO-8859-1")
    odds = pd.read_csv("./csv_data/" + league + "/spreads.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","Home Open ML","Away Open ML","Home Close ML","Away Close ML","Open Spread","Home Open Spread Odds","Away Open Spread Odds","Close Spread","Home Close Spread Odds","Away Close Spread Odds","Open Total","Home Open Total Odds","Away Open Total Odds","Close Total","Home Close Total Odds","Away Close Total Odds","Home Score","Away Score"])
    for i, r in stats.iterrows():
        found = False
        print (i)
        if (int(r["Date"].split("-")[0]) < 2017):
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
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(r["Home Score"])
            A.addCellToRow(r["Away Score"])
            A.appendRow()
            continue
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
                A.addCellToRow(row["Home Open ML"])
                A.addCellToRow(row["Away Open ML"])
                A.addCellToRow(row["Home Close ML"])
                A.addCellToRow(row["Away Close ML"])
                A.addCellToRow(row["Open Spread"])
                A.addCellToRow(row["Home Open Spread Odds"])
                A.addCellToRow(row["Away Open Spread Odds"])
                A.addCellToRow(row["Close Spread"])
                A.addCellToRow(row["Home Close Spread Odds"])
                A.addCellToRow(row["Away Close Spread Odds"])
                A.addCellToRow(row["Open Total"])
                A.addCellToRow(row["Home Open Total Odds"])
                A.addCellToRow(row["Away Open Total Odds"])
                A.addCellToRow(row["Close Total"])
                A.addCellToRow(row["Home Close Total Odds"])
                A.addCellToRow(row["Away Close Total Odds"])
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
            A.addCellToRow(r["Home Open ML"])
            A.addCellToRow(r["Away Open ML"])
            A.addCellToRow(r["Home Close ML"])
            A.addCellToRow(r["Away Close ML"])
            A.addCellToRow(r["Open Spread"])
            A.addCellToRow(r["Home Open Spread Odds"])
            A.addCellToRow(r["Away Open Spread Odds"])
            A.addCellToRow(r["Close Spread"])
            A.addCellToRow(r["Home Close Spread Odds"])
            A.addCellToRow(r["Away Close Spread Odds"])
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
            A.addCellToRow(r["Home Score"])
            A.addCellToRow(r["Away Score"])
            A.appendRow()
    A.dictToCsv("./csv_data/" + league + "/combined.csv")

def preMatchAverages(league):
    with open("./csv_data/" + league + "/player_priors.pkl","rb") as inputFile:
        priorDict = pickle.load(inputFile)
        #print (priorDict)
    stats = pd.read_csv("./csv_data/" + league + "/combined.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_GP","A_GP","H_Pace","A_Pace","H_ORtg","A_ORtg","H_DRtg","A_DRtg","H_eFG%","A_eFG%","H_DeFG%","A_DeFG%","H_TO%","A_TO%","H_DTO%","A_DTO%","H_OR%","A_OR%","H_DOR%","A_DOR%","H_FTR","A_FTR","H_DFTR","A_DFTR","H_FIC","A_FIC","H_DFIC","A_DFIC","F_H_ORtg","F_A_ORtg","F_H_DRtg","F_A_DRtg","F_H_eFG%","F_A_eFG%","F_H_DeFG%","F_A_DeFG%","F_H_TO%","F_A_TO%","F_H_DTO%","F_A_DTO%","F_H_OR%","F_A_OR%","F_H_DOR%","F_A_DOR%","F_H_FTR","F_A_FTR","F_H_DFTR","F_A_DFTR","F_H_FIC","F_A_FIC","F_H_DFIC","F_A_DFIC","H_gsf_TS%","H_gsf_TO%","H_gsf_OREB%","H_gsf_FTR","H_pfc_TS%","H_pfc_TO%","H_pfc_OREB%","H_pfc_FTR","H_opp_gsf_TS%","H_opp_gsf_TO%","H_opp_gsf_OREB%","H_opp_gsf_FTR","H_opp_pfc_TS%","H_opp_pfc_TO%","H_opp_pfc_OREB%","H_opp_pfc_FTR","A_gsf_TS%","A_gsf_TO%","A_gsf_OREB%","A_gsf_FTR","A_pfc_TS%","A_pfc_TO%","A_pfc_OREB%","A_pfc_FTR","A_opp_gsf_TS%","A_opp_gsf_TO%","A_opp_gsf_OREB%","A_opp_gsf_FTR","A_opp_pfc_TS%","A_opp_pfc_TO%","A_opp_pfc_OREB%","A_opp_pfc_FTR","Home Open ML","Away Open ML","Home Close ML","Away Close ML","Open Spread","Home Open Spread Odds","Away Open Spread Odds","Close Spread","Home Close Spread Odds","Away Close Spread Odds","Open Total","Home Open Total Odds","Away Open Total Odds","Close Total","Home Close Total Odds","Away Close Total Odds","Home Score","Away Score","Actual Spread","Actual Total"])
    #start at 2013, updates to 2014 on index 0
    curSeasonStart = 2013
    for index, row in stats.iterrows():
        print (index)
        #If new season
        if (index == 0 or abs(datetime.date(int(row["Date"].split("-")[0]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[2])) - datetime.date(int(stats.at[index-1,"Date"].split("-")[0]), int(stats.at[index-1,"Date"].split("-")[1]), int(stats.at[index-1,"Date"].split("-")[2]))).days > 30):
            seasonDict = {}
            curSeasonStart += 1
        #init seasondicts
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"Pace":[],"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"opp_gsf_TS%":[],"opp_gsf_TO%":[],"opp_gsf_OREB%":[],"opp_gsf_FTR":[],"opp_pfc_TS%":[],"opp_pfc_TO%":[],"opp_pfc_OREB%":[],"opp_pfc_FTR":[],"GP":0,"Players":{}}
        #iterates through all the possible slots a player can be in in the combined csv
        for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                if (row["h_" + b + c + "name"] == row["h_" + b + c + "name"]):
                    #if the player is not in the records of the team this season
                    if (row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "") not in seasonDict[row["Home"]]["Players"]):
                        #Min_lastgame: number of minutes played last game
                        seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")] = {"MIN_lastgame":0,"POS":c.split("_")[0]}
                        #initialize count stats as 0
                        for stat in ["PTS","FGA","FTA","TOV","MIN","OREB","opp_DREB"]:
                            seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][stat] = 0
                        #Initialize dict for calculating advanced stats based on prior seasons
                        careerStats = {"PTS":0,"FGA":0,"FTA":0,"TOV":0,"orbTally":0,"MIN":0,"GP":0}
                        for key in priorDict[row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]:
                            #When the key matches the current season, we stop so that we ONLY have priors
                            if (int(key.split("-")[0]) >= curSeasonStart):
                                break
                            for x in ["PTS","FGA","FTA","TOV","MIN"]:
                                careerStats[x] += float(priorDict[row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key][x])
                            #orbtally: weighted sum of OREB% based on minutes played in a game - will divide by minutes later to get weighted average
                            #have to do it this way since the opponent DREBs are impossible to match with when each player was in the game
                            careerStats["orbTally"] += float(priorDict[row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key]["OREB%"]) * float(priorDict[row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key]["MIN"])
                        #Final declaration of priors, never edited again
                        try:
                            seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["Priors"] = {"TS%":careerStats["PTS"] / (2*(careerStats["FGA"] + 0.44*careerStats["FTA"])),"TO%":careerStats["TOV"]/(careerStats["FGA"] + 0.44*careerStats["FTA"] + careerStats["TOV"]),"OREB%":careerStats["orbTally"]/careerStats["MIN"]/100,"FTR":careerStats["FTA"]/careerStats["FGA"],"MIN":careerStats["MIN"]}
                        except ZeroDivisionError:
                            seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["Priors"] = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"Pace":[],"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"opp_gsf_TS%":[],"opp_gsf_TO%":[],"opp_gsf_OREB%":[],"opp_gsf_FTR":[],"opp_pfc_TS%":[],"opp_pfc_TO%":[],"opp_pfc_OREB%":[],"opp_pfc_FTR":[],"GP":0,"Players":{}}
        for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                if (row["a_" + b + c + "name"] == row["a_" + b + c + "name"]):
                    if (row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "") not in seasonDict[row["Away"]]["Players"]):
                        seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")] = {"MIN_lastgame":0,"POS":c.split("_")[0]}
                        for stat in ["PTS","FGA","FTA","TOV","MIN","OREB","opp_DREB"]:
                            seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][stat] = 0
                        careerStats = {"PTS":0,"FGA":0,"FTA":0,"TOV":0,"orbTally":0,"MIN":0,"GP":0}
                        for key in priorDict[row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]:
                            if (int(key.split("-")[0]) >= curSeasonStart):
                                break
                            for x in ["PTS","FGA","FTA","TOV","MIN"]:
                                careerStats[x] += float(priorDict[row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key][x])
                            careerStats["orbTally"] += float(priorDict[row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key]["OREB%"]) * float(priorDict[row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")][key]["MIN"])
                        try:
                            seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["Priors"] = {"TS%":careerStats["PTS"] / (2*(careerStats["FGA"] + 0.44*careerStats["FTA"])),"TO%":careerStats["TOV"]/(careerStats["FGA"] + 0.44*careerStats["FTA"] + careerStats["TOV"]),"OREB%":careerStats["orbTally"]/careerStats["MIN"]/100,"FTR":careerStats["FTA"]/careerStats["FGA"],"MIN":careerStats["MIN"]}
                        except ZeroDivisionError:
                            seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["Priors"] = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
        if (seasonDict[row["Away"]]["GP"] >= 5 and seasonDict[row["Home"]]["GP"] >= 5):
            A.addCellToRow(row["Date"])
            A.addCellToRow(row["Home"])
            A.addCellToRow(row["Away"])
            A.addCellToRow(seasonDict[row["Home"]]["GP"])
            A.addCellToRow(seasonDict[row["Away"]]["GP"])
            A.addCellToRow(np.average(seasonDict[row["Home"]]["Pace"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["Pace"]))
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

            #Average of last 5 games - Form
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


            #Four factors stats for players
            #Player stats are grouped for the model into perimeter players (pg,sg,sf) and interior players (pf,c)
            #bayesianPlayerStatsBeta gets the posterior mean for the four factors based on player priors and current season data
            #the posterior mean is mupltiplied by the minutes played by the player in the PREVIOUS game within the current league to get a weighted sum - the assumption: next lineup will match the previous
            #the weighted sums are divided by the total minutes played by that position group last game
            #ultimately, we are rating the position groups for the upcoming game based on the bayesian evaluation AND each player's relative playing time within the group
            fourf = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
            for key in seasonDict[row["Home"]]["Players"]:
                if (seasonDict[row["Home"]]["Players"][key]["POS"] == "pg" or seasonDict[row["Home"]]["Players"][key]["POS"] == "sg" or seasonDict[row["Home"]]["Players"][key]["POS"] == "sf"):
                    try:
                        fourf["TS%"] += bayesianPlayerStatsBeta("gsf_TS%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["PTS"] / (2*(seasonDict[row["Home"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Home"]]["Players"][key]["FTA"])), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TS%"] += bayesianPlayerStatsBeta("gsf_TS%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["TO%"] += bayesianPlayerStatsBeta("gsf_TO%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["TOV"] / (seasonDict[row["Home"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Home"]]["Players"][key]["FTA"] + seasonDict[row["Home"]]["Players"][key]["TOV"]), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TO%"] += bayesianPlayerStatsBeta("gsf_TO%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("gsf_OREB%", seasonDict[row["Home"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["OREB"] / (seasonDict[row["Home"]]["Players"][key]["OREB"] + seasonDict[row["Home"]]["Players"][key]["opp_DREB"]), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("gsf_OREB%", seasonDict[row["Home"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["FTR"] += bayesianPlayerStatsBeta("gsf_FTR", seasonDict[row["Home"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["FTA"] / seasonDict[row["Home"]]["Players"][key]["FGA"], seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["FTR"] += bayesianPlayerStatsBeta("gsf_FTR", seasonDict[row["Home"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    fourf["MIN"] += seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
            A.addCellToRow(fourf["TS%"] / fourf["MIN"])
            A.addCellToRow(fourf["TO%"] / fourf["MIN"])
            A.addCellToRow(fourf["OREB%"] / fourf["MIN"])
            A.addCellToRow(fourf["FTR"] / fourf["MIN"])

            fourf = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
            for key in seasonDict[row["Home"]]["Players"]:
                if (seasonDict[row["Home"]]["Players"][key]["POS"] == "pf" or seasonDict[row["Home"]]["Players"][key]["POS"] == "c"):
                    try:
                        fourf["TS%"] += bayesianPlayerStatsBeta("pfc_TS%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["PTS"] / (2*(seasonDict[row["Home"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Home"]]["Players"][key]["FTA"])), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TS%"] += bayesianPlayerStatsBeta("pfc_TS%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["TO%"] += bayesianPlayerStatsBeta("pfc_TO%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["TOV"] / (seasonDict[row["Home"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Home"]]["Players"][key]["FTA"] + seasonDict[row["Home"]]["Players"][key]["TOV"]), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TO%"] += bayesianPlayerStatsBeta("pfc_TO%", seasonDict[row["Home"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("pfc_OREB%", seasonDict[row["Home"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["OREB"] / (seasonDict[row["Home"]]["Players"][key]["OREB"] + seasonDict[row["Home"]]["Players"][key]["opp_DREB"]), seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("pfc_OREB%", seasonDict[row["Home"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["FTR"] += bayesianPlayerStatsBeta("pfc_FTR", seasonDict[row["Home"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Home"]]["Players"][key]["FTA"] / seasonDict[row["Home"]]["Players"][key]["FGA"], seasonDict[row["Home"]]["Players"][key]["MIN"]) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["FTR"] += bayesianPlayerStatsBeta("pfc_FTR", seasonDict[row["Home"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Home"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
                    fourf["MIN"] += seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"]
            A.addCellToRow(fourf["TS%"] / fourf["MIN"])
            A.addCellToRow(fourf["TO%"] / fourf["MIN"])
            A.addCellToRow(fourf["OREB%"] / fourf["MIN"])
            A.addCellToRow(fourf["FTR"] / fourf["MIN"])

            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_gsf_TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_gsf_TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_gsf_OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_gsf_FTR"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_pfc_TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_pfc_TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_pfc_OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Home"]]["opp_pfc_FTR"]))

            fourf = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
            for key in seasonDict[row["Away"]]["Players"]:
                if (seasonDict[row["Away"]]["Players"][key]["POS"] == "pg" or seasonDict[row["Away"]]["Players"][key]["POS"] == "sg" or seasonDict[row["Away"]]["Players"][key]["POS"] == "sf"):
                    try:
                        fourf["TS%"] += bayesianPlayerStatsBeta("gsf_TS%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["PTS"] / (2*(seasonDict[row["Away"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Away"]]["Players"][key]["FTA"])), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TS%"] += bayesianPlayerStatsBeta("gsf_TS%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["TO%"] += bayesianPlayerStatsBeta("gsf_TO%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["TOV"] / (seasonDict[row["Away"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Away"]]["Players"][key]["FTA"] + seasonDict[row["Away"]]["Players"][key]["TOV"]), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TO%"] += bayesianPlayerStatsBeta("gsf_TO%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("gsf_OREB%", seasonDict[row["Away"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["OREB"] / (seasonDict[row["Away"]]["Players"][key]["OREB"] + seasonDict[row["Away"]]["Players"][key]["opp_DREB"]), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("gsf_OREB%", seasonDict[row["Away"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["FTR"] += bayesianPlayerStatsBeta("gsf_FTR", seasonDict[row["Away"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["FTA"] / seasonDict[row["Away"]]["Players"][key]["FGA"], seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["FTR"] += bayesianPlayerStatsBeta("gsf_FTR", seasonDict[row["Away"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    fourf["MIN"] += seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
            A.addCellToRow(fourf["TS%"] / fourf["MIN"])
            A.addCellToRow(fourf["TO%"] / fourf["MIN"])
            A.addCellToRow(fourf["OREB%"] / fourf["MIN"])
            A.addCellToRow(fourf["FTR"] / fourf["MIN"])

            fourf = {"TS%":0,"TO%":0,"OREB%":0,"FTR":0,"MIN":0}
            for key in seasonDict[row["Away"]]["Players"]:
                if (seasonDict[row["Away"]]["Players"][key]["POS"] == "pf" or seasonDict[row["Away"]]["Players"][key]["POS"] == "c"):
                    try:
                        fourf["TS%"] += bayesianPlayerStatsBeta("pfc_TS%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["PTS"] / (2*(seasonDict[row["Away"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Away"]]["Players"][key]["FTA"])), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TS%"] += bayesianPlayerStatsBeta("pfc_TS%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TS%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["TO%"] += bayesianPlayerStatsBeta("pfc_TO%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["TOV"] / (seasonDict[row["Away"]]["Players"][key]["FGA"] + 0.44*seasonDict[row["Away"]]["Players"][key]["FTA"] + seasonDict[row["Away"]]["Players"][key]["TOV"]), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["TO%"] += bayesianPlayerStatsBeta("pfc_TO%", seasonDict[row["Away"]]["Players"][key]["Priors"]["TO%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("pfc_OREB%", seasonDict[row["Away"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["OREB"] / (seasonDict[row["Away"]]["Players"][key]["OREB"] + seasonDict[row["Away"]]["Players"][key]["opp_DREB"]), seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["OREB%"] += bayesianPlayerStatsBeta("pfc_OREB%", seasonDict[row["Away"]]["Players"][key]["Priors"]["OREB%"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    try:
                        fourf["FTR"] += bayesianPlayerStatsBeta("pfc_FTR", seasonDict[row["Away"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], seasonDict[row["Away"]]["Players"][key]["FTA"] / seasonDict[row["Away"]]["Players"][key]["FGA"], seasonDict[row["Away"]]["Players"][key]["MIN"]) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    except ZeroDivisionError:
                        fourf["FTR"] += bayesianPlayerStatsBeta("pfc_FTR", seasonDict[row["Away"]]["Players"][key]["Priors"]["FTR"], seasonDict[row["Away"]]["Players"][key]["Priors"]["MIN"], 0, 0) * seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
                    fourf["MIN"] += seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"]
            A.addCellToRow(fourf["TS%"] / fourf["MIN"])
            A.addCellToRow(fourf["TO%"] / fourf["MIN"])
            A.addCellToRow(fourf["OREB%"] / fourf["MIN"])
            A.addCellToRow(fourf["FTR"] / fourf["MIN"])

            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_gsf_TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_gsf_TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_gsf_OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_gsf_FTR"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_pfc_TS%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_pfc_TO%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_pfc_OREB%"]))
            A.addCellToRow(np.average(seasonDict[row["Away"]]["opp_pfc_FTR"]))



            A.addCellToRow(row["Home Open ML"])
            A.addCellToRow(row["Away Open ML"])
            A.addCellToRow(row["Home Close ML"])
            A.addCellToRow(row["Away Close ML"])
            A.addCellToRow(row["Open Spread"])
            A.addCellToRow(row["Home Open Spread Odds"])
            A.addCellToRow(row["Away Open Spread Odds"])
            A.addCellToRow(row["Close Spread"])
            A.addCellToRow(row["Home Close Spread Odds"])
            A.addCellToRow(row["Away Close Spread Odds"])
            A.addCellToRow(row["Open Total"])
            A.addCellToRow(row["Home Open Total Odds"])
            A.addCellToRow(row["Away Open Total Odds"])
            A.addCellToRow(row["Close Total"])
            A.addCellToRow(row["Home Close Total Odds"])
            A.addCellToRow(row["Away Close Total Odds"])
            A.addCellToRow(row["Home Score"])
            A.addCellToRow(row["Away Score"])
            A.addCellToRow(row["Away Score"] - row["Home Score"])
            A.addCellToRow(row["Away Score"] + row["Home Score"])
            A.appendRow()

        seasonDict[row["Home"]]["Pace"].append(row["Poss"])
        seasonDict[row["Away"]]["Pace"].append(row["Poss"])
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

        #We get the count data for the position groups for each team so that we can get the opponents performance for the other team
        homeResults = {"gsf_PTS":0,"gsf_FGA":0,"gsf_FTA":0,"gsf_TOV":0,"gsf_OReb":0,"pfc_PTS":0,"pfc_FGA":0,"pfc_FTA":0,"pfc_TOV":0,"pfc_OReb":0,"DReb":0}
        awayResults = {"gsf_PTS":0,"gsf_FGA":0,"gsf_FTA":0,"gsf_TOV":0,"gsf_OReb":0,"pfc_PTS":0,"pfc_FGA":0,"pfc_FTA":0,"pfc_TOV":0,"pfc_OReb":0,"DReb":0}
        for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
            for c in ["pg_","sg_","sf_"]:
                if (row["a_" + b + c + "name"] == row["a_" + b + c + "name"]):
                    awayResults["gsf_PTS"] += row["a_" + b + c + "PTS"]
                    awayResults["gsf_FGA"] += int(row["a_" + b + c + "FGM-A"].split("-")[1])
                    awayResults["gsf_FTA"] += int(row["a_" + b + c + "FTM-A"].split("-")[1])
                    awayResults["gsf_TOV"] += row["a_" + b + c + "TO"]
                    awayResults["gsf_OReb"] += row["a_" + b + c + "OReb"]
                    awayResults["DReb"] += row["a_" + b + c + "DReb"]
                if (row["h_" + b + c + "name"] == row["h_" + b + c + "name"]):
                    homeResults["gsf_PTS"] += row["h_" + b + c + "PTS"]
                    homeResults["gsf_FGA"] += int(row["h_" + b + c + "FGM-A"].split("-")[1])
                    homeResults["gsf_FTA"] += int(row["h_" + b + c + "FTM-A"].split("-")[1])
                    homeResults["gsf_TOV"] += row["h_" + b + c + "TO"]
                    homeResults["gsf_OReb"] += row["h_" + b + c + "OReb"]
                    homeResults["DReb"] += row["h_" + b + c + "DReb"]
            for c in ["pf_","c_"]:
                if (row["a_" + b + c + "name"] == row["a_" + b + c + "name"]):
                    awayResults["pfc_PTS"] += row["a_" + b + c + "PTS"]
                    awayResults["pfc_FGA"] += int(row["a_" + b + c + "FGM-A"].split("-")[1])
                    awayResults["pfc_FTA"] += int(row["a_" + b + c + "FTM-A"].split("-")[1])
                    awayResults["pfc_TOV"] += row["a_" + b + c + "TO"]
                    awayResults["pfc_OReb"] += row["a_" + b + c + "OReb"]
                    awayResults["DReb"] += row["a_" + b + c + "DReb"]
                if (row["h_" + b + c + "name"] == row["h_" + b + c + "name"]):
                    homeResults["pfc_PTS"] += row["h_" + b + c + "PTS"]
                    homeResults["pfc_FGA"] += int(row["h_" + b + c + "FGM-A"].split("-")[1])
                    homeResults["pfc_FTA"] += int(row["h_" + b + c + "FTM-A"].split("-")[1])
                    homeResults["pfc_TOV"] += row["h_" + b + c + "TO"]
                    homeResults["pfc_OReb"] += row["h_" + b + c + "OReb"]
                    homeResults["DReb"] += row["h_" + b + c + "DReb"]

        if (awayResults["gsf_PTS"] != 0 and awayResults["gsf_FGA"] != 0):
            seasonDict[row["Home"]]["opp_gsf_TS%"].append(awayResults["gsf_PTS"] / (2*(awayResults["gsf_FGA"] + 0.44*awayResults["gsf_FTA"])))
            seasonDict[row["Home"]]["opp_gsf_TO%"].append(awayResults["gsf_TOV"]/(awayResults["gsf_FGA"] + 0.44*awayResults["gsf_FTA"] + awayResults["gsf_TOV"]))
            seasonDict[row["Home"]]["opp_gsf_OREB%"].append(awayResults["gsf_OReb"] / (awayResults["gsf_OReb"] + homeResults["DReb"]))
            seasonDict[row["Home"]]["opp_gsf_FTR"].append(awayResults["gsf_FTA"] / awayResults["gsf_FGA"])
        if (awayResults["pfc_PTS"] != 0 and awayResults["pfc_FGA"] != 0):
            seasonDict[row["Home"]]["opp_pfc_TS%"].append(awayResults["pfc_PTS"] / (2*(awayResults["pfc_FGA"] + 0.44*awayResults["pfc_FTA"])))
            seasonDict[row["Home"]]["opp_pfc_TO%"].append(awayResults["pfc_TOV"]/(awayResults["pfc_FGA"] + 0.44*awayResults["pfc_FTA"] + awayResults["pfc_TOV"]))
            seasonDict[row["Home"]]["opp_pfc_OREB%"].append(awayResults["pfc_OReb"] / (awayResults["pfc_OReb"] + homeResults["DReb"]))
            seasonDict[row["Home"]]["opp_pfc_FTR"].append(awayResults["pfc_FTA"] / awayResults["pfc_FGA"])

        if (homeResults["gsf_PTS"] != 0 and homeResults["gsf_FGA"] != 0):
            seasonDict[row["Away"]]["opp_gsf_TS%"].append(homeResults["gsf_PTS"] / (2*(homeResults["gsf_FGA"] + 0.44*homeResults["gsf_FTA"])))
            seasonDict[row["Away"]]["opp_gsf_TO%"].append(homeResults["gsf_TOV"]/(homeResults["gsf_FGA"] + 0.44*homeResults["gsf_FTA"] + homeResults["gsf_TOV"]))
            seasonDict[row["Away"]]["opp_gsf_OREB%"].append(homeResults["gsf_OReb"] / (homeResults["gsf_OReb"] + awayResults["DReb"]))
            seasonDict[row["Away"]]["opp_gsf_FTR"].append(homeResults["gsf_FTA"] / homeResults["gsf_FGA"])
        if (homeResults["pfc_PTS"] != 0 and homeResults["pfc_FGA"] != 0):
            seasonDict[row["Away"]]["opp_pfc_TS%"].append(homeResults["pfc_PTS"] / (2*(homeResults["pfc_FGA"] + 0.44*homeResults["pfc_FTA"])))
            seasonDict[row["Away"]]["opp_pfc_TO%"].append(homeResults["pfc_TOV"]/(homeResults["pfc_FGA"] + 0.44*homeResults["pfc_FTA"] + homeResults["pfc_TOV"]))
            seasonDict[row["Away"]]["opp_pfc_OREB%"].append(homeResults["pfc_OReb"] / (homeResults["pfc_OReb"] + awayResults["DReb"]))
            seasonDict[row["Away"]]["opp_pfc_FTR"].append(homeResults["pfc_FTA"] / homeResults["pfc_FGA"])

        #update each players stats
        playersInGame = []
        for b in ["s_","r1_","r2_","r3_","r4_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                if (row["h_" + b + c + "name"] == row["h_" + b + c + "name"]):
                    playersInGame.append(row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", ""))
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["PTS"] += row["h_" + b + c + "PTS"]
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["FGA"] += int(row["h_" + b + c + "FGM-A"].split("-")[1])
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["FTA"] += int(row["h_" + b + c + "FTM-A"].split("-")[1])
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["TOV"] += row["h_" + b + c + "TO"]
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["OREB"] += row["h_" + b + c + "OReb"]
                    try:
                        seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["opp_DREB"] += awayResults["DReb"] * 40 / (row["h_" + b + c + "seconds"] / 60)
                    except ZeroDivisionError:
                        seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["opp_DREB"] += 0
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["MIN"] += row["h_" + b + c + "seconds"] / 60
                    seasonDict[row["Home"]]["Players"][row["h_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["MIN_lastgame"] = row["h_" + b + c + "seconds"] / 60
        #if a player didn't play, update min_lastgame to 0
        for key in seasonDict[row["Home"]]["Players"]:
            if (key not in playersInGame):
                seasonDict[row["Home"]]["Players"][key]["MIN_lastgame"] = 0
        playersInGame = []
        for b in ["s_","r1_","r2_","r3_","r4_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                if (row["a_" + b + c + "name"] == row["a_" + b + c + "name"]):
                    playersInGame.append(row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", ""))
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["PTS"] += row["a_" + b + c + "PTS"]
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["FGA"] += int(row["a_" + b + c + "FGM-A"].split("-")[1])
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["FTA"] += int(row["a_" + b + c + "FTM-A"].split("-")[1])
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["TOV"] += row["a_" + b + c + "TO"]
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["OREB"] += row["a_" + b + c + "OReb"]
                    try:
                        seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["opp_DREB"] += homeResults["DReb"] * 40 / (row["a_" + b + c + "seconds"] / 60)
                    except ZeroDivisionError:
                        seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["opp_DREB"] += 0
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["MIN"] += row["a_" + b + c + "seconds"] / 60
                    seasonDict[row["Away"]]["Players"][row["a_" + b + c + "name"].replace(".", "").replace("'", "").replace("-", " ").replace(",", "")]["MIN_lastgame"] = row["a_" + b + c + "seconds"] / 60
        for key in seasonDict[row["Away"]]["Players"]:
            if (key not in playersInGame):
                seasonDict[row["Away"]]["Players"][key]["MIN_lastgame"] = 0


        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1

    A.dictToCsv("./csv_data/" + league + "/preMatchAverages.csv")

def interactionTerms(league):
    data = pd.read_csv("./csv_data/" + league + "/preMatchAverages.csv", encoding = "ISO-8859-1")
    dict = {}
    for col in data.columns:
        if (("gsf" in col or "pfc" in col) and "opp_" not in col and "I_" not in col):
            dict[col] = []
        if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "_GP" not in col and "Pace" not in col and "_D" not in col and "I_" not in col):
            dict[col] = []
        if (("H_" in col or "A_" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            dict["P_" + col] = []
    for index, row in data.iterrows():
        curPace = (row["H_Pace"] + row["A_Pace"]) / 2
        for col in data.columns:
            if (("gsf" in col or "pfc" in col) and "opp_" not in col and "I_" not in col):
                if ("H_" in col):
                    dict[col].append(row[col] * row[col.replace("H","A_opp")])
                if ("A_" in col):
                    dict[col].append(row[col] * row[col.replace("A","H_opp")])
            if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "_GP" not in col and "Pace" not in col and "_D" not in col and "I_" not in col):
                if ("H_" in col and "ORtg" not in col):
                    dict[col].append(row[col] * row[col.replace("H_","A_D")])
                elif ("H_" in col):
                    dict[col].append(row[col] * row["A_DRtg"])
                if ("A_" in col and "ORtg" not in col):
                    dict[col].append(row[col] * row[col.replace("A_","H_D")])
                elif ("A_" in col):
                    dict[col].append(row[col] * row["H_DRtg"])
            if (("H_" in col or "A_" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
                dict["P_" + col].append(row[col] * curPace)
    for key in dict:
        if ("P_" not in key):
            data["I_" + key] = dict[key]
        else:
            data[key] = dict[key]
    data.to_csv("./csv_data/" + league + "/preMatchAverages.csv", index = False)

def train_test_split(league):
    data = pd.read_csv("./csv_data/" + league + "/preMatchAverages.csv", encoding = "ISO-8859-1")
    test = False
    trainRows = []
    testRows = []
    for index, row in data.iterrows():
        #used to be 2017
        if (row["Date"].split("-")[0] == "2017" and abs(datetime.date(int(row["Date"].split("-")[0]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[2])) - datetime.date(int(data.at[index-1,"Date"].split("-")[0]), int(data.at[index-1,"Date"].split("-")[1]), int(data.at[index-1,"Date"].split("-")[2]))).days > 30):
            test = True
        if (test):
            testRows.append(index)
        else:
            trainRows.append(index)
    data.iloc[trainRows].to_csv("./csv_data/" + league + "/train.csv", index = False)
    data.iloc[testRows].to_csv("./csv_data/" + league + "/test.csv", index = False)

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
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    greedyTestLeagues = ["France","Italy","Spain","Germany"]
    if (league in greedyTestLeagues):
        greedyTestLeagues.remove(league)
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    # for l in greedyTestLeagues:
    #     new = pd.read_csv("./csv_data/" + l + "/test.csv", encoding = "ISO-8859-1")
    #     new = new[new["Home Score"].notna()]
    #     train = train.append(new, ignore_index = True)
    test = pd.read_csv("./csv_data/" + league + "/test.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    xCols = []
    for col in train.columns:
        if (("gsf" in col or "pfc" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    #print (xCols)
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

    predictions = []
    train_pred = []
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
    test["Predicted Total"] = predictions
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
        if (predictions[i] < test_OpenTotals[i]):
            tAwayOpen.append(abs(predictions[i] - test_OpenTotals[i])/sPred)
            openCoverProb.append(t.cdf(x=abs(predictions[i] - test_OpenTotals[i])/sPred, df=len(y_train) - len(xCols)))
        else:
            tAwayOpen.append(0-abs(predictions[i] - test_OpenTotals[i])/sPred)
            openCoverProb.append(t.cdf(x=0-abs(predictions[i] - test_OpenTotals[i])/sPred, df=len(y_train) - len(xCols)))
        if (predictions[i] < test_CloseTotals[i]):
            tAwayClose.append(abs(predictions[i] - test_CloseTotals[i])/sPred)
            closeCoverProb.append(t.cdf(x=abs(predictions[i] - test_CloseTotals[i])/sPred, df=len(y_train) - len(xCols)))
        else:
            tAwayClose.append(0-abs(predictions[i] - test_CloseTotals[i])/sPred)
            closeCoverProb.append(t.cdf(x=0-abs(predictions[i] - test_CloseTotals[i])/sPred, df=len(y_train) - len(xCols)))
        spredd.append(sPred)
    test["T Away Open"] = tAwayOpen
    test["T Away Close"] = tAwayClose
    test["S Pred"] = spredd
    test["Predict Open Over"] = openCoverProb
    test["Predict Close Over"] = closeCoverProb

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

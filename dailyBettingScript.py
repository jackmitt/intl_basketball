import pandas as pd
import numpy as np
from helpers import Database
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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from os.path import exists
from helpers import Database
from dateutil.relativedelta import relativedelta
import pickle
from helpers import bayesianPlayerStatsBeta
import smtplib, ssl

def kellyStake(p, decOdds, kellyDiv):
    if ((p - (1 - p)/(decOdds - 1)) / kellyDiv > 0.05):
        return (0.05)
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def scrapePinnacle(league):
    A = Database(["Date","Home","Away","Spread","Home Spread Odds","Away Spread Odds","Total","Over Total Odds","Under Total Odds"])
    driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    if (league == "Germany"):
        browser.get("https://www.pinnacle.com/en/basketball/germany-bundesliga/matchups/#period:0")
    if (league == "Spain"):
        browser.get("https://www.pinnacle.com/en/basketball/spain-acb/matchups#period:0")
    if (league == "Italy"):
        browser.get("https://www.pinnacle.com/en/basketball/italy-lega-a/matchups#period:0")
    if (league == "France"):
        browser.get("https://www.pinnacle.com/en/basketball/france-championnat-pro-a/matchups#period:0")
    if (league == "France2"):
        browser.get("https://www.pinnacle.com/en/basketball/france-championnat-pro-b/matchups#period:0")
    if (league == "Germany2"):
        browser.get("https://www.pinnacle.com/en/basketball/germany-pro-a/matchups#period:0")
    if (league == "Italy2"):
        browser.get("https://www.pinnacle.com/en/basketball/italy-lega-nazionale-pallacanestro-gold/matchups#period:0")
    if (league == "VTB"):
        browser.get("https://www.pinnacle.com/en/basketball/europe-vtb-united-league/matchups#period:0")
    if (league == "Euroleague"):
        browser.get("https://www.pinnacle.com/en/basketball/europe-euroleague/matchups#period:0")
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find(class_="contentBlock square")
    for game in main.contents:
        try:
            fail = game.find_all("span")[8].text
        except:
            continue
        A.addCellToRow(datetime.date.today())
        if ("ERROR" in standardizeTeamName(game.find_all("span")[0].text, league)):
            print (standardizeTeamName(game.find_all("span")[0].text, league))
        if ("ERROR" in standardizeTeamName(game.find_all("span")[1].text, league)):
            print (standardizeTeamName(game.find_all("span")[1].text, league))

        A.addCellToRow(standardizeTeamName(game.find_all("span")[0].text, league))
        A.addCellToRow(standardizeTeamName(game.find_all("span")[1].text, league))
        A.addCellToRow(game.find_all("span")[3].text)
        A.addCellToRow(game.find_all("span")[4].text)
        A.addCellToRow(game.find_all("span")[6].text)
        A.addCellToRow(game.find_all("span")[9].text)
        A.addCellToRow(game.find_all("span")[10].text)
        A.addCellToRow(game.find_all("span")[12].text)
        A.appendRow()
    browser.close()
    return (A.getDataFrame())

def updateSeasonStats(league, last_date):
    if (not exists("./csv_data/" + league + "/Current Season/gameStatsNew.csv")):
        oldUrls = []
    else:
        oldUrls = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")["url"].tolist()
    with open("./csv_data/" + league + "/player_priors.pkl","rb") as inputFile:
        priorDict = pickle.load(inputFile)
    A = Database(["Date","Home","Away","Poss","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","url"])
    for a in ["h_","a_"]:
        for b in ["s_","r1_","r2_","r3_","r4_","l1_","l2_","l3_"]:
            for c in ["pg_","sg_","sf_","pf_","c_"]:
                for d in ["name","seconds","FGM-A","3PM-A","FTM-A","FIC","OReb","DReb","Ast","PF","STL","TO","BLK","PTS"]:
                    A.addColumn(a + b + c + d)
    driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1325x744")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    curDate = last_date +datetime.timedelta(days=1)
    gameUrls = []
    playerUrls = []
    if (league == "Germany"):
        urlRoot = "https://basketball.realgm.com/international/league/15/German-BBL/scores/"
    elif (league == "Spain"):
        urlRoot = "https://basketball.realgm.com/international/league/4/Spanish-ACB/scores/"
    elif (league == "Italy"):
        urlRoot = "https://basketball.realgm.com/international/league/6/Italian-Lega-Basket-Serie-A/scores/"
    elif (league == "France"):
        urlRoot = "https://basketball.realgm.com/international/league/12/French-Jeep-Elite/scores/"
    elif (league == "France2"):
        urlRoot = "https://basketball.realgm.com/international/league/50/French-LNB-Pro-B/scores/"
    elif (league == "Germany2"):
        urlRoot = "https://basketball.realgm.com/international/league/94/German-Pro-A/scores/"
    elif (league == "Italy2"):
        urlRoot = "https://basketball.realgm.com/international/league/54/Italian-Serie-A2-Basket/scores/"
    elif (league == "VTB"):
        urlRoot = "https://basketball.realgm.com/international/league/35/VTB-United-League/scores/"
    elif (league == "Euroleague"):
        urlRoot = "https://basketball.realgm.com/international/league/1/Euroleague/scores/"
    while (curDate < datetime.date.today()+datetime.timedelta(days=1)):
        browser.get(curDate.strftime(urlRoot + "%Y-%m-%d/All"))
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        all = soup.find(class_="large-column-left scoreboard")
        for t in all.find_all("table"):
            for h in t.find_all('a'):
                if (h.has_attr("href") and "boxscore" in h['href']):
                    if (h['href'] not in gameUrls and h["href"] not in oldUrls):
                        gameUrls.append(h['href'])
        curDate = curDate + datetime.timedelta(days=1)

    for game in gameUrls:
        browser.get("https://basketball.realgm.com" + game)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        A.addCellToRow(game.split("boxscore/")[1].split("/")[0])
        A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[1].find_all("td")[0].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[0].find_all("td")[0].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[0].find_all("td")[1].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[1].find_all("td")[2].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[0].find_all("td")[2].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[1].find_all("td")[1].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[0].find_all("td")[1].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[1].find_all("td")[2].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[0].find_all("td")[2].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[1].find_all("td")[3].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[0].find_all("td")[3].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[1].find_all("td")[4].text)
        A.addCellToRow(soup.find_all(class_="basketball force-table")[2].find("tbody").find_all("tr")[0].find_all("td")[4].text)
        A.addCellToRow(soup.find_all(class_="tablesaw compact tablesaw-swipe tablesaw-sortable")[1].find("tfoot").find_all("tr")[1].find_all("td")[8].text)
        A.addCellToRow(soup.find_all(class_="tablesaw compact tablesaw-swipe tablesaw-sortable")[0].find("tfoot").find_all("tr")[1].find_all("td")[8].text)
        A.addCellToRow(game)

        for z in ["h", "a"]:
            if (z == "h"):
                hdc = soup.find(class_="large-column-left").find_all("table")[1].find("tbody")
                hbs = soup.find_all(class_="tablesaw compact tablesaw-swipe tablesaw-sortable")[1].find("tbody")
            else:
                hdc = soup.find(class_="large-column-left").find_all("table")[0].find("tbody")
                hbs = soup.find_all(class_="tablesaw compact tablesaw-swipe tablesaw-sortable")[0].find("tbody")
            roles = ["s","r","r","r","r","l","l","l"]
            for tr in hdc.find_all("tr"):
                while (tr.find("strong").text == "Lim PT" and roles[0] == "r"):
                    for i in range(14*5):
                        A.addCellToRow(np.nan)
                    del roles[0]
                for td in tr.find_all("td"):
                    if (td["data-th"] != "Role"):
                        try:
                            curDude = td.find("a").text
                        except:
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
                            continue
                        A.addCellToRow(curDude)
                        for p in hbs.find_all("tr"):
                            if (p.find("a").text == curDude):
                                A.addCellToRow(int(p.find_all("td")[4].text.split(":")[0]) * 60 + int(p.find_all("td")[4].text.split(":")[1]))
                                A.addCellToRow(p.find_all("td")[5].text)
                                A.addCellToRow(p.find_all("td")[6].text)
                                A.addCellToRow(p.find_all("td")[7].text)
                                A.addCellToRow(p.find_all("td")[8].text)
                                A.addCellToRow(p.find_all("td")[9].text)
                                A.addCellToRow(p.find_all("td")[10].text)
                                A.addCellToRow(p.find_all("td")[12].text)
                                A.addCellToRow(p.find_all("td")[13].text)
                                A.addCellToRow(p.find_all("td")[14].text)
                                A.addCellToRow(p.find_all("td")[15].text)
                                A.addCellToRow(p.find_all("td")[16].text)
                                A.addCellToRow(p.find_all("td")[17].text)
                del roles[0]
            for i in range(len(roles)*5*14):
                A.addCellToRow(np.nan)

        A.appendRow()


        for team in soup.find_all(class_="tablesaw compact tablesaw-swipe tablesaw-sortable"):
            for x in team.find_all("a"):
                if (x.has_attr("href")):
                    if (x['href'] not in playerUrls):
                        if (x['href'].split("player/")[1].split("/Summary")[0].replace("-", " ") not in priorDict):
                            playerUrls.append(x['href'])

    if (not exists("./csv_data/" + league + "/Current Season/gameStatsNew.csv")):
        A.dictToCsv("./csv_data/" + league + "/Current Season/gameStatsNew.csv")
    else:
        stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
        temp = A.getDataFrame()
        stats = stats.append(temp)
        #fix bayreuth name Germany
        if (league == "Germany"):
            for index, row in stats.iterrows():
                if (row["Home"] == "BAY" and "Bayreuth" in row["url"].split("-at-")[1]):
                    stats.at[index, "Home"] = "BAYR"
                if (row["Away"] == "BAY" and "Bayreuth" in row["url"].split("-at-")[0]):
                    stats.at[index, "Away"] = "BAYR"
        #Fix Fortitudo bologna Italy
        if (league == "Italy"):
            for index, row in stats.iterrows():
                if (row["Home"] == "BOL" and "Fortituto-Kontatto" in row["url"].split("-at-")[1]):
                    stats.at[index, "Home"] = "BOLO"
                if (row["Away"] == "BOL" and "Fortituto-Kontatto" in row["url"].split("-at-")[0]):
                    stats.at[index, "Away"] = "BOLO"
        stats.to_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", index = False)

    for url in playerUrls:
        browser.get("https://basketball.realgm.com" + url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")] = {}
        for x in soup.find_all("h2"):
            if (x.text == "International Regular Season Stats - Totals"):
                for season in x.find_next().find_next_sibling().find("tbody").find_all("tr"):
                    if ("multiple-teams-highlight" not in season["class"]):
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text] = {}
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["GP"] = season.find_all("td")[3].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["MIN"] = season.find_all("td")[5].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["FGM"] = season.find_all("td")[6].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["FGA"] = season.find_all("td")[7].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["3PM"] = season.find_all("td")[9].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["3PA"] = season.find_all("td")[10].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["FTM"] = season.find_all("td")[12].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["FTA"] = season.find_all("td")[13].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["OREB"] = season.find_all("td")[15].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["DREB"] = season.find_all("td")[16].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["AST"] = season.find_all("td")[18].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["STL"] = season.find_all("td")[19].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["BLK"] = season.find_all("td")[20].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["TOV"] = season.find_all("td")[22].text
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["PTS"] = season.find_all("td")[23].text
            elif (x.text == "International Regular Season Stats - Advanced Stats"):
                for season in x.find_next().find_next_sibling().find("tbody").find_all("tr"):
                    if ("multiple-teams-highlight" not in season["class"]):
                        priorDict[url.split("player/")[1].split("/Summary")[0].replace("-", " ")][season.find_all("td")[0].text]["OREB%"] = season.find_all("td")[7].text
    if (len(playerUrls) != 0):
        with open("./csv_data/" + league + "/player_priors.pkl", "wb") as f:
            pickle.dump(priorDict, f)

    browser.close()

def bet(league, pinnacleLines):
    with open("./csv_data/" + league + "/player_priors.pkl","rb") as inputFile:
        priorDict = pickle.load(inputFile)
    stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_GP","A_GP","H_Pace","A_Pace","H_ORtg","A_ORtg","H_DRtg","A_DRtg","H_eFG%","A_eFG%","H_DeFG%","A_DeFG%","H_TO%","A_TO%","H_DTO%","A_DTO%","H_OR%","A_OR%","H_DOR%","A_DOR%","H_FTR","A_FTR","H_DFTR","A_DFTR","H_FIC","A_FIC","H_DFIC","A_DFIC","F_H_ORtg","F_A_ORtg","F_H_DRtg","F_A_DRtg","F_H_eFG%","F_A_eFG%","F_H_DeFG%","F_A_DeFG%","F_H_TO%","F_A_TO%","F_H_DTO%","F_A_DTO%","F_H_OR%","F_A_OR%","F_H_DOR%","F_A_DOR%","F_H_FTR","F_A_FTR","F_H_DFTR","F_A_DFTR","F_H_FIC","F_A_FIC","F_H_DFIC","F_A_DFIC","H_gsf_TS%","H_gsf_TO%","H_gsf_OREB%","H_gsf_FTR","H_pfc_TS%","H_pfc_TO%","H_pfc_OREB%","H_pfc_FTR","H_opp_gsf_TS%","H_opp_gsf_TO%","H_opp_gsf_OREB%","H_opp_gsf_FTR","H_opp_pfc_TS%","H_opp_pfc_TO%","H_opp_pfc_OREB%","H_opp_pfc_FTR","A_gsf_TS%","A_gsf_TO%","A_gsf_OREB%","A_gsf_FTR","A_pfc_TS%","A_pfc_TO%","A_pfc_OREB%","A_pfc_FTR","A_opp_gsf_TS%","A_opp_gsf_TO%","A_opp_gsf_OREB%","A_opp_gsf_FTR","A_opp_pfc_TS%","A_opp_pfc_TO%","A_opp_pfc_OREB%","A_opp_pfc_FTR","Spread","Home Spread Odds","Away Spread Odds","Total","Over Total Odds","Under Total Odds"])
    #start at 2013, updates to 2014 on index 0
    curSeasonStart = 2021
    seasonDict = {}
    for index, row in stats.iterrows():
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
    for index, row in pinnacleLines.iterrows():
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



        A.addCellToRow(row["Spread"])
        A.addCellToRow(row["Home Spread Odds"])
        A.addCellToRow(row["Away Spread Odds"])
        A.addCellToRow(row["Total"])
        A.addCellToRow(row["Over Total Odds"])
        A.addCellToRow(row["Under Total Odds"])
        A.appendRow()

    test = A.getDataFrame().dropna()

    dict = {}
    for col in test.columns:
        if (("H_" in col or "A_" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            dict["P_" + col] = []
    for index, row in test.iterrows():
        curPace = (row["H_Pace"] + row["A_Pace"]) / 2
        for col in test.columns:
            if (("H_" in col or "A_" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
                dict["P_" + col].append(row[col] * curPace)
    for key in dict:
        test[key] = dict[key]

    predictions = []
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    xCols = []
    for col in train.columns:
        if (("gsf" in col or "pfc" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Spread"]
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
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    xCols = []
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "P_" not in col and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Spread"]
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
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    xCols = []
    for col in train.columns:
        if (("gsf" in col or "pfc" in col) and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Total"]
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
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/train.csv", encoding = "ISO-8859-1")
    train = train[train["Home Score"].notna()]
    aggLeagues = ["France","Italy","Germany"]
    for l in aggLeagues:
        new = pd.read_csv("./csv_data/" + l + "/train.csv", encoding = "ISO-8859-1")
        new = new[new["Home Score"].notna()]
        train = train.append(new, ignore_index = True)
    xCols = []
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "gsf" not in col and "pfc" not in col and "_GP" not in col and "Pace" not in col and "I_" not in col):
            xCols.append(col)
            train = train[train[col].notna()]
    y_train = train["Actual Total"]
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

    bankroll = 17000
    bet = []
    amount = []
    if (league == "Spain"):
        agreewager = 0.05
        playerwager = 0.03
        teamwager = 0.00
    elif (league == "France"):
        agreewager = 0.05
        playerwager = 0.03
        teamwager = 0.00
    elif (league == "Euroleague"):
        agreewager = 0.05
        playerwager = 0.00
        teamwager = 0.00
    elif (league == "VTB"):
        agreewager = 0.05
        playerwager = 0.03
        teamwager = 0.03
    elif (league == "Italy2"):
        agreewager = 0.04
        playerwager = 0.03
        teamwager = 0.03
    elif (league == "Germany"):
        agreewager = 0.00
        playerwager = 0.04
        teamwager = 0.04
    elif (league == "Italy"):
        agreewager = 0.00
        playerwager = 0.00
        teamwager = 0.05
    for index, row in test.iterrows():
        if ((abs(row["Player Model Predicted Spread"] - float(row["Spread"])) < 3.5 or abs(row["Player Model Predicted Spread"] - float(row["Spread"])) > 7.5) and (abs(row["Team Model Predicted Spread"] - float(row["Spread"])) < 5 or abs(row["Team Model Predicted Spread"] - float(row["Spread"])) > 12.5)):
            bet.append(np.nan)
            amount.append(np.nan)
            continue
        if (abs(row["Player Model Predicted Spread"] - float(row["Spread"])) > 3.5 and abs(row["Player Model Predicted Spread"] - float(row["Spread"])) < 7.5 and abs(row["Team Model Predicted Spread"] - float(row["Spread"])) > 5 and abs(row["Team Model Predicted Spread"] - float(row["Spread"])) < 12.5):
            if (row["Player Model Predicted Spread"] < float(row["Spread"]) and row["Team Model Predicted Spread"] < float(row["Spread"])):
                if (agreewager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(row["Spread"])
                amount.append(bankroll * agreewager)
            elif (row["Player Model Predicted Spread"] > float(row["Spread"]) and row["Team Model Predicted Spread"] > float(row["Spread"])):
                if (agreewager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(0-float(row["Spread"]))
                amount.append(bankroll * agreewager)
            else:
                bet.append(np.nan)
                amount.append(np.nan)
                continue
        elif (abs(row["Player Model Predicted Spread"] - float(row["Spread"])) > 3.5 and abs(row["Player Model Predicted Spread"] - float(row["Spread"])) < 7.5):
            if (row["Player Model Predicted Spread"] < float(row["Spread"])):
                if (playerwager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(row["Spread"])
                amount.append(bankroll * playerwager)
            elif (row["Player Model Predicted Spread"] > float(row["Spread"])):
                if (playerwager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(0-float(row["Spread"]))
                amount.append(bankroll * playerwager)
        elif(abs(row["Team Model Predicted Spread"] - float(row["Spread"])) > 5 and abs(row["Team Model Predicted Spread"] - float(row["Spread"])) < 12.5):
            if (row["Team Model Predicted Spread"] < float(row["Spread"])):
                if (teamwager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(row["Spread"])
                amount.append(bankroll * teamwager)
            elif (row["Team Model Predicted Spread"] > float(row["Spread"])):
                if (teamwager == 0.00):
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
                bet.append(0-float(row["Spread"]))
                amount.append(bankroll * teamwager)
    test["Spread Bet"] = bet
    test["Spread Amount"] = amount

    bet = []
    amount = []
    if (league != "Italy2"):
        if (league == "Spain" or league == "Italy"):
            agreewager = 0.05
            playerwager = 0.03
            teamwager = 0.00
        elif (league == "France"):
            playerwager = 0.035
            agreewager = 0.06
            teamwager = 0.00
        elif (league == "Germany"):
            agreewager = 0.02
            playerwager = 0.04
            teamwager = 0.00
        elif (league == "Euroleague"):
            agreewager = 0.00
            playerwager = 0.00
            teamwager = 0.03
        elif (league == "VTB"):
            agreewager = 0.00
            playerwager = 0.00
            teamwager = 0.00
        for index, row in test.iterrows():
            if ((abs(row["Player Model Predicted Total"] - float(row["Total"])) < 5 or abs(row["Player Model Predicted Total"] - float(row["Total"])) > 12.5) and (abs(row["Team Model Predicted Total"] - float(row["Total"])) < 5 or abs(row["Team Model Predicted Total"] - float(row["Total"])) > 12.5)):
                bet.append(np.nan)
                amount.append(np.nan)
                continue
            if (abs(row["Player Model Predicted Total"] - float(row["Total"])) > 5 and abs(row["Player Model Predicted Total"] - float(row["Total"])) < 12.5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) > 5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Player Model Predicted Total"] > float(row["Total"]) and row["Team Model Predicted Total"] > float(row["Total"])):
                    if (agreewager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * agreewager)
                elif (row["Player Model Predicted Total"] < float(row["Total"]) and row["Team Model Predicted Total"] < float(row["Total"])):
                    if (agreewager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * agreewager)
                else:
                    bet.append(np.nan)
                    amount.append(np.nan)
                    continue
            elif (abs(row["Player Model Predicted Total"] - float(row["Total"])) > 5 and abs(row["Player Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Player Model Predicted Total"] > float(row["Total"])):
                    if (playerwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * playerwager)
                else:
                    if (playerwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * playerwager)
            elif (abs(row["Team Model Predicted Total"] - float(row["Total"])) > 5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Team Model Predicted Total"] > float(row["Total"])):
                    if (teamwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * teamwager)
                else:
                    if (teamwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * teamwager)
    else:
        agreewager = 0.05
        playerwager = 0.035
        teamwager = 0.035
        for index, row in test.iterrows():
            if ((abs(row["Player Model Predicted Total"] - float(row["Total"])) < 3.5 or abs(row["Player Model Predicted Total"] - float(row["Total"])) > 12.5) and (abs(row["Team Model Predicted Total"] - float(row["Total"])) < 3.5 or abs(row["Team Model Predicted Total"] - float(row["Total"])) > 12.5)):
                bet.append(np.nan)
                amount.append(np.nan)
                continue
            if (abs(row["Player Model Predicted Total"] - float(row["Total"])) > 3.5 and abs(row["Player Model Predicted Total"] - float(row["Total"])) < 12.5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) > 3.5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Player Model Predicted Total"] > float(row["Total"]) and row["Team Model Predicted Total"] > float(row["Total"])):
                    if (agreewager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * agreewager)
                elif (row["Player Model Predicted Total"] < float(row["Total"]) and row["Team Model Predicted Total"] < float(row["Total"])):
                    if (agreewager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * agreewager)
            elif (abs(row["Player Model Predicted Total"] - float(row["Total"])) > 3.5 and abs(row["Player Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Player Model Predicted Total"] > float(row["Total"])):
                    if (playerwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * playerwager)
                else:
                    if (playerwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * playerwager)
            elif (abs(row["Team Model Predicted Total"] - float(row["Total"])) > 3.5 and abs(row["Team Model Predicted Total"] - float(row["Total"])) < 12.5):
                if (row["Team Model Predicted Total"] > float(row["Total"])):
                    if (teamwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Over")
                    amount.append(bankroll * teamwager)
                else:
                    if (teamwager == 0.00):
                        bet.append(np.nan)
                        amount.append(np.nan)
                        continue
                    bet.append("Under")
                    amount.append(bankroll * teamwager)
    test["O/U Bet"] = bet
    test["O/U Amount"] = amount

    curBets = pd.read_csv("./csv_data/botbets3.0.csv", encoding = "ISO-8859-1")
    curBets = curBets.append(test)
    curBets.to_csv("./csv_data/botbets3.0.csv", index = False)

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "bbot0444@gmail.com"
    receiver_email = "jjmittenthal@crimson.ua.edu"
    password = "f3&FDvS9W7d+V!*g"
    message = """\
    Subject: """
    message = message + league + "\n\n"

    realBet = False
    for index, row in test.iterrows():
        if (row["Spread Bet"] == row["Spread Bet"]):
            realBet = True
            if (row["Spread Bet"] == row["Spread"]):
                message = message + row["Home"] + " " + str(row["Spread Bet"]) + " Vs. " + row["Away"] + "\nOdds: " + str(row["Home Spread Odds"]) + "\nAmount: " + str(row["Spread Amount"]) + "\n\n"
            else:
                message = message + row["Home"] + " Vs. " + row["Away"] + " " + str(row["Spread Bet"]) + "\nOdds: " + str(row["Away Spread Odds"]) + "\nAmount: " + str(row["Spread Amount"]) + "\n\n"
        if (row["O/U Bet"] == row["O/U Bet"]):
            realBet = True
            if (row["O/U Bet"] == "Over"):
                message = message + row["Home"] + " Vs. " + row["Away"] + "Over " + str(row["Total"]) + "\nOdds: " + str(row["Over Total Odds"]) + "\nAmount: " + str(row["O/U Amount"]) + "\n\n"
            else:
                message = message + row["Home"] + " Vs. " + row["Away"] + "Under " + str(row["Total"]) + "\nOdds: " + str(row["Under Total Odds"]) + "\nAmount: " + str(row["O/U Amount"]) + "\n\n"
    if (realBet):
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


#league = "Italy2"
# stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
# last = stats.at[len(stats.index) - 1, "Date"]
# updateSeasonStats(league, datetime.date(int(last.split("-")[0]), int(last.split("-")[1]), int(last.split("-")[2])))
#updateSeasonStats(league, datetime.date(2021, 9, 1))
#bet(league, scrapePinnacle(league))

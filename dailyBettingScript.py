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

def kellyStake(p, decOdds, kellyDiv):
    if ((p - (1 - p)/(decOdds - 1)) / kellyDiv > 0.05):
        return (0.05)
    return ((p - (1 - p)/(decOdds - 1)) / kellyDiv)

def scrapePinnacle(league):
    A = Database(["Date","Home","Away","Home ML","Away ML","Spread","Home Spread Odds","Away Spread Odds"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
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
    #if (league == "Spain2")
        #
    time.sleep(5)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    main = soup.find(class_="contentBlock square")
    for game in main.contents:
        try:
            fail = game.find_all("span")[3].text
        except:
            continue
        A.addCellToRow(datetime.date.today())
        if ("ERROR" in standardizeTeamName(game.find_all("span")[0].text, league)):
            print (standardizeTeamName(game.find_all("span")[0].text, league))
        if ("ERROR" in standardizeTeamName(game.find_all("span")[1].text, league)):
            print (standardizeTeamName(game.find_all("span")[1].text, league))

        A.addCellToRow(standardizeTeamName(game.find_all("span")[0].text, league))
        A.addCellToRow(standardizeTeamName(game.find_all("span")[1].text, league))
        A.addCellToRow(-1)
        A.addCellToRow(-1)
        A.addCellToRow(game.find_all("span")[3].text)
        A.addCellToRow(game.find_all("span")[4].text)
        A.addCellToRow(game.find_all("span")[6].text)
        A.appendRow()
    browser.close()
    return (A.getDataFrame())

def updateSeasonStats(league, last_date):
    A = Database(["Date","Home","Away","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","url"])
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=driver_path, options = chrome_options)
    browser.maximize_window()
    curDate = last_date +datetime.timedelta(days=1)
    gameUrls = []
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
    while (curDate < datetime.date.today()+datetime.timedelta(days=1)):
        browser.get(curDate.strftime(urlRoot + "%Y-%m-%d/All"))
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        all = soup.find(class_="large-column-left scoreboard")
        for t in all.find_all("table"):
            for h in t.find_all('a'):
                if (h.has_attr("href") and "boxscore" in h['href']):
                    if (h['href'] not in gameUrls):
                        gameUrls.append(h['href'])
        curDate = curDate + datetime.timedelta(days=1)

    for game in gameUrls:
        browser.get("https://basketball.realgm.com" + game)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        A.addCellToRow(game.split("boxscore/")[1].split("/")[0])
        if ("ERROR" in standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[1].text, league)):
            print (standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[1].text, league))
        A.addCellToRow(standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[1].text, league))
        if ("ERROR" in standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[0].text, league)):
            print (standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[0].text, league))
        A.addCellToRow(standardizeTeamName(soup.find(class_="boxscore-gamedetails").find_all("a")[0].text, league))
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
        A.appendRow()
    if (not exists("./csv_data/" + league + "/Current Season/gameStats.csv")):
        A.dictToCsv("./csv_data/" + league + "/Current Season/gameStats.csv")
    else:
        stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStats.csv", encoding = "ISO-8859-1")
        temp = A.getDataFrame()
        stats = stats.append(temp)
        stats.to_csv("./csv_data/" + league + "/Current Season/gameStats.csv", index = False)

    browser.close()

def bet(league, pinnacleLines):
    stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStats.csv", encoding = "ISO-8859-1")
    A = Database(["Date","Home","Away","H_GP","A_GP","H_ORtg","A_ORtg","H_DRtg","A_DRtg","H_eFG%","A_eFG%","H_DeFG%","A_DeFG%","H_TO%","A_TO%","H_DTO%","A_DTO%","H_OR%","A_OR%","H_DOR%","A_DOR%","H_FTR","A_FTR","H_DFTR","A_DFTR","H_FIC","A_FIC","H_DFIC","A_DFIC","F_H_ORtg","F_A_ORtg","F_H_DRtg","F_A_DRtg","F_H_eFG%","F_A_eFG%","F_H_DeFG%","F_A_DeFG%","F_H_TO%","F_A_TO%","F_H_DTO%","F_A_DTO%","F_H_OR%","F_A_OR%","F_H_DOR%","F_A_DOR%","F_H_FTR","F_A_FTR","F_H_DFTR","F_A_DFTR","F_H_FIC","F_A_FIC","F_H_DFIC","F_A_DFIC","Home ML","Away ML","Spread","Home Spread Odds","Away Spread Odds"])
    for index, row in stats.iterrows():
        if (index == 0):
            seasonDict = {}
        if (row["Home"] not in seasonDict):
            seasonDict[row["Home"]] = {"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"adj_ORtg":[],"adj_DRtg":[],"adj_eFG%":[],"adj_DeFG%":[],"adj_TO%":[],"adj_DTO%":[],"adj_OR%":[],"adj_DOR%":[],"adj_FTR":[],"adj_DFTR":[],"adj_FIC":[],"adj_DFIC":[],"GP":0}
        if (row["Away"] not in seasonDict):
            seasonDict[row["Away"]] = {"ORtg":[],"DRtg":[],"eFG%":[],"DeFG%":[],"TO%":[],"DTO%":[],"OR%":[],"DOR%":[],"FTR":[],"DFTR":[],"FIC":[],"DFIC":[],"adj_ORtg":[],"adj_DRtg":[],"adj_eFG%":[],"adj_DeFG%":[],"adj_TO%":[],"adj_DTO%":[],"adj_OR%":[],"adj_DOR%":[],"adj_FTR":[],"adj_DFTR":[],"adj_FIC":[],"adj_DFIC":[],"GP":0}
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

        seasonDict[row["Away"]]["GP"] += 1
        seasonDict[row["Home"]]["GP"] += 1
    for index, row in pinnacleLines.iterrows():
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

        A.addCellToRow(row["Home ML"])
        A.addCellToRow(row["Away ML"])
        A.addCellToRow(row["Spread"])
        A.addCellToRow(row["Home Spread Odds"])
        A.addCellToRow(row["Away Spread Odds"])
        A.appendRow()

    test = A.getDataFrame()

    predictions = []
    train_pred = []
    train = pd.read_csv("./csv_data/Spain/backup/train.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    aggLeagues = ["Italy","Germany","France"]
    for l in aggLeagues:
        train = train.append(pd.read_csv("./csv_data/" + l + "/backup/train.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True), ignore_index = True)
    xCols = []
    for col in train.columns:
        if (("H_" in col or "A_" in col) and "_GP" not in col):
            xCols.append(col)
    y_train = train["Actual Spread"]
    test_OpenSpreads = test["Spread"]
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
    openCoverProb = []
    spredd = []
    for i in range(len(predictions)):
        sPred = math.sqrt(mean_squared_error(y_train, train_pred) + np.matmul(np.matmul(X_test.to_numpy()[i],mean_squared_error(y_train, train_pred)*inv(np.matmul(np.transpose(X_train.to_numpy()),X_train.to_numpy()))), np.transpose(X_test.to_numpy()[i])))
        if (predictions[i] < float(test_OpenSpreads[i])):
            tAwayOpen.append(abs(predictions[i] - float(test_OpenSpreads[i]))/sPred)
            openCoverProb.append(t.cdf(x=abs(predictions[i] - float(test_OpenSpreads[i]))/sPred, df=len(y_train) - len(xCols)))
        else:
            tAwayOpen.append(0-abs(predictions[i] - float(test_OpenSpreads[i]))/sPred)
            openCoverProb.append(t.cdf(x=0-abs(predictions[i] - float(test_OpenSpreads[i]))/sPred, df=len(y_train) - len(xCols)))
        spredd.append(sPred)
    test["T Away"] = tAwayOpen
    test["S Pred"] = spredd
    test["Predict Home Cover"] = openCoverProb

    bankroll = 19000
    bet = []
    amount = []
    kellyDiv = 1
    lowConfLeagues = ["Spain","France","Italy","Germany","VTB"]
    highConfLeagues = ["Italy2","France2","Germany2"]
    if (league in lowConfLeagues):
        p = 0.55
    else:
        p = 0.6
    for index, row in test.iterrows():
        if (abs(row["Predicted Spread"] - float(row["Spread"])) < 5):
            bet.append(np.nan)
            amount.append(np.nan)
            continue
        elif (row["Predict Home Cover"] > 1 / float(row["Home Spread Odds"])):
            bet.append(row["Spread"])
            amount.append(bankroll * kellyStake(p, float(row["Home Spread Odds"]), kellyDiv))
        elif (1 - row["Predict Home Cover"] > 1 / float(row["Away Spread Odds"])):
            bet.append(0-float(float(row["Spread"])))
            amount.append(bankroll * kellyStake(p, float(row["Away Spread Odds"]), kellyDiv))
        else:
            bet.append(np.nan)
            amount.append(np.nan)
    test["Bet"] = bet
    test["Amount"] = amount
    curBets = pd.read_csv("./csv_data/bets.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
    curBets = curBets.append(test)
    curBets.to_csv("./csv_data/bets.csv", index = False)


league = "France2"
stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStats.csv", encoding = "ISO-8859-1").dropna().reset_index(drop=True)
last = stats.at[len(stats.index) - 1, "Date"]
updateSeasonStats(league, datetime.date(int(last.split("-")[0]), int(last.split("-")[1]), int(last.split("-")[2])))
#updateSeasonStats(league, datetime.date(2021, 9, 22))
#bet(league, scrapePinnacle(league))

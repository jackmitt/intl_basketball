import dailyBettingScript as dbs
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
import gc



leagues = ["Spain","France","Italy","Germany","Euroleague","VTB","Italy2"]
for league in leagues:
    #with open("./PieUpdates/" + league + ".txt", 'r') as file:
        #date_time = datetime.datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S)")
    #statsGood = True
    #if (abs((date_time - datetime.datetime.now()).total_seconds()) > 7 * 60 * 60):
        #statsGood = False
        #try:
    # stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
    # last = stats.at[len(stats.index) - 1, "Date"]
    # dbs.updateSeasonStats(league, datetime.date(int(last.split("-")[0]), int(last.split("-")[1]), int(last.split("-")[2])))
    # with open("./PieUpdates/" + league + ".txt", 'w') as file:
    #     file.write(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"))
    statsGood = True
        #except:
        #print ("Failed to update season stats for " + league)
    # if (statsGood):
    #     try:
    lines = dbs.scrapePinnacle(league)
    curBets = pd.read_csv("./csv_data/botbets3.0.csv", encoding = "ISO-8859-1")
    if (not lines.empty):
        droprows = []
        for index, row in lines.iterrows():
            for i, r in curBets.iterrows():
                if (row["Home"] == r["Home"] and row["Away"] == r["Away"] and abs(row["Date"] - datetime.date(int(r["Date"].split("-")[0]), int(r["Date"].split("-")[1]), int(r["Date"].split("-")[2]))).days <= 2):
                    droprows.append(index)
                    break
        lines = lines.drop(droprows)
        if (not lines.empty):
            dbs.bet(league, lines)
        # except:
        #     print("Failed to scrape pinnacle / bet for " + league)

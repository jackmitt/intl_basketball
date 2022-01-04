from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from os.path import exists
from helpers import Database
import datetime

def americanToDecimal(odds):
    if (odds < 0):
        return (1 - (100 / odds))
    else:
        return (odds/100 + 1)


## Scrapes regular season closing betting lines from oddsportal (consensus average) for all seasons since 2008/2009 and saves them to a csv - Make sure you have chromedriver.exe for the correct version of Chrome
## Take out the covid bubble games yourself manually
def oddsportal(yearStart, yearEnd):
    A = Database(["Season","Date","Home","Away","Home ML","Away ML","Favorite","Spread","Home Spread Odds","Away Spread Odds","Home Score","Away Score","url"])
    seasons = []
    for i in range(yearStart, yearEnd+1):
        seasons.append(str(i) + "-" + str(i+1))
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    if (not exists("./gameUrls.csv")):
        gameUrls = []
        for season in seasons:
            browser.get("https://www.oddsportal.com/basketball/spain/acb-" + season + "/results/")
            browser.maximize_window()
            for i in range(10):
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                main = soup.find(class_="table-main")
                regSeason = False
                for row in main.find_all("tr"):
                    if ("nob-border" in row["class"]):
                        if ("Offs" in row.find("th").text or "Pre" in row.find("th").text):
                            regSeason = False
                        else:
                            regSeason = True
                    if (regSeason and "deactivate" in row["class"]):
                        gameUrls.append("https://www.oddsportal.com/" + row.find(class_="name table-participant").find("a")["href"])
                browser.find_element_by_xpath("//*[@id='pagination']/a[9]/span").click()
                time.sleep(3)
        save = {}
        save["urls"] = gameUrls
        dfFinal = pd.DataFrame.from_dict(save)
        dfFinal = dfFinal.drop_duplicates()
        dfFinal.to_csv("./gameUrls.csv", index = False)
    else:
        gameUrls = pd.read_csv('./gameUrls.csv', encoding = "ISO-8859-1")["urls"].tolist()

    counter = 0
    if (exists("./csv_data/bettingLines.csv")):
        A.initDictFromCsv("./csv_data/bettingLines.csv")
        scrapedGames = pd.read_csv('./csv_data/bettingLines.csv', encoding = "ISO-8859-1")["url"].tolist()
        for game in scrapedGames:
            gameUrls.remove(game)

    for game in gameUrls:
        browser.get(game)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        #season
        A.addCellToRow(game.split("acb-")[1].split("-")[0] + '/' + game.split("acb-")[1].split("-")[1].split("/")[0])
        #date
        A.addCellToRow(soup.find(id="col-content").find("p").text)
        #home
        A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[0])
        #away
        A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[1])
        #moneylines
        pinnacleFound = False
        for row in soup.find(class_="table-container").find_all("tr"):
            try:
                sportsbook = row.find(class_="name").text
            except:
                continue
            if (sportsbook == "Pinnacle"):
                pinnacleFound = True
                #home
                A.addCellToRow(row.find_all("td")[1].text)
                #away
                A.addCellToRow(row.find_all("td")[2].text)
        if (not pinnacleFound):
            A.addCellToRow(np.nan)
            A.addCellToRow(np.nan)
        #spread stuff
        try:
            browser.find_element_by_xpath("//*[@id='bettype-tabs']/ul/li[4]/a/span").click()
        except:
            A.trashRow()
            continue
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        minDiff = 99999
        for option in soup.find(id="odds-data-table").find_all("div"):
            try:
                diff = abs(americanToDecimal(float(option.find_all("a")[1].text)) - americanToDecimal(float(option.find_all("a")[2].text)))
                sp1 = americanToDecimal(float(option.find_all("a")[1].text))
                sp2 = americanToDecimal(float(option.find_all("a")[2].text))
            except:
                continue
            if (diff < minDiff and sp1 > 1.87 and sp2 > 1.87):
                bestSpread = option
                minDiff = diff
        #favorite
        try:
            if ("+" in bestSpread.find("a").text):
                A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[1])
            elif ("-" in bestSpread.find("a").text):
                A.addCellToRow(soup.find(id="col-content").find("h1").text.split(" - ")[0])
            else:
                A.addCellToRow("Even")
        except:
            A.trashRow()
            continue
        #spread
        if ("+" in bestSpread.find("a").text):
            A.addCellToRow(bestSpread.find("a").text.split("+")[1])
        elif ("-" in bestSpread.find("a").text):
            A.addCellToRow(bestSpread.find("a").text.split("-")[1])
        else:
            A.addCellToRow(0)
        #home spread odds
        A.addCellToRow(bestSpread.find_all("a")[1].text)
        #away spread odds
        A.addCellToRow(bestSpread.find_all("a")[2].text)
        #home score
        try:
            A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[0])
        except:
            A.trashRow()
            continue
        #away score
        if ("OT" in soup.find(class_="result").find("strong").text.split(":")[1]):
            A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[1].split(" OT")[0])
        else:
            A.addCellToRow(soup.find(class_="result").find("strong").text.split(":")[1])
        A.addCellToRow(game)
        A.appendRow()
        counter += 1
        if (counter % 20 == 1):
            A.dictToCsv("./csv_data/bettingLines.csv")
    # except:
    #     browser.close()
    #     print ("SCRAPER FAILED. RESTARTING...")
    #     oddsportal(yearStart, yearEnd)

    A.dictToCsv("./csv_data/bettingLines.csv")
    browser.close()

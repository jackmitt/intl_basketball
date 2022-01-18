from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from os.path import exists
from helpers import Database
import datetime
from dateutil.relativedelta import relativedelta

def americanToDecimal(odds):
    if (odds < 0):
        return (1 - (100 / odds))
    else:
        return (odds/100 + 1)


#Scrapes regular season closing betting lines from oddsportal (consensus average) for all seasons since 2008/2009 and saves them to a csv - Make sure you have chromedriver.exe for the correct version of Chrome
#Take out the covid bubble games yourself manually
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
    try:
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
    except:
        browser.close()
        print ("SCRAPER FAILED. RESTARTING...")
        oddsportal(yearStart, yearEnd)

    A.dictToCsv("./csv_data/bettingLines.csv")
    browser.close()

def realgm(urlRoot, year, month, day):
    A = Database(["Date","Home","Away","h_ORtg","a_ORtg","h_eFG%","a_eFG%","h_TO%","a_TO%","h_OR%","a_OR%","h_FTR","a_FTR","h_FIC","a_FIC","url"])
    league = urlRoot.split("/scores")[0].split("/")[6]
    print (league)
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.maximize_window()
    if (not exists("./" + league + "_realgm_gameUrls.csv")):
        curDate = datetime.date(year, month, day)
        gameUrls = []
        while (curDate < datetime.date(2022, 1, 1)):
            browser.get(curDate.strftime(urlRoot + "%Y-%m-%d/All"))
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            all = soup.find(class_="large-column-left scoreboard")
            for t in all.find_all("table"):
                for h in t.find_all('a'):
                    #print (t.find_all("tr")[3].find("th").find("a")['href'])
                    if (h.has_attr("href") and "boxscore" in h['href']):
                        if (h['href'] not in gameUrls):
                            gameUrls.append(h['href'])
            curDate = curDate + datetime.timedelta(days=1)
        save = {}
        save["urls"] = gameUrls
        dfFinal = pd.DataFrame.from_dict(save)
        dfFinal = dfFinal.drop_duplicates()
        dfFinal.to_csv('./' + league + '_realgm_gameUrls.csv', index = False)
    else:
        gameUrls = pd.read_csv('./' + league + '_realgm_gameUrls.csv', encoding = "ISO-8859-1")["urls"].tolist()

    counter = 0
    if (exists("./csv_data/" + league + "_gameStats.csv")):
        A.initDictFromCsv("./csv_data/" + league + "_gameStats.csv")
        scrapedGames = pd.read_csv('./csv_data/' + league + '_gameStats.csv', encoding = "ISO-8859-1")["url"].tolist()
        for game in scrapedGames:
            gameUrls.remove(game)
    try:
        for game in gameUrls:
            browser.get("https://basketball.realgm.com" + game)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            A.addCellToRow(game.split("boxscore/")[1].split("/")[0])
            A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[1].find_all("td")[0].text)
            A.addCellToRow(soup.find_all(class_="basketball force-table")[1].find("tbody").find_all("tr")[0].find_all("td")[0].text)
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
            counter += 1
            if (counter % 20 == 1):
                A.dictToCsv("./csv_data/" + league + "_gameStats.csv")
    except:
        time.sleep(300)
        browser.close()
        realgm(urlRoot, year, month, day)
    A.dictToCsv("./csv_data/" + league + "_gameStats.csv")
    browser.close()

def nowgoal(urlRoot, startMonth, league):
    A = Database(["Date","Home","Away","Home Open ML","Away Open ML","Home Close ML","Away Close ML","Open Spread","Home Open Spread Odds","Away Open Spread Odds","Close Spread","Home Close Spread Odds","Away Close Spread Odds","Home Score","Away Score","url"])
    browser = webdriver.Chrome(executable_path='chromedriver.exe')
    browser.maximize_window()
    if (not exists("./" + league + "_nowgoal_gameUrls.csv")):
        if (league != "Euroleague" and league != "VTB"):
            rootier = "https://basketball.nowgoal5.com/Normal/"
            league_num = urlRoot.split("/")[5]
            if (league == "Germany2"):
                curDate = datetime.date(2015, startMonth, 1)
                curSeason = "2015-2016"
            else:
                curDate = datetime.date(2014, startMonth, 1)
                curSeason = "2014-2015"
            gameUrls = []
            while (curDate < datetime.date(2022, 1, 1)):
                try:
                    browser.get(curDate.strftime(rootier + curSeason + "/" + league_num + "?y=%Y&m=%m"))
                except:
                    time.sleep(300)
                    nowgoal(urlRoot, startMonth, league)
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                if (len(soup.find_all(class_="odds-icon1x2 r0")) > 0):
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    needToUpdate = True
                else:
                    if (needToUpdate):
                        curSeason = str(curDate.year) + "-" + str(curDate.year + 1)
                        needToUpdate = False
                curDate = curDate + relativedelta(months=+1)
            save = {}
            save["urls"] = gameUrls
            dfFinal = pd.DataFrame.from_dict(save)
            dfFinal = dfFinal.drop_duplicates()
            dfFinal.to_csv('./' + league + '_nowgoal_gameUrls.csv', index = False)
        elif (league == "VTB"):
            rootier = "https://basketball.nowgoal5.com/CupMatch/"
            league_num = urlRoot.split("/")[5]
            curDate = datetime.date(2014, startMonth, 1)
            seasons = ["2014-2015","2015-2016","2016-2017","2017-2018","2018-2019","2019-2020","2020-2021"]
            gameUrls = []
            for curSeason in seasons:
                browser.get(curDate.strftime(rootier + curSeason + "/" + league_num))
                if (curSeason == "2014-2015" or curSeason == "2015-2016" or curSeason == "2016-2017" or curSeason == "2018-2019" or curSeason == "2020-2021"):
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr/td[1]").click()
                    browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                elif (curSeason == "2017-2018"):
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[1]").click()
                    browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                elif (curSeason == "2019-2020" or curSeason == "2021-2022"):
                    browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
        else:
            rootier = "https://basketball.nowgoal5.com/CupMatch/"
            league_num = urlRoot.split("/")[5]
            curDate = datetime.date(2014, startMonth, 1)
            seasons = ["2014-2015","2015-2016","2016-2017","2017-2018","2018-2019","2019-2020","2020-2021"]
            gameUrls = []
            for curSeason in seasons:
                browser.get(curDate.strftime(rootier + curSeason + "/" + league_num))
                if (curSeason == "2014-2015"):
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[4]").click()
                    time.sleep(1)
                    for i in range(2, 6):
                        element = browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[" + str(i) + "]")
                        element.click()
                        time.sleep(1)
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        for t in soup.find_all(class_="odds-icon1x2 r0"):
                            gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[1]").click()
                    time.sleep(1)
                    for i in range(2, 4):
                        element = browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[" + str(i) + "]")
                        element.click()
                        time.sleep(1)
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        for t in soup.find_all(class_="odds-icon1x2 r0"):
                            gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[3]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[4]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[3]/td[1]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                elif (curSeason == "2019-2020"):
                    browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[2]").click()
                    time.sleep(1)
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                elif(curSeason == "2015-2016"):
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[1]").click()
                    time.sleep(1)
                    for i in range(2, 6):
                        element = browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[" + str(i) + "]")
                        element.click()
                        time.sleep(1)
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        for t in soup.find_all(class_="odds-icon1x2 r0"):
                            gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[2]").click()
                    time.sleep(1)
                    for i in range(2, 4):
                        element = browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[" + str(i) + "]")
                        element.click()
                        time.sleep(1)
                        soup = BeautifulSoup(browser.page_source, 'html.parser')
                        for t in soup.find_all(class_="odds-icon1x2 r0"):
                            gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[3]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[4]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[1]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                else:
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[1]").click()
                    time.sleep(1)
                    element = browser.find_element_by_xpath("//*[@id='showRound']/table/tbody/tr/td[2]")
                    element.click()
                    time.sleep(1)
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[2]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[3]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[1]/td[4]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])
                    browser.find_element_by_xpath("//*[@id='qualifyDiv']/table/tbody/tr[2]/td[1]").click()
                    soup = BeautifulSoup(browser.page_source, 'html.parser')
                    for t in soup.find_all(class_="odds-icon1x2 r0"):
                        gameUrls.append(t['href'])

    else:
        gameUrls = pd.read_csv('./' + league + '_nowgoal_gameUrls.csv', encoding = "ISO-8859-1")["urls"].tolist()
    #
    #
    counter = 0
    if (exists("./csv_data/" + league + "_spreads.csv")):
        A.initDictFromCsv("./csv_data/" + league + "_spreads.csv")
        scrapedGames = pd.read_csv('./csv_data/' + league + '_spreads.csv', encoding = "ISO-8859-1")["url"].tolist()
        for game in scrapedGames:
            gameUrls.remove(game)

    for game in gameUrls:
        browser.get("https:" + game)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        try:
            A.addCellToRow(soup.find(id="headStr").find("span").text.split()[0])
            A.addCellToRow(soup.find_all(class_="o_team")[0].text)
            A.addCellToRow(soup.find_all(class_="o_team")[1].text)
            try:
                A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-2].find_all("td")[1].text)
                A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-2].find_all("td")[2].text)
                A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-1].find_all("td")[1].text)
                A.addCellToRow(soup.find_all(class_="odds-table-bg")[4].find_all("tr")[-1].find_all("td")[2].text)
            except:
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
            try:
                bet365 = soup.find(class_="odds-table-bg").find_all("tr")[5]
                test = float(bet365.find_all("td")[2].find("span").text) * -1
                test = float(bet365.find_all("td")[2].find("span").text) * -1
            except:
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(np.nan)
                A.addCellToRow(soup.find_all(class_="team_bf")[0].text)
                A.addCellToRow(soup.find_all(class_="team_bf")[1].text)
                A.addCellToRow(game)
                A.appendRow()
                continue
            try:
                A.addCellToRow(float(bet365.find_all("td")[2].text.replace(bet365.find_all("td")[2].find("span").text, "")) * -1)
            except:
                A.addCellToRow(float(bet365.find_all("td")[2].find("span").text) * -1)
            A.addCellToRow(float(bet365.find_all("td")[1].find_all("span")[0].text) + 1)
            A.addCellToRow(float(bet365.find_all("td")[3].find_all("span")[0].text) + 1)
            A.addCellToRow(float(bet365.find_all("td")[2].find("span").text) * -1)
            A.addCellToRow(float(bet365.find_all("td")[1].find_all("span")[1].text) + 1)
            A.addCellToRow(float(bet365.find_all("td")[3].find_all("span")[1].text) + 1)
            A.addCellToRow(soup.find_all(class_="team_bf")[0].text)
            A.addCellToRow(soup.find_all(class_="team_bf")[1].text)
            A.addCellToRow(game)
            A.appendRow()
            counter += 1
            if (counter % 20 == 1):
                A.dictToCsv("./csv_data/" + league + "_spreads.csv")
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
            A.addCellToRow(np.nan)
            A.addCellToRow(game)
            A.appendRow()
    # except:
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(np.nan)
    #     A.addCellToRow(game)
    #     A.appendRow()
        # A.dictToCsv("./csv_data/" + league + "_spreads.csv")
        # nowgoal(urlRoot, startMonth, league)
    A.dictToCsv("./csv_data/" + league + "_spreads.csv")
    browser.close()

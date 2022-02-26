import pandas as pd
import dailyBettingScript as dbs


leagues = ["Spain","France","Italy","Germany","Euroleague","VTB","Italy2","France2"]
# leagues = ["Italy2"]
while(1):
    for league in leagues:
        with open("./PieUpdates/" + league + ".txt", 'r') as file:
            date_time = datetime.datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S)")
        statsGood = True
        if (abs(date_time - datetime.datetime.now()).hours > 6):
            statsGood = False
            try:
                stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
                last = stats.at[len(stats.index) - 1, "Date"]
                updateSeasonStats(league, datetime.date(int(last.split("-")[0]), int(last.split("-")[1]), int(last.split("-")[2])))
                with open("./PieUpdates/" + league + ".txt", 'w') as file:
                    file.write(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"))
                statsGood = True
            except:
                print ("Failed to update season stats for " + league)
            finally:
                gc.collect()
        if (statsGood):
            try:
                lines = dbs.scrapePinnacle(league)
                if (not lines.empty):
                    dbs.bet(league, lines)
            except:
                print("Failed to scrape pinnacle / bet for " + league);
            finally:
                gc.collect()
    break

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
                curBets = pd.read_csv("./csv_data/botbets2.0.csv", encoding = "ISO-8859-1")
                if (not lines.empty):
                    droprows = []
                    for index, row in lines.iterrows():
                        for i, r in curBets.iterrows():
                            if (row["Home"] == r["Home"] and row["Away"] == r["Away"] and abs(datetime.date(int(row["Date"].split("-")[0]), int(row["Date"].split("-")[1]), int(row["Date"].split("-")[2])) - datetime.date(int(r["Date"].split("-")[0]), int(r["Date"].split("-")[1]), int(r["Date"].split("-")[2]))).days <= 2):
                                droprows.append(index)
                                break
                    lines = lines.drop(droprows)
                    if (not lines.empty):
                        dbs.bet(league, lines)
            except:
                print("Failed to scrape pinnacle / bet for " + league);
            finally:
                gc.collect()
    break

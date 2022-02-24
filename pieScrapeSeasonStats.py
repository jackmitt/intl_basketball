from dailyBettingScript import updateSeasonStats
import datetime
import pandas as pd

leagues = ["Spain","France","Germany","Italy","Euroleague","France2","Italy2","VTB"]
for league in leagues:
    # with open("./PieUpdates/" + league + ".txt", 'r') as file:
    #     date_time = datetime.datetime.strptime(file.read(), "%d-%b-%Y (%H:%M:%S)")
    #     print (abs(date_time - datetime.datetime.now()).seconds)
    stats = pd.read_csv("./csv_data/" + league + "/Current Season/gameStatsNew.csv", encoding = "ISO-8859-1")
    last = stats.at[len(stats.index) - 1, "Date"]
    updateSeasonStats(league, datetime.date(int(last.split("-")[0]), int(last.split("-")[1]), int(last.split("-")[2])))
    with open("./PieUpdates/" + league + ".txt", 'w') as file:
        file.write(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"))

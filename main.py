from scrapers import oddsportal
from scrapers import realgm
from scrapers import nowgoal
import data_manipulation as dm
import prediction_evaluation as pe



leagues = ["Italy2"]
#leagues = ["Spain","France","Italy","Germany","VTB","Spain2","Italy2","France2","Germany2","Turkey"]
for league in leagues:
    print (league + "---------------------------------------------------------------------------")
    #dm.checkTeamNames(league)
    #dm.combine_spreads_and_stats(league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pe.betWithLines(20000, league = league)
    #dm.predictions(league)
    #dm.aggregateModelPredictions(league)
    #pe.simulateKellyBets(20000, 1, "Open", league)
    #pe.simulateKellyBets(20000, 1, "Close", league)
    #pe.kellySpreadBets(20000, 1, "Open", league)
    #pe.kellySpreadBets(20000, 1, "Close", league)
    #pe.betWithLines(20000, league)
    pe.analyzeMyLines(league)
#pe.simulateKellyBets(20000, kellyDiv = 1, preCovid = False)

















#realgm("https://basketball.realgm.com/international/league/7/Turkish-BSL/scores/", 2014, 10, 11)
#realgm("https://basketball.realgm.com/international/league/54/Italian-Serie-A2-Basket/scores/", 2014, 10, 5)
#realgm("https://basketball.realgm.com/international/league/50/French-LNB-Pro-B/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/55/Spanish-LEB-Gold/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/94/German-Pro-A/scores/", 2014, 9, 27)
#realgm("https://basketball.realgm.com/international/league/18/Adriatic-League-Liga-ABA/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/35/VTB-United-League/scores/", 2014, 10, 3)
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/18", 10, "Adriatic")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/228", 10, "Italy2")
#nowgoal("https://basketball.nowgoal5.com/CupMatch/2021-2022/171", 10, "VTB")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/226", 10, "Spain2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2015-2016/376", 9, "Germany2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/22", 10, "German")

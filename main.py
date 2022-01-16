from scrapers import oddsportal
from scrapers import realgm
from scrapers import nowgoal
import data_manipulation as dm
import prediction_evaluation as pe



#leagues = ["Spain","France","Italy","Germany"]
#for league in leagues:
    #print (league + "---------------------------------------------------------------------------")
    #dm.combine_spreads_and_stats(league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pe.betWithLines(20000, league = league)
    #dm.predictions(league)
    #dm.aggregateModelPredictions(league)
    #pe.simulateKellyBets(20000, 6, "Open", league)
    #pe.simulateKellyBets(20000, 6, "Close", league)
    #pe.kellySpreadBets(20000, 6, "Open", league)
    #pe.kellySpreadBets(20000, 6, "Close", league)
    #pe.betWithLines(20000, league)
    #pe.analyzeMyLines(league)
#pe.simulateKellyBets(20000, kellyDiv = 1, preCovid = False)



























realgm("https://basketball.realgm.com/international/league/7/Turkish-BSL/scores/", 2014, 10, 11)
realgm("https://basketball.realgm.com/international/league/54/Italian-Serie-A2-Basket/scores/", 2014, 10, 5)
realgm("https://basketball.realgm.com/international/league/50/French-LNB-Pro-B/scores/", 2014, 10, 3)
realgm("https://basketball.realgm.com/international/league/55/Spanish-LEB-Gold/scores/2014-10-03/", 2014, 10, 3)
realgm("https://basketball.realgm.com/international/league/94/German-Pro-A/scores/", 2014, 9, 27)
realgm("https://basketball.realgm.com/international/league/18/Adriatic-League-Liga-ABA/scores/", 2014, 10, 3)
realgm("https://basketball.realgm.com/international/league/35/VTB-United-League/scores/", 2014, 10, 3)
#nowgoal("https://basketball.nowgoal5.com/CupMatch/2014-2015/7", 10, "Euroleague")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/19", 9, "France")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/16", 10, "Italy")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/17", 10, "Greece")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/14", 10, "Australia")
#nowgoal("https://basketball.nowgoal5.com/Normal/2014-2015/22", 10, "German")

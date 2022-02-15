from scrapers import oddsportal
from scrapers import realgm
from scrapers import nowgoal
from scrapers import scrapePinnacle
from scrapers import updateSeasonStats
import data_manipulation as dm
import prediction_evaluation as pe
import pandas as pd
import datetime
import smtplib, ssl


#leagues = ["Italy2"]
#leagues = ["Spain","France","Italy","Germany","VTB","Italy2","France2","Germany2"]
#for league in leagues:
    #print (league + "---------------------------------------------------------------------------")
    #dm.checkTeamNames(league)
    #dm.combine_spreads_and_stats(league)
    #dm.preMatchAverages(league)
    #dm.train_test_split(league)
    #pe.betWithLines(20000, league = league)
    #dm.predictions(league)
    #dm.aggregateModelPredictions(league)
    #pe.simulateKellyBets(20000, 1, "Open", league)
    #pe.simulateKellyBets(20000, 1, "Close", league)
    #pe.kellySpreadBets(20000, 1, "Open", league, uf = 0)
    #pe.kellySpreadBets(20000, 1, "Close", league, uf = 0)
    #pe.betWithLines(20000, league)
    #pe.analyzeMyLines(league)
#pe.simulateKellyBets(20000, kellyDiv = 1, preCovid = False)

















#realgm("https://basketball.realgm.com/international/league/7/Turkish-BSL/scores/", 2014, 10, 11)
#realgm("https://basketball.realgm.com/international/league/54/Italian-Serie-A2-Basket/scores/", 2014, 10, 5)
#realgm("https://basketball.realgm.com/international/league/50/French-LNB-Pro-B/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/55/Spanish-LEB-Gold/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/94/German-Pro-A/scores/", 2014, 9, 27)
#realgm("https://basketball.realgm.com/international/league/18/Adriatic-League-Liga-ABA/scores/", 2014, 10, 3)
#realgm("https://basketball.realgm.com/international/league/35/VTB-United-League/scores/", 2014, 10, 3)
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/20", 9, "Spain")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/16", 10, "Italy")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/19", 9, "France")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/22", 9, "Germany")
#nowgoal("https://basketball.nowgoal5.com/CupMatch/2017-2018/171", 10, "VTB")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/225", 10, "France2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/376", 9, "Germany2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/228", 9, "Italy2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/226", 9, "Spain2")
#nowgoal("https://basketball.nowgoal5.com/Normal/2017-2018/18", 9, "ABA")
#nowgoal("https://basketball.nowgoal5.com/CupMatch/2017-2018/7", 9, "Euroleague")

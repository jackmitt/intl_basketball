from scrapers import oddsportal
from scrapers import realgm
from scrapers import nowgoal
from scrapers import scrapePinnacle
from scrapers import updateSeasonStats
from scrapers import realgmPlayerPriors
import data_manipulation as dm
import prediction_evaluation as pe
import pandas as pd
import datetime
import smtplib, ssl

leagues = ["Adriatic","VTB"]
for league in leagues:
    print (league + "---------------------------------------------------------------------------")
    dm.preMatchAverages(league)

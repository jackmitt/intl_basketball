import pandas as pd
from dailyBettingScript import scrapePinnacle
from dailyBettingScript import bet

lines = scrapePinnacle(league)
if (not lines.empty):
    bet(league, lines)

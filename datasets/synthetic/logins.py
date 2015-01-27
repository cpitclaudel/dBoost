#!/usr/bin/env python3
# Generates synthetic datasets of online logins

# Schema: Outlier, User, Timestamp, Country
# There are three users: 0, 1, and 2. User 1 always logs in from the same country. User 2 logs in from one country on weekdays, and another on weekends. User 3 logs in from various countries.

from countrydata import COUNTRY_DATA
import random
import utils

class User:
    def __init__(self, userid, countries):
        self.uid = userid
        self.countries = [country[0] for country in countries]

users = [User(uid, utils.choose_n(10, COUNTRY_DATA)) for uid in range(3)]

OUTLIERS_RATE = 0.01

def random_login():
    user = random.choice(users)
    tsp = utils.random_timestamp()
    outlier = random.random() < OUTLIERS_RATE

    if user.uid == 0:
        country = user.countries[outlier]
    elif user.uid == 1:
        country = user.countries[outlier ^ utils.isweekend(tsp)]
    elif user.uid == 2:
        country = random.choice(user.countries)
    
    return (outlier, user.uid, tsp, country)

utils.write_lines("logins", 10000, random_login)

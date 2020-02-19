#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
all these packages included with standard library - need python to run this
so, just having a python distribution means can import these
all pip installed libraries are saved to ext lib folders?!

want for this to prompt me to input starting url in console or form
then I input it, script runs and output is list of shit. Also pick numbers,
also pick price range - gets me hottest deals in range


"""

from random import randint
from time import sleep
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import re
import pandas as pd
import numpy as np
import datetime


class scraper(object):

    def __init__(self, pages, items):

        # initialize the structure
        # behaviour - modified by some methods
        self.list_dicts = []
        self.pages = pages
        self.items = items

    # ONLY NEEDS TO WORK ON ONE URL!!!!!
    # this parses the inside of the page
    # want a function to spit out an array of results for different urls
    def checker(self, page_url, fields):

        # dicitonary with urls as keys, and values are dicitonary of keys and values
        url_dict = {"url": page_url}

        # make beautiful soup out of all URLs
        # for page_url in urls:

        # print("")
        # print(page_url)

        # make beautiful soup
        uClient = uReq(page_url)
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()

        if "price" in fields:

            try:

                containers_price = page_soup.findAll("div", {"class": re.compile('priceContainer')})

                price = containers_price[0].find_all("span")[1].contents[0]

                print(price)

                # !!!
                url_dict["price"] = price

            except:

                pass

        if "address" in fields:

            try:

                containers_address = page_soup.findAll("div", {"class": re.compile('locationContainer')})

                address = containers_address[0].find_all("span")[0].contents[0]

                print(address)

                # !!!
                url_dict["address"] = address

            except:

                pass

        if "visits" in fields:

            try:

                containers_visits = page_soup.findAll("div", {"class": re.compile('visitCounter')})

                # visits_macro_string_timestamp = re.findall(r'datetime="(.+?)" title="', str(containers_timestamp[0]))

                visits = containers_visits[0].find_all("span")[0].find_all("span")[0].contents[0]

                print(visits)

                # !!!
                url_dict["visits"] = visits




            except:

                pass

        if "timestamp" in fields:

            try:

                containers_timestamp = page_soup.findAll("div", {"class": re.compile('datePosted')})

                # visits_macro_string_timestamp = re.findall(r'datetime="(.+?)" title="', str(containers_timestamp[0]))

                timestamp = containers_timestamp[0].find_all("time")[0]['datetime']

                print(timestamp)

                # !!!
                url_dict["timestamp"] = timestamp



            except:

                pass

        return url_dict

    # iterates items, and per item calls checker
    def itemParser(self, page_url):

        items = []

        # make beautiful soup object
        uClient = uReq(page_url)
        page_soup_iter = soup(uClient.read(), "html.parser")
        uClient.close()

        page_items = page_soup_iter.findAll("div", {"data-listing-id": re.compile('.*')})

        # CHANGE NUMBER HERE!!!!!
        for item in page_items[0:self.items]:
            sleep(randint(1, 5))

            # get the url - have it
            item_url = item['data-vip-url']

            page_url = "https://www.kijiji.ca" + item_url

            # print(page_url)

            # now load the url as bs
            uClient = uReq(page_url)
            page_soup_item = soup(uClient.read(), "html.parser")
            uClient.close()

            # now echo
            fields = ["timestamp", "visits", "address", "timestamp", "price"]

            # parse function
            # get all the fields here as dictionary
            dict_items = self.checker(page_url, fields)

            # add to list
            items.append(dict_items)

        return items

    # iterates pages, them runs item parser
    def interface(self, page_url):

        # list_dicts = []

        for i in range(self.pages):
            sleep(randint(1, 5))

            # echo
            print(page_url)

            # make beautiful soup object
            uClient = uReq(page_url)
            page_soup_iter = soup(uClient.read(), "html.parser")
            uClient.close()

            # THIS IS WHERE THE CODE BELOW IS RAN - ITERATE THE ITEMS
            # can capture all items here and keep appending page to page and then return
            # keep appending to list of dicitonaries
            items_list = self.itemParser(page_url)

            self.list_dicts += items_list

            # get the pagination
            containers_timestamp = page_soup_iter.findAll("div", {"class": re.compile('pagination')})

            next_page = str(containers_timestamp[0].find_all("a", title="Next")[0]["href"])

            # reassign page_url
            page_url = "https://www.kijiji.ca" + next_page

            print("!!!!!!!!!!!!!!!!!!!!!!!")

            print(page_url)

        return self.list_dicts



#"https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/c30349001l1700272"
url_input = input("Please enter starting url: ")
pages_input = input("Please enter number of pages you want to parse: ")
items_input = input("Please enter number of items per page to parse: ")
#max_price_input = input("max price?: ")

#
inst = scraper(pages=int(pages_input), items=int(items_input)).interface(url_input)









###################################################################
#######################PROCESSING OF DATA #########################
# df
def makeDf(list_input):
    return pd.DataFrame(list_input)


# df and processing
df = makeDf(inst)
#df.head()






# processing df


# udf to get time
def time_elapsed(t):
    x = datetime.datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.000Z')

    y = datetime.datetime.today()

    z = y - x

    return z.days + (z.seconds / 60 / 60 / 24)

# clean out the price and restrict df by the price
#var = '$700.00'
#print(float(var[1:]))

#clean price and convert to number


#filter price



# replace nan with 0
df['visits'] = df['visits'].replace([np.nan], '0')

# prep visits for numeric
df['visits'] = df['visits'].astype(str).apply(lambda x: x.replace(',', '') if x != np.nan else np.nan)

# to numeric
df["visits"] = pd.to_numeric(df["visits"])

# modify dates to time since posted
df['days'] = df['timestamp'].map(time_elapsed)

# get rank
df['rank'] = df['visits'] / df['days']
df = df.sort_values(by=['rank'], ascending=False)
#print(df)
#df.columns

# to array
array_urls = df[['url']].to_numpy()
array_ranks = df[['rank']].to_numpy()

for a, r in zip(array_urls, array_ranks):
    print(r)
    print(a)



    
    
    

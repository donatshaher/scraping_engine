#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:00:27 2020

@author: Don

A scraper
"""


            
            



from random import randint
from time import sleep
from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import re
import pandas as pd
import numpy as np




class scraper(object):
    
    def __init__(self, pages,items):
        
        # initialize the structure
        # behaviour - modified by some methods
        self.list_dicts = []
        self.pages = pages
        self.items = items
   
        
            
    
    
    #ONLY NEEDS TO WORK ON ONE URL!!!!!
    # this parses the inside of the page
    # want a function to spit out an array of results for different urls
    def checker(self, page_url, fields):
        
        # dicitonary with urls as keys, and values are dicitonary of keys and values
        url_dict = {"url": page_url}
        
        # make beautiful soup out of all URLs
        #for page_url in urls:
            
            
            #print("")
            #print(page_url)
            
            
        # make beautiful soup
        uClient = uReq(page_url)
        page_soup = soup(uClient.read(), "html.parser")
        uClient.close()
    
    
        # conditions
        if "price" in fields:
            
                    
            containers_price = page_soup.findAll("div", {"class": re.compile('priceContainer')})
            
            visits_macro_string_price = re.findall(r'<span content="(.+?)">', str(containers_price[0]))
            
            print(visits_macro_string_price)
            #print(list(containers_price[0].descendants)[2])
          
          
            
            
            
        if "visits" in fields:
            
            containers = page_soup.findAll("div", {"class": re.compile('visitCounter')})
    
    
            visits_macro_string = re.findall(r'(?<=<span><span>)(.+?)</span>', str(containers[0]))
            
            print(visits_macro_string)
            #list(containers[0].descendants)[4]
           
          
            
            
        if "address" in fields:
            
            containers_address = page_soup.findAll("div", {"class": re.compile('locationContainer')})
    
            visits_macro_string_adress = re.findall(r'PostalAddress">(.+?)</span><a class="mapLink-1573660252"', str(containers_address[0]))
            
            print(visits_macro_string_adress)
            
            #print(list(containers_address2[0].descendants)[3])
            
            
            
            
        if "timestamp" in fields:
            
            try:
            
                containers_timestamp = page_soup.findAll("div", {"class": re.compile('datePosted')})
    
            #visits_macro_string_timestamp = re.findall(r'datetime="(.+?)" title="', str(containers_timestamp[0]))
    
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
        
        #make beautiful soup object
        uClient = uReq(page_url)
        page_soup_iter = soup(uClient.read(), "html.parser")
        uClient.close()
        
        
        
        page_items = page_soup_iter.findAll("div", {"data-listing-id": re.compile('.*')})
        
        # CHANGE NUMBER HERE!!!!!
        for item in page_items[0:self.items]:
            
            print(1)
            
            sleep(randint(5,10))
            
            print(2)
            
            # get the url - have it
            item_url = item['data-vip-url']
            
            page_url = "https://www.kijiji.ca" + item_url
            
            #print(page_url)
            print(3)
            
            #now load the url as bs
            uClient = uReq(page_url)
            page_soup_item = soup(uClient.read(), "html.parser")
            uClient.close()
            
            #now echo
            fields = ["timestamp"]  #, "visits", "address", "timestamp" "price"]
        
            print(4)
            
            # parse function
            # get all the fields here as dictionary
            dict_items = checker(page_url, fields)
            
            print(5)
            
            # add to list
            items.append(dict_items)
            
            
            
        return items
    
    
    
            
    
    
    
    
    
    
    # iterates pages, them runs item parser
    def interface(self, page_url):
        
        #list_dicts = []
    
    
        for i in range(self.pages):
            
            
            sleep(randint(5,20))
            
            #echo
            print(page_url)
            
            
            #make beautiful soup object
            uClient = uReq(page_url)
            page_soup_iter = soup(uClient.read(), "html.parser")
            uClient.close()
                
            
            # THIS IS WHERE THE CODE BELOW IS RAN - ITERATE THE ITEMS
            # can capture all items here and keep appending page to page and then return
            # keep appending to list of dicitonaries
            items_list = itemParser(page_url)
            
            self.list_dicts += items_list
            
            
            # get the pagination
            containers_timestamp = page_soup_iter.findAll("div", {"class": re.compile('pagination')})
            
            next_page = str(containers_timestamp[0].find_all("a", title="Next")[0]["href"])
            
            
        
            # reassign page_url
            page_url = "https://www.kijiji.ca" + next_page
            
            print("!!!!!!!!!!!!!!!!!!!!!!!")
            
            print(page_url)
            
            
        return self.list_dicts
             
            
            
    
    
    
    





# df
def makeDf(list_input):
    

    return pd.DataFrame(list_input)
    
    
     



#       
inst = scraper(pages=2, items=2).interface("https://www.kijiji.ca/b-for-rent/gta-greater-toronto-area/c30349001l1700272")
    
    
    
        


        
#df and processing
print(makeDf(inst))
     
    
    
    
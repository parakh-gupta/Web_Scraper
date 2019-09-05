#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import requests
import regex as re
import json


# In[2]:


chromedriver = "C:/Users/Parakh Gupta/Downloads/setups/chromedriver" # path to the chromedriver executable
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))
sys.path.append(chromedriver)
driver = webdriver.Chrome(chromedriver)


# In[4]:


def get_house_links( driver):
    house_links=[]
    cities=['Gurgaon','Noida','Ghaziabad','Greater-Noida','Bangalore','Mumbai','Pune','Hyderabad','Kolkata','Chennai',
            'New-Delhi','Ahmedabad','Navi-Mumbai','Thane','Faridabad','Bhubaneswar','Bokaro-Steel-City','Vijayawada','Vrindavan''Bhopal',
            'Gorakhpur','Jamshedpur','Agra','Allahabad','Jodhpur''Aurangabad','Jaipur','Mangalore','Nagpur','Guntur','Navsari','Palghar','Salem','Haridwar','Durgapur',
            'Madurai','Manipal','Patna','Ranchi','Raipur','Sonipat','Kottayam','Kozhikode','Thrissur','Tirupati','Trivandrum','Trichy','Udaipur','Vapi','Varanasi',
            'Vadodara','Visakhapatnam','Surat','Kanpur','Kochi','Mysore','Goa','Bhiwadi','Lucknow','Nashik','Guwahati','Chandigarh','Indore','Coimbatore','Dehradun']
    for city in cities:
        for i in range(1,90):
            driver.get("https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&page="+str(i)+"&cityName="+str(city))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            get_data(soup)


# In[5]:


def get_data(soup):
    h=[]
    prop=soup.find_all('div',class_='m-srp-card SRCard')
    for i in prop:
        name=""
        id_=""
        description=""
        url=""
        price=""
        priceInWord=""
        cityName=""
        addressLocality=""
        longitude=""
        latitude=""
        numberOfRooms=""
        bathroom=""
        bedroom=""
        floorSize=""
        floorno=""
        furnshingstatus=""
        agentName=""
        agentCompanyName=""
        agentMaskedmobilenumber=""
        meta=i.find_all('meta')
        for m in meta:
            if m['itemprop']=='name':
                name=m['content']
            if m['itemprop']=='description':
                description=m['content']
            if m['itemprop']=='url':
                url=str('https://www.magicbricks.com'+m['content'])
            if m['itemprop']=='addressLocality':
                addressLocality=m['content']
            if m['itemprop']=='longitude':
                longitude=m['content']
            if m['itemprop']=='latitude':
                latitude=m['content']
            if m['itemprop']=='numberOfRooms':
                numberOfRooms=m['content']
            if m['itemprop']=='floorSize':
                floorSize=m['content']
        s=i.find('span',class_='hidden')
        bathroom=s['data-bathroom']
        bedroom=s['data-bedroom']
        floorno=s['data-floorno']   
        furnshingstatus=s['data-furnshingstatus']
        price=s['data-price']
        id_=s['id']
        ag=soup.find('span',id=id_)
        priceInWord=ag['data-priced']
        cityName=ag['data-cityname']
        agentName=ag['data-soname']
        agentCompanyName=ag['data-companyname']
        agentMaskedmobilenumber=ag['data-maskedmobilenumber']
        var = {
                "name":name,
                "id":id_,
                "description":description,
                "url":url,
                "price":price,
                "priceInWord":priceInWord,
                "location":
                        {
                            "cityName":cityName,
                            "addressLocality":addressLocality,
                            "longitude":longitude,
                            "latitude":latitude,
                        },
                "flatDetails":
                        {
                            "numberOfRooms":numberOfRooms,
                            "bathroom":bathroom,
                            "bedroom":bedroom,
                            "floorSize":floorSize,
                            "floorno":floorno,
                            "furnshingstatus":furnshingstatus,
                        },
                "agentDetails":
                        {
                            "agentName":agentName,
                            "agentCompanyName":agentCompanyName,
                            "agentMaskedmobilenumber":agentMaskedmobilenumber,
                        }

            }
        print(var)
        h.append(var)
    with open("data.json",'r+') as f:
        feeds = json.load(f)
        for i in h:
            feeds['property'].append(var)
        f.seek(0)
        json.dump(feeds, f)


# In[6]:


v={
    "property":[]
}
with open("data.json", mode='w', encoding='utf-8') as f:
    json.dump(v,f)


# In[ ]:


get_house_links(driver)


# In[ ]:





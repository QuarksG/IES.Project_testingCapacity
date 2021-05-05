#!/usr/bin/env python
# coding: utf-8

# This Jupiter notebook is used to download, pre-process and save data about all test data in the Czech Republic from 
# the webpage of the Czech...... Output from this notebook is CSV file with downloaded data about........ that will be further processed, cleaned and aggregated.

# 
# os package is used only to check whether we are in the correct working directory.
# 
# In the def, we will be applying methods from requests (downloading site content), BeautifulSoup (machine reading of downloaded data), tqdm (interactive measurement of the downloading progress) and time (setting pause between requests from the site) packages.
# 
# After the data are downloaded we use pandas to pre-process and save them.

# After downloading the packages, I will check the data structure in order to make sure that we can scrape the given information 
# here below we used BeutfulSoup library to request the data.

# In[6]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from tqdm import tqdm
import re
import numpy as np
html_text = requests.get("https://testovani.uzis.cz/").text.strip()
soup = BeautifulSoup(html_text, 'lxml')
test_centeres = soup.find_all('div', class_="list__result")
header = soup.find('div', class_="list__headline").text.strip()
print(f" Header: {header}") 

for test_centere in test_centeres:
    company_name = test_centere.find('span', class_="list__col").text.replace('\n ', '')
    #callendar= test_centere.find('div', class_="main")#.text.replace('\n ', '')
    print(f" Company Name : {company_name.strip()}")
   
    print(' ')
    


# In[2]:


header = soup.find('div', class_="list__headline").text.strip()
header# in order to check how many free places are available


# Getting info about the website

# In[63]:


import pandas as pd # to be saved and aggreagated into datafame
import numpy as np


# In[11]:


def get_page_links(url):# Firstly created the function gets the data and returns the links of the each company 
    sleep(0.2) 
    base_url='https://testovani.uzis.cz/'
    r = requests.get(url)
    soup= BeautifulSoup(r.text,'lxml')
    links=soup.select('div.list__result a')
    return[ base_url + link.attrs['href'] for link in links] 
    
    
def test_locatio_detail(url): # Created the second function which grabs all necessary information form each comapny and returns
    r = requests.get(url)
    soup= BeautifulSoup(r.text,'lxml')
    company_details={
        'Name':soup.select_one('div.detail__main h1').text.strip().replace('\n',' '),
        'Adress':soup.select_one('div.info td:nth-child(2)').text.strip().replace('\n',''),
        'Upřesnění polohy':soup.select_one('div.info :nth-child(2) td:nth-child(2)').text.strip().replace('\n',''),
        'Telefon':soup.select_one('div.info a').text.strip().replace('\n',''),
        'Poznámka':soup.select_one('div.info :nth-child(4) td:nth-child(2)').text.strip().replace('\n',''),
        'Příjem':soup.select_one('div.info :nth-child(5) td:nth-child(2)').text.strip().replace('\n',''),
        'Cena za samoodběř':soup.select_one('div.info :nth-child(6) td:nth-child(2)').text.strip().replace('\n',''),
        'Způsob rezervace':soup.select_one('div.info :nth-child(7) td:nth-child(2)').text.strip().replace('\n',''),
        'Odkaz na rezervační systém':soup.select_one('div.info :nth-child(8) td:nth-child(2)').text.strip().replace('\n',''),
        'DRIVE-IN':soup.select_one('div.info :nth-child(9) td:nth-child(2)').text.strip().replace('\n',''),
        #'Av_days':pd.DataFrame([soup.select_one('div.opening').text.strip().replace('\n','')])
   
    }
    #print(company_details)    
    return company_details
#test_location_detail('https://testovani.uzis.cz//Detail?id=b84211a4-9c9e-4773-8439-71bb18fde2d4&backURL')    
    
    
#get_page_links("https://testovani.uzis.cz/")    

def main():# Created 3rd function which focuses on gattering all the information into one dictionary, to be saved in main function
   results=[]
   urls= get_page_links('https://testovani.uzis.cz/')
   comp_info=[test_locatio_detail(url) for url in urls]
   results.append(comp_info) #creating the data storage for further use, as we assume to use the callendar sting
   return results

print(main())


# In[10]:


def test_locatio_detail(url): # Created the second function which grabs all necessary information form each comapny and returns
    r = requests.get(url)
    soup= BeautifulSoup(r.text,'lxml')
    company_details={
        'Name':soup.select_one('div.detail__main h1').text.strip().replace('\n',' '),
        'Adress':soup.select_one('div.info td:nth-child(2)').text.strip().replace('\n',''),
        'Upřesnění polohy':soup.select_one('div.info :nth-child(2) td:nth-child(2)').text.strip().replace('\n',''),
        'Telefon':soup.select_one('div.info a').text.strip().replace('\n',''),
        'Poznámka':soup.select_one('div.info :nth-child(4) td:nth-child(2)').text.strip().replace('\n',''),
        'Příjem':soup.select_one('div.info :nth-child(5) td:nth-child(2)').text.strip().replace('\n',''),
        'Cena za samoodběř':soup.select_one('div.info :nth-child(6) td:nth-child(2)').text.strip().replace('\n',''),
        'Způsob rezervace':soup.select_one('div.info :nth-child(7) td:nth-child(2)').text.strip().replace('\n',''),
        'Odkaz na rezervační systém':soup.select_one('div.info :nth-child(8) td:nth-child(2)').text.strip().replace('\n',''),
        'DRIVE-IN':soup.select_one('div.info :nth-child(9) td:nth-child(2)').text.strip().replace('\n',''),
        #'Av_days':pd.DataFrame([soup.select_one('div.opening').text.strip().replace('\n','')])
   
    }
    #print(company_details)    
    return company_details
f=test_locatio_detail('https://testovani.uzis.cz//Detail?id=b84211a4-9c9e-4773-8439-71bb18fde2d4&backURL')
pd.DataFrame(f,index=['1',])


# Cleaned and used the previous main function to set structured data.

# In[125]:


def main():# Created 3rd function which focuses on gattering all the information into one dictionary, to be saved in main function
   #results=[]
   urls= get_page_links('https://testovani.uzis.cz/')
   comp_info=pd.DataFrame([test_locatio_detail(url) for url in urls])
   #results.append(comp_info)
   return comp_info

main()


# In[126]:


df=main()


# In[130]:


df.to_csv('Covid.csv')


# We will next load the data to our working directory to process the data clean and put it in commercially friendly way

# In[133]:


data = pd.read_csv('Covid.csv', index_col = 0)
data.head(10)


# I have tried to scrap the calendar, saved in csv file.

# In[68]:


def calnedar(url): # Created the second function which grabs all necessary information form each comapny and returns
    r = requests.get(url)
    soup= BeautifulSoup(r.text,'lxml')
    company_calendars={
        'Calendar':soup.select_one('div.slots__list').text.strip().replace('\n',' ')
    }
    
    return company_calendars
Ca=calnedar('https://testovani.uzis.cz/Detail?id=f4d02b50-1561-4c7e-9cf4-8d85b2d985ea&backURL=/')
Ca


# In[67]:


def all_clendarInfo():# Here I will source all available calendar info.
   #results=[]
   urls= get_page_links('https://testovani.uzis.cz/')
   calnedars=pd.DataFrame([calnedar(url) for url in urls])
   #results.append(comp_info)
   return calnedars

all_clendarInfo()


# In[38]:


cad_dataframe=all_clendarInfo()
cad_dataframe.to_csv('calendar.csv')


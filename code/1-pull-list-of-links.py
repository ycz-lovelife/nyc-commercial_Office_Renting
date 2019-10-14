
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[4]:


link_list = []
links = soup_page.find_all(class_='uniformRow listing-row grid-md grid-v-center pad-half-sm ')

for i in range(len(links)):
    link_list.append(links[i]['href'])

for i in link_list:
    print (i)
print('There are '+str(len(link_list)) +' total pages')


# In[39]:


import time, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#open page
chromedriver = "C:/Users/yichi/Desktop/Metis/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)
my_html_ny = 'https://42floors.com/for-lease/office-space/us/ny/new-york'
driver.get(my_html_ny)

time.sleep(2)

#grab web page html as text
page = requests.get(my_html_ny).content

'''
set BeautifulSoup to click next page and grab all page links until no next page tag available
'''
link_list = []
count = 0
previous_url = 0
next_url = my_html_ny 
continue_while_loop = True
while continue_while_loop:
    
    page = requests.get(next_url).content
    soup = BeautifulSoup(page,'lxml')
    
    #scrape page
    
    links = soup.find_all(class_='uniformRow listing-row grid-md grid-v-center pad-half-sm ')
    
    #append scraped scraped links to list
    for i in range(len(links)):
        link_list.append(links[i]['href'])
    
    try:
        nextpage_button = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div[3]/h4')
        nextpage_button.click()
    except:
        None
    count += 1
    
    
    previous_url = driver.current_url
    time.sleep(1)
    
    nextpage_button = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div[2]/div[2]/div/ul/li[2]')
    nextpage_button.click()
    
    next_url = driver.current_url
    if previous_url==next_url:
        continue_while_loop = False
        



# In[40]:


print(len(link_list))


# In[41]:


driver.close()


# In[43]:


os.getcwd()


# In[44]:


#store progress in pickle
import pickle

with open('pickle-files/link_list.pkl','wb') as picklefile:
    pickle.dump(link_list,picklefile)
#link_list is list or dictionary of values


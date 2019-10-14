import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

#load list of links in
import pickle

with open('pickle-files/link_list_1004.pkl', 'rb') as picklefile: 
    link_list = pickle.load(picklefile)

#check how many url lists are loaded
print(len(link_list))



def build_dict(test_soup):
    test = {}
    test['title'] = test_soup.find(class_='bold margin-none').text.strip()

    #square feet - num
    test['sqft'] = (test_soup.find('div',itemtype = 'http://schema.org/Offer')
                    .find(class_='listing-size col-5-sm col-3-md')
                    .text.strip().rstrip('sqft').rstrip()
                   )

    # location address - string
    test['address'] = test_soup.find(text=re.compile('NY')).strip()

    # floor level - num
    test['floor_level'] = test_soup.find(class_='listing-name col-6-sm col-3-md col-center').text.strip()


    f_xpath = test_soup.find(class_='features section')
    # building construction year - num
    if f_xpath.find(text=re.compile('Constructed')):
        test['construct_year'] = (f_xpath.find(text=re.compile('Constructed'))
                                  .parent.parent.find(class_='strong').text.strip()
                                 )
    else:
        test['construct_year'] = 'None'

    # building renovation year - num
    if f_xpath.find(text=re.compile('Renovated')):
        test['renovate_year'] = (f_xpath.find(text=re.compile('Renovated'))
                                 .parent.parent.find(class_='strong')
                                 .text.strip()
                                )
    else:
        test['renovate_year'] = 'None'

    # metro transition lines near the building - string
    if test_soup.find(class_='features section').find(text=re.compile('Public Transit')):
        test['public_transit'] = (test_soup.find(class_='features section')
                                  .find(text=re.compile('Public Transit'))
                                  .parent.parent.find(class_='strong')
                                  .text
                                  .strip()
                                 )
    else:
        test['public_transit'] = 'None'


    # building class - categorical
    if f_xpath.find(text=re.compile('Building')):
        test['building_class'] = (f_xpath.find(text=re.compile('Building'))
                                  .parent.parent.find(class_='strong')
                                  .text.strip()
                                 )
    else:
        test['building_class'] = 'None'

    #Common Kitchen
    if f_xpath.find(text=re.compile('Kitchen')):
        test['common_kitchen'] = '1'
    else:
        test['common_kitchen'] = '0'        

    #       Showers
    if f_xpath.find(text=re.compile('Showers')):
        test['showers'] = '1'
    else:
        test['showers'] = '0'

    #       Key Card Access
    if f_xpath.find(text=re.compile('Key Card Access')):
        test['key_card_access'] = '1'
    else:
        test['key_card_access'] = '0'

    #       On site Security
    if f_xpath.find(text=re.compile('Security')):
        test['on_site_security'] = '1'
    else:
        test['on_site_security'] = '0'


    #list posted date - datetime    
    post_xpath = test_soup.find(class_='listing-touched_at col-3-md hide-sm')
    if post_xpath:
        test['post_date'] = post_xpath.text.strip().split('\n')[0]
    else:
        test['post_date'] = 'None'


    features_xpath = test_soup.find('div',class_='features grid grid-top grid-nest margin-v')
    #lease term length - num
    if features_xpath.find(text=re.compile('Term')):
        test['term_length'] = (features_xpath.find(text=re.compile('Term'))
                               .parent.parent.find('span', class_='text-nowrap text-bold')
                               .text)
    else:
        test['term_length'] = 'None'

    #building construction type - 
    f_xpath = test_soup.find("div",class_="grid grid-nest grid-top")
    if f_xpath.find(text=re.compile('Construction Type')):
        test['construction_type'] = (f_xpath.find(text=re.compile('Construction Type'))
                                     .parent.parent.find('div',class_='strong')
                                     .text
                                     .strip())
    else:
        test['construction_type'] = 'None'


    #Amenities
    amenity_xpath = test_soup.find("div",class_="margin-v grid grid-top grid-nest")
    #Furniture
    if amenity_xpath:
        for i in amenity_xpath:
            if amenity_xpath.find(text=re.compile('Kitchen')):
                test['furniture'] = '1'
            else:
                test['furniture'] = '0'

            #Turnkey
            if amenity_xpath.find(text=re.compile('Turnkey')):
                test['turnkey'] = '1'
            else:
                test['turnkey'] = '0'

            #Natural Light
            if amenity_xpath.find(text=re.compile('Natural Light')):
                test['natural_light'] = '1'
            else:
                test['natural_light'] = '0'


            #High Ceilings
            if amenity_xpath.find(text=re.compile('High Ceilings')):
                test['high_ceilings'] = '1'
            else:
                test['high_ceilings'] = '0'

            #Plug and Play
            if amenity_xpath.find(text=re.compile('Plug')):
                test['plug_and_play'] = '1'
            else:
                test['plug_and_play'] = '0'


        #price rate
        rate_xpath = test_soup.find(class_='listing-rate col-2-md hide-sm ')
        if rate_xpath:
            test['rate_price'] = rate_xpath.text.strip().split('\n')[0]
            test['rate_term'] = rate_xpath.text.strip().split('\n')[1].strip().lstrip('/')
        else:
            test['rate_price'] = 'None'
            test['rate_term'] = 'None'
    return test




master_data_list = []
error_list = []
good_list = []
for url in link_list:
    test_url = 'https://42floors.com'+url
    test_page = requests.get(test_url).text
    test_soup = BeautifulSoup(test_page, "lxml")
    try:
        master_data_list.append(build_dict(test_soup))
        good_list.append(url)
    except:
        error_list.append(url)
        pass
    
    
print (len(master_data_list),len(error_list))





print(len(master_data_list))





#save data
with open('pickle-files/master_data_1007.pkl', 'wb') as picklefile: 
     pickle.dump(master_data_list,picklefile)




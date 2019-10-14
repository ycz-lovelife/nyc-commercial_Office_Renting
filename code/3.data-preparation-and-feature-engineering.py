import numpy as np
import pandas as pd
import pickle 

#load file from pickle
with open('pickle-files/master_data_1007.pkl', 'rb') as picklefile: 
    master_data_dict = pickle.load(picklefile)


#transform to dataframe
df = pd.DataFrame(master_data_dict)

#take out data without price rate and clean the column
df['rate_price'] = df['rate_price'].astype(object).str.replace('$',' ')
df['rate_price'] = df['rate_price'].str.strip()
df = df[df['rate_price'] != '—']
df['rate_price'] = df['rate_price'].str.replace(',','')
df['rate_price'] = df['rate_price'].astype(float)


#convert sqft to numbers
df['sqft'] = df['sqft'].str.replace(',','').astype(int)


#reset index after dropping all lists without price
df = df.reset_index(drop = True)

#standarizing Rate Price into sqft/month
xyz = []

for i in range(len(df['rate_price'])):
    if (df.loc[i, 'rate_term'] =='mo'):
        xyz.append(df.loc[i,'rate_price']/df.loc[i,'sqft'])
        df['rate_term'].iloc[i] = df['rate_term'].iloc[i].replace('mo','sqft/mo')
    elif (df.loc[i, 'rate_term'] =='sqft/yr'):
        xyz.append(df.loc[i,'rate_price']/12)
        df['rate_term'].iloc[i] = df['rate_term'].iloc[i].replace('sqft/yr','sqft/mo')
    elif (df.loc[i, 'rate_term'] =='yr'):
        xyz.append((df.loc[i,'rate_price']/12)/df.loc[i,'sqft'])
        df['rate_term'].iloc[i] = df['rate_term'].iloc[i].replace('yr','sqft/mo')
    else:
        xyz.append(df.loc[i, 'rate_price'])

df['rate_price'] = pd.Series(xyz)

#convert renovate_year column to binary -- 0 if 'None', 1 if with a year
df['renovate_year'] = np.where(df['renovate_year'] == 'None', 0, 1)
df = df.rename({'renovate_year': 'has_renovated'}, axis=1)
df['has_renovated'] = df['has_renovated'].astype('int')

#create new column nearby_public_transit to get how many subway lines are available near the leasing office area
df['nearby_public_transit'] = [len(i.split(',')) for i in df['public_transit']]


#transform amenity columns as categorical types
df['common_kitchen'] = df['common_kitchen'].astype('int')
df['showers'] = df['showers'].astype('int')
df['key_card_access'] = df['key_card_access'].astype('int')
df['on_site_security'] = df['on_site_security'].astype('int')
df['furniture'] = df['furniture'].astype('int')
df['turnkey'] = df['turnkey'].astype('int')
df['natural_light'] = df['natural_light'].astype('int')
df['high_ceilings'] = df['high_ceilings'].astype('int')
df['plug_and_play'] = df['plug_and_play'].astype('int')

#convert *construction_type* into dummies and append to df
ct = pd.get_dummies(df['construction_type'].str.split(', ').apply(pd.Series).stack()).sum(level=0)
ct = pd.DataFrame(ct)
df = df.join(ct)
df = pd.DataFrame(df)

#set data types of construction types as integer
df['Brick'] = df['Brick'].astype('int')
df['Concrete'] = df['Concrete'].astype('int')
df['Glass'] = df['Glass'].astype('int')
df['Masonry'] = df['Masonry'].astype('int')
df['None'] = df['None'].astype('int')
df['Steel'] = df['Steel'].astype('int')
df['Stone'] = df['Stone'].astype('int')
df['Tiltwall'] = df['Tiltwall'].astype('int')
df['Wood'] = df['Wood'].astype('int')

#transform all numbers to None for building_class
b = []

for i in range(len(df['building_class'])):
    if (df.loc[i, 'building_class'] =='1'):
        b.append('None')
    elif (df.loc[i, 'building_class'] =='2'):
        b.append('None')
    elif (df.loc[i, 'building_class'] =='5'):
        b.append('None')
    else:
        b.append(df.loc[i, 'building_class'])

df['building_class'] = pd.Series(b)

import datetime
#convert post_date column from 'MMM DD' format to datetime
df['post_date'] = pd.to_datetime(df['post_date'],format='%b %d')
df['post_date'] = df['post_date'] + pd.DateOffset(year = 2019)

#create column 'month' to get month name
df['month'] = df['post_date'].dt.month_name()

#create days from today column 
df['days_of_listing'] = (datetime.date.today() - (df['post_date']).dt.date).apply(lambda x: x.days)

#get district from address column and overwrite on address column
df['district'] = [i.split(',')[0] for i in df['address']]  


#fill None value with median of construction year
df['construct_year'] = df['construct_year'].replace('None', np.nan).astype(float)
df['construct_year'] = df['construct_year'].fillna(df['construct_year'].median())
df['construct_year'] = df['construct_year'].astype(int)

#remove white spaces from scraping
df['term_length'] = df['term_length'].str.strip()

#replace None value with numpy nan
df['term_length'] = df['term_length'].replace('None', np.nan)

#get dummy variables for building class and month
df = pd.get_dummies(data = df, columns = ['building_class','month','district','term_length'])

#drop unit price outliers
df = df.drop(df[df['rate_price'] > 30].index)

#save dataframe
with open('pickle-files/dataframe_1008.pkl', 'wb') as picklefile: 
     pickle.dump(df,picklefile)


# ### Cleaning Works Left to Do
# 1. clean *floor_level* data and transform to categorical dummy

df[['title','sqft','address','floor_level']].head(10)

df['floor_level'].str.split()


test_list = []
errors = []
for i in df['floor_level'].str.split():
    if len(i) > 1:
        try:
            test_list.append(int(i[1]))
        except:
            errors.append(i)
    else:
        errors.append(i)
        pass


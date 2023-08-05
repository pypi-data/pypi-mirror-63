"""
data_prep.py - Extract data from date range and create models
Usage:
    data_prep.py [options]
    data_prep.py -h | --help

Options:
    -h --help             Show this message.
    --output_folder=OUT   Output folder for the data and reports to be saved.
    --country=CNT         Arg for filtering by a specific country
"""
from __future__ import print_function
import pandas as pd
import numpy as np
import re
import os
import docopt
import sys
import pickle
import os.path
from datetime import datetime, date, time 
from dateutil.parser import parse
from time import strftime
import pyarrow
import json
import git
from difflib import get_close_matches
from tqdm import tqdm
from covidify.config import REPO, TMP_FOLDER, TMP_GIT, DATA

args = docopt.docopt(__doc__)
out = args['--output_folder']
country = args['--country']

if country == 'Global':
    country = None

def clean_sheet_names(new_ranges):
    indices = []    
    # Remove all sheets that dont have a numeric header
    numeric_sheets = [x for x in new_ranges if re.search(r'\d', x)]
    
    return numeric_sheets

def clone_repo(TMP_FOLDER, REPO):
    print('Cloning Data Repo...')
    git.Git(TMP_FOLDER).clone(REPO)

# Create Tmp Folder
if not os.path.isdir(TMP_FOLDER):
    print('Creating folder...')
    print('...', TMP_FOLDER)
    os.mkdir(TMP_FOLDER)

#Check if repo exists
#git pull if it does
if not os.path.isdir(TMP_GIT):
    clone_repo(TMP_FOLDER, REPO)
else:
    try:
        print('git pull from', REPO)
        rep = git.Repo(TMP_GIT)
        rep.remotes.origin.pull()
    except:
        print('Could not pull from', REPO)
        sys.exit()
    
sheets = os.listdir(DATA)

# Clean the result to the sheet tabs we want
print('Getting sheets...')
cleaned_sheets = clean_sheet_names(sheets)


def clean_last_updated(last_update):
    '''
    convert date and time in YYYYMMDD HMS format
    '''
    date = parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")
    time = parse(str(last_update).split(' ')[1]).strftime('%H:%M:%S')
    parsed_date = str(date) + ' ' + str(time)

    return parsed_date

def get_date(last_update):
    return parse(str(last_update).split(' ')[0]).strftime("%Y-%m-%d")

def get_csv_date(file):
    return get_date(file.split('.')[0] + ' ')    

def drop_duplicates(df_raw):
    '''
    Take the max date value for each province for a given date
    '''
    days_list = []
    
    for datetime in df_raw.date.unique():
        tmp_df = df_raw[df_raw.date == datetime]
        tmp_df = tmp_df.sort_values(['Last Update']).drop_duplicates('Province/State', keep='last')
        days_list.append(tmp_df)

    return days_list


keep_cols = ['Confirmed', 'Country/Region', 'Deaths', 'Last Update', 'Province/State', 'Recovered']
numeric_cols = ['Confirmed', 'Deaths', 'Recovered']

def get_data(cleaned_sheets):
    all_csv = []
    # Import all CSV's
    for file in tqdm(sorted(sheets), desc='... importing data: '):
        if 'csv' in file:
            # print('...', file)
            tmp_df = pd.read_csv(os.path.join(DATA, file), index_col=None, header=0, parse_dates=['Last Update'])
            tmp_df = tmp_df[keep_cols]
            tmp_df[numeric_cols] = tmp_df[numeric_cols].fillna(0)
            tmp_df[numeric_cols] = tmp_df[numeric_cols].astype(int)
            tmp_df['Province/State'].fillna(tmp_df['Country/Region'], inplace=True) #If no region given, fill it with country

            tmp_df['Last Update'] = tmp_df['Last Update'].apply(clean_last_updated)
            tmp_df['date'] = tmp_df['Last Update'].apply(get_date)
            tmp_df['file_date'] = get_csv_date(file)
            all_csv.append(tmp_df)

    # concatenate all csv's into one df
    df_raw = pd.concat(all_csv, axis=0, ignore_index=True, sort=True)
    df_raw = df_raw.sort_values(by=['Last Update'])

    frames = drop_duplicates(df_raw)
    tmp = pd.concat(frames, axis=0, ignore_index=True, sort=True)
    
    return tmp


df = get_data(cleaned_sheets)

# Now that we have all the data we now need to clean it 
# - Fill null values
# - remore suspected values
# - change column names
def clean_data(tmp_df):
    if 'Demised' in tmp_df.columns:
        tmp_df.rename(columns={'Demised':'Deaths'}, inplace=True)

    if 'Country/Region' in tmp_df.columns:
        tmp_df.rename(columns={'Country/Region':'country'}, inplace=True)
    
    if 'Province/State' in tmp_df.columns:
        tmp_df.rename(columns={'Province/State':'province'}, inplace=True)
        
    if 'Last Update' in tmp_df.columns:
        tmp_df.rename(columns={'Last Update':'datetime'}, inplace=True)
        
    if 'Suspected' in tmp_df.columns:
        tmp_df = tmp_df.drop(columns='Suspected')

    for col in tmp_df.columns:
        tmp_df[col] = tmp_df[col].fillna(0)
    
    #Lower case all col names
    tmp_df.columns = map(str.lower, tmp_df.columns) 
    return tmp_df

df  = clean_data(df)


def get_similar_countries(c, country_list):
    pos_countries = get_close_matches(c, country_list)
    
    if len(pos_countries) > 0:
        print('\033[1;31m'+c, 'was not listed. did you mean', pos_countries[0].capitalize() + '?\033[0;0m')
        sys.exit(1)
    else:
        print('\033[1;31m'+c, 'was not listed.\033[0;0m')
        sys.exit(1)
        
def check_specified_country(df, country):
    '''
    let user filter reports by country, if not found
    then give a option if the string is similar
    '''
    
    # Get all unique countries in the data
    country_list = list(map(lambda x:x.lower().strip(), set(df.country.values)))

    if country:
        print('Country specified')
        if country.lower() == 'china': #Mainland china china dont come up as similar
            print(country, 'was not listed. did you mean Mainland China?')
            sys.exit(1)

        # give similar option if similarity found
        elif country.lower() not in country_list:
            get_similar_countries(country, country_list)
            
        else:
            #Return filtered dataframe
            print('... filtering data for', country)
            if len(country) == 2:
                df = df[df.country == country.upper()]
            else:
                df = df[df.country == country.capitalize()]
            return df
    else:
        print('No specific country specified')
        return df


df = check_specified_country(df, country)

# sheets need to be sorted by date value
print('Sorting by datetime...')
current_date = str(datetime.date(datetime.now()))

if df.date.max() == current_date:
    df = df[df.date != df.date.max()]
else:
    df = df[df.date != current_date]

df = df.sort_values('datetime')

'''
Get the difference of the sum totals for each
date and plot them on a trendline graph
'''
def get_new_cases(tmp, col):
    diff_list = []
    tmp_df_list = []
    df = tmp.copy()

    for i, day in enumerate(df.sort_values('date').date.unique()):    
        tmp_df = df[df.date == day]
        tmp_df_list.append(tmp_df[col].sum())
        
        if i == 0:
            diff_list.append(tmp_df[col].sum())
        else:
            diff_list.append(tmp_df[col].sum() - tmp_df_list[i-1])
        
    return diff_list

def get_moving_average(tmp, col):
    df = tmp.copy()
    return df[col].rolling(window=2).mean()

def get_exp_moving_average(tmp, col):
    df = tmp.copy()
    return df[col].ewm(span=2, adjust=True).mean()


print('Calculating dataframe for new cases...')
daily_cases_df = pd.DataFrame([])
daily_cases_df['new_confirmed_cases'] = get_new_cases(df, 'confirmed')
daily_cases_df['new_deaths'] = get_new_cases(df, 'deaths')
daily_cases_df['new_recoveries'] = get_new_cases(df, 'recovered')
daily_cases_df['date'] = df.date.unique()

#Moving average
daily_cases_df['confirmed_MA'] = get_moving_average(daily_cases_df, 'new_confirmed_cases')
daily_cases_df['deaths_MA'] = get_moving_average(daily_cases_df, 'new_deaths')
daily_cases_df['recovered_MA'] = get_moving_average(daily_cases_df, 'new_recoveries')

#Exponential moving average
daily_cases_df['confirmed_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_confirmed_cases')
daily_cases_df['deaths_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_deaths')
daily_cases_df['recovered_exp_MA'] = get_exp_moving_average(daily_cases_df, 'new_recoveries')


'''
Calculate the number of people that are ACTUALLY infected on a given day
currently infected = sum of people date - (recovored + died)
ex: 5 = 10 - (4 - 1)

'''
current_infected = pd.DataFrame([])
current_infected['currently_infected'] = (df.groupby('date').confirmed.sum() - \
                                          (df.groupby('date').deaths.sum() + df.groupby('date').recovered.sum()))
current_infected['delta'] = (current_infected['currently_infected'] - df.groupby('date').confirmed.sum())
daily_cases_df = pd.merge(daily_cases_df, current_infected, how='outer', on='date')


#Create date of extraction folder
data_folder = os.path.join('data', str(datetime.date(datetime.now())))
save_dir = os.path.join(out, data_folder)

if not os.path.exists(save_dir):
    os.system('mkdir -p ' + save_dir)

print('Creating subdirectory for data...')
print('...', save_dir)

print('Saving...')
file_name = 'agg_data_{}.parquet.gzip'.format(datetime.date(datetime.now()))
df.astype(str).to_parquet(os.path.join(save_dir, file_name), compression='gzip')
print('...', file_name)


csv_file_name = 'agg_data_{}.csv'.format(datetime.date(datetime.now()))
df.astype(str).to_csv(os.path.join(save_dir, csv_file_name))
print('...', csv_file_name)


daily_cases_file_name = 'trend_{}.csv'.format(datetime.date(datetime.now()))
daily_cases_df.astype(str).to_csv(os.path.join(save_dir, daily_cases_file_name))
print('...', daily_cases_file_name)

print('Done!')
# Import all necessary packages
import numpy as np
import pandas as pd

# APIs
from dstapi import DstApi

# plotting
import matplotlib.pyplot as plt
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
plt.rcParams.update({'axes.grid':True,'grid.color':'black','grid.alpha':'0.25','grid.linestyle':'--'})
plt.rcParams.update({'font.size': 14})

# Create a function to load IFOR41.
def load_IFOR41(ULLIG,KOMMUNEDK,varname):

    params = {
        'table': 'IFOR41',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'ULLIG', 'values': [ULLIG]},
            {'code': 'KOMMUNEDK', 'values': [KOMMUNEDK]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }    

    # b. download
    df = DstApi('IFOR41').get_data(params=params)

    # c. set types and rename
    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.drop(columns=['ULLIG'])
    df = df.rename(columns={'INDHOLD': varname, 'KOMMUNEDK': 'municipality', 'TID': 'year'})

    # e. sorts
    df = df.sort_values(by=['municipality'])
    
    return df

# Create a function to load IFOR32.
def load_IFOR32(DECILGEN,KOMMUNEDK,varname):

    params = {
        'table': 'IFOR32',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'DECILGEN', 'values': [DECILGEN]},
            {'code': 'KOMMUNEDK', 'values': [KOMMUNEDK]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }

    dict_deci = {row['id']: row['text'] for i,row in DstApi('IFOR32').variable_levels('DECILGEN',language='en').iterrows()}

    # b. download
    df = DstApi('IFOR32').get_data(params=params)

    # c. set types and rename
    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.rename(columns={'INDHOLD': varname, 'KOMMUNEDK': 'municipality', 'TID': 'year'})
    

    # d. clean data
    df['DECILGEN'] = df.DECILGEN.replace(
        {dict_deci['1DC']: '1',
        dict_deci['2DC']: '2',
        dict_deci['3DC']: '3',
        dict_deci['4DC']: '4',
        dict_deci['5DC']: '5',
        dict_deci['6DC']: '6',
        dict_deci['7DC']: '7',
        dict_deci['8DC']: '8',
        dict_deci['9DC']: '9',
        dict_deci['10DC']: '10'
        })

    df = df.pivot_table(index=['year', 'municipality'], columns='DECILGEN', values=varname)
    df.columns = [f'{varname}_{c}' for c in df.columns]

    # e. calculate total and top 10% share
    df[f'{varname}_total'] = df.sum(axis=1)
    df[f'{varname}_top10_share'] = df[f'{varname}_10'] / df[f'{varname}_total']


    # f. reset index and sorts
    df = df.reset_index().sort_values(by=['municipality'])

    return df

# Create a function to load NGLK.
def load_NGLK(OMRÅDE, BNØGLE, BRUTNETUDG, PRISENHED, varname):

    params = {
        'table': 'NGLK',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'OMRÅDE', 'values': [OMRÅDE]},
            {'code': 'BNØGLE', 'values': [BNØGLE]},
            {'code': 'BRUTNETUDG', 'values': [BRUTNETUDG]},
            {'code': 'PRISENHED', 'values': [PRISENHED]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }    

    # b. download
    df = DstApi('NGLK').get_data(params=params)

    # c. set types and rename
    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.drop(columns=['BNØGLE', 'BRUTNETUDG', 'PRISENHED'])
    df = df.rename(columns={'INDHOLD': varname, 'OMRÅDE': 'municipality', 'TID': 'year'})

    # e. sorts
    df = df.sort_values(by=['municipality'])
    
    return df

# Create a function to load FOD407.
def load_FOD407(OMRÅDE, ALDER, varname):

    params = {
        'table': 'FOD407',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'OMRÅDE', 'values': [OMRÅDE]},
            {'code': 'ALDER', 'values': [ALDER]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }    

    # b. download
    df = DstApi('FOD407').get_data(params=params)

    # c. set types and rename
    df['INDHOLD'] = pd.to_numeric(df['INDHOLD'], errors='coerce')
    df = df.dropna(subset=['INDHOLD'])

    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.drop(columns=['ALDER'])
    df = df.rename(columns={'INDHOLD': varname, 'OMRÅDE': 'municipality', 'TID': 'year'})

    # e. sorts
    df = df.sort_values(by=['municipality'])
    
    return df

# Create a function to load STRAFNA7.
def load_STRAFNA7(OMRÅDE, OVERTRÆD, varname):

    params = {
        'table': 'STRAFNA7',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'OMRÅDE', 'values': [OMRÅDE]},
            {'code': 'OVERTRÆD', 'values': [OVERTRÆD]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }    

    # b. download
    df = DstApi('STRAFNA7').get_data(params=params)

    # c. set types and rename
    df['INDHOLD'] = pd.to_numeric(df['INDHOLD'], errors='coerce')
    df = df.dropna(subset=['INDHOLD'])

    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.drop(columns=['OVERTRÆD'])
    df = df.rename(columns={'INDHOLD': varname, 'OMRÅDE': 'municipality', 'TID': 'year'})

    # e. sorts
    df = df.sort_values(by=['municipality'])
    
    return df

# Create a function to load BEFOLK3.
def load_BEFOLK3(OMRÅDE, KØN, ALDER, varname):

    params = {
        'table': 'BEFOLK3',
        'format': 'BULK', # semicolon separated file
        'lang': 'en',
        'variables': [
            {'code': 'OMRÅDE', 'values': [OMRÅDE]},
            {'code': 'KØN', 'values': [KØN]},
            {'code': 'ALDER', 'values': [ALDER]},
            {'code': 'Tid', 'values': ['*']},
            ]
    }    

    # b. download
    df = DstApi('BEFOLK3').get_data(params=params)

    # c. set types and rename
    df['TID'] = df['TID'].astype(int)
    df['INDHOLD'] = df['INDHOLD'].astype(float)
    df = df.drop(columns=['KØN', 'ALDER'])
    df = df.rename(columns={'INDHOLD': varname, 'OMRÅDE': 'municipality', 'TID': 'year'})

    # e. sorts
    df = df.sort_values(by=['municipality'])
    
    return df
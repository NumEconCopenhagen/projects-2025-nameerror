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

################################ Exercise 1 data on inequality ################################

# Create a function to load IFOR41.
def load_IFOR41(ULLIG,KOMMUNEDK,varname):
    """
    Load and clean data from Statistics Denmark's IFOR41 table for the given
    unemployment insurance status (ULLIG) and municipalities (KOMMUNEDK).

    Returns a DataFrame with columns ['municipality', 'year', varname].
    """
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
    """
    Load and clean data from Statistics Denmark's IFOR32 table for the given
    income deciles (DECILGEN) and municipalities (KOMMUNEDK), pivoting deciles
    into separate columns and adding total income and top-10% income share.

    Returns a DataFrame with columns ['year', 'municipality', varname_1..varname_10,
    varname_total', varname_top10_share'].
    """
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
    """
    Load and clean data from Statistics Denmark's NGLK table for the given
    area (OMRÅDE), budget key (BNØGLE), expenditure type (BRUTNETUDG) and
    price unit (PRISENHED).

    Returns a DataFrame with columns ['municipality', 'year', varname].
    """
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
    """
    Load and clean data from Statistics Denmark's FOD407 table for the given
    area (OMRÅDE) and age group (ALDER), dropping rows with non-numeric values.

    Returns a DataFrame with columns ['municipality', 'year', varname].
    """
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
    """
    Load and clean data from Statistics Denmark's STRAFNA7 table for the given
    area (OMRÅDE) and type of offense (OVERTRÆD), dropping rows with non-numeric values.

    Returns a DataFrame with columns ['municipality', 'year', varname].
    """
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
    """
    Load and clean data from Statistics Denmark's BEFOLK3 table for the given
    area (OMRÅDE), gender (KØN) and age group (ALDER).

    Returns a DataFrame with columns ['municipality', 'year', varname].
    """
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


################################ Exercise 2 Model simulation ################################


# Create a function to simulate the model.
def simulate(seed=2025, N=50000,
    edu_prob = np.array([0.4, 0.35, 0.25]),
    edu_years = np.array([1, 3, 5]),
    ini_hum_cap = np.array([1, 1.2, 1.55]),
    gro_hum_cap = np.array([0.01, 0.02, 0.03]),
    depreciation = 0.06,
    std_of_shock = 0.1,
    job_fin_prob = 0.6,
    job_sep_prob = 0.05,
    stu_gra = 0.45,
    repl_rate = 0.6,
    ben_floor = 0.35):

    """
    Simulate a life-cycle model of education, employment and income for a panel of individuals.

    Each of the N individuals is randomly assigned one of three education levels (0, 1, 2),
    which determines how many periods they spend in education and the initial level and
    growth rate of their human capital. After finishing education, individuals transition
    stochastically between employment and unemployment each period, and their human capital
    grows (while employed) or depreciates (while unemployed), subject to a log-normal shock.
    Income is derived from human capital while employed, from a fixed grant while in
    education, and from a fraction of last job income (subject to a floor) while unemployed.

    Parameters
    ----------
    seed : int
        Seed for the random number generator, ensuring reproducible simulations.
    N : int
        Number of individuals to simulate.
    edu_prob : np.ndarray, shape (3,)
        Probability of being assigned each of the three education levels.
    edu_years : np.ndarray, shape (3,)
        Number of periods spent in education for each education level.
    ini_hum_cap : np.ndarray, shape (3,)
        Initial human capital level upon finishing education, for each education level.
    gro_hum_cap : np.ndarray, shape (3,)
        Per-period growth rate of human capital while employed, for each education level.
    depreciation : float
        Per-period depreciation rate of human capital while not employed.
    std_of_shock : float
        Standard deviation of the log-normal shock applied to human capital each period.
    job_fin_prob : float
        Probability that an unemployed (non-student) individual finds a job in a given period.
    job_sep_prob : float
        Probability that an employed individual loses their job in a given period.
    stu_gra : float
        Income (student grant) received while in education.
    repl_rate : float
        Replacement rate applied to an individual's last job income while unemployed.
    ben_floor : float
        Minimum income floor applied in every period, regardless of employment status.

    Returns
    -------
    dict
        Dictionary with the following keys:

        - "ages" : np.ndarray, shape (T,) - Ages simulated (18 to 65).
        - "income" : np.ndarray, shape (T, N) - Income of each individual in each period.
        - "employed" : np.ndarray, shape (T, N) - Employment status of each individual in each period.
        - "h" : np.ndarray, shape (T, N) - Human capital of each individual in each period.
        - "educ" : np.ndarray, shape (N,) - Education level (0, 1, or 2) of each individual.
    """
    #a. Creates objects for later use
    rng = np.random.default_rng(seed)
    ages = np.arange(18, 66) 
    T = len(ages)

    # b. Simulate education levels for each individual

    # b.i Set intial education and human capital levels
    educ = rng.choice(3, size=N, p=edu_prob) # Each individual is assigned an education level (0, 1, or 2).
    
    S_i = edu_years[educ] 
    h0_i = ini_hum_cap[educ]
    Delta_i = gro_hum_cap[educ]

    # b.ii Initialize arrays to store simulation results
    income = np.full((T, N), np.nan)
    employed = np.zeros((T, N), dtype=bool)
    h = np.zeros((T, N))
    last_job_income = np.full(N, ben_floor)
    ever_employed = np.zeros(N, dtype=bool)

    # c. simulate the model over T periods
    for t in range(T):
        in_education = t < S_i

        # c.i Employment status
        if t == 0:
            employed[t] = False # initially, all individuals are students
        else:
            was_employed = employed[t - 1]
            newly_employed = (~was_employed) & (rng.random(N) < job_fin_prob)
            newly_unemployed = was_employed & (rng.random(N) < job_sep_prob)

            employed[t] = (was_employed & ~newly_unemployed) | newly_employed

        employed[t] = employed[t] & ~in_education # Students are unemployed

        # c.ii Human capital evolution
        psi = rng.lognormal(-0.5 * std_of_shock**2, std_of_shock, size=N) # Creates human capital shocks

        if t > 0: # Updates human capital for people in the work force and keeps it constant for students
            h_prev = h[t - 1]
            h_new = np.where(
                employed[t],
                h_prev * (1 + Delta_i) * psi,
                h_prev * (1 - depreciation) * psi,
            )
            
            h[t] = np.where(in_education, h_prev, h_new)
        else:
            h[t] = h0_i  

        
        just_finished = (t > 0) & (S_i == t)
        h[t] = np.where(just_finished, h0_i, h[t])

        # c.iii Income evolution
        income[t] = np.where(
            in_education,
            stu_gra,
            np.where(employed[t], h[t], repl_rate * last_job_income),
        )

        income[t] = np.maximum(income[t], ben_floor)  # No one can earn less than the benefit floor

        last_job_income = np.where(employed[t], income[t], last_job_income)

        ever_employed = ever_employed | employed[t]

    return {
        "ages": ages,
        "income": income,
        "employed": employed,
        "h": h,
        "educ": educ,
    }
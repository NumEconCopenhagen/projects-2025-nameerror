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

    rng = np.random.default_rng(seed) # sætter generator op. bruges senere til .choice, .random og .lognormal
    ages = np.arange(18, 66) # danner en array m. tallene 18, 19, ..., 64, 65. (66 kommer ikke med)
    T = len(ages) # parameterværdi som får værdien 66-18 = 48, altså det samlede antal perioder

    # uddannelseslængde per individ: 0=kort, 1=mellem, 2=lang
    educ = rng.choice(3, size=N, p=edu_prob) # simulerer N gange et udtræk via rng. Udtrækket er et tal af tre muligheder (0,1,2) ud fra de tilh. ssh. fra edu_prob. Dette er lodtrækning af education.
    # muligt problem med educ. Et tal per år i dataframe "out". Bør der ikke være en array med 50k tal i t = 0 (eller bare alle rows) som angiver hvilken udd hvert individ har?

    # slå individspecifikke parametre op via educ
    S_i = edu_years[educ] # array der for hvert id angiver edu_years ud fra deres educ.
    h0_i = ini_hum_cap[educ] # array der tilsv. angiver hver individs initiale human capital ud fra deres educ.
    Delta_i = gro_hum_cap[educ] # tilsvarende hvert individs vækstrate i human capital ud fra educ.

    income = np.full((T, N), np.nan) # danner en tom array med dimensionerne T x N (48 x 50k) med værdierne NaN, som bliver overwritten i takt med at hvert år simuleres
    employed = np.zeros((T, N), dtype=bool) # tilsvarende for employment status (en boolean var) som, som udgangspunkt har værdien False over det hele
    h = np.zeros((T, N)) # tilsvarende for human capital level der som udgangspunkt sættes til 0
    last_job_income = np.full(N, ben_floor)  # tom array som skal bruges til at angive individers forrige løn. Den sættes som udgangspunkt til benefit floor, fordi den senere skal bruges til at angive individers indkomst når de er arbejdsløse.
    ever_employed = np.zeros(N, dtype=bool) # tom boolean array som skal bruges til at angive om individer nogensinde har været employed

    for t in range(T): # hovedloopet for funktionen der kører for hver af de 48 perioder
        in_education = t < S_i # angiver først om et individ statig er under udd (hvis udd-længde er længere end antal perioder der er simuleret)

        # --- Beskæftigelsesstatus (Markovkæde) ---
        if t == 0: # dvs. i første periode (alder 18)
            # Første periode starter som ledig (uden for uddannelse håndteres nedenfor)
            employed[t] = False # række t=0 af array employed indtastes False for alle fordi ingen som udgangspunkt har job fordi alle uddannelser tager min. et år
        else: # for perioder der ikke er den første
            was_employed = employed[t - 1] # angiver om en person var employed i sidste periode ud fra forrige værdi af employed-array
            newly_employed = (~was_employed) & (rng.random(N) < job_fin_prob) # hvis individ IKKE var employed i forrige periode OG et tilfældigt tal der trækkes mellem 0 og 1 er lavere end job finding prob., så er personen kommet i job.
            # det er en metode der bruges til at realisere om en person kommer i arbejde, altså at trække et tilfældigt tal mellem 0 og 1 og sammenholde det med en grænse.
            newly_unemployed = was_employed & (rng.random(N) < job_sep_prob) # tilsvarende for de hvor was_employed = True, trækkes et tal mellem 0 og 1 og sammenholdes med job_separation rate. 
            employed[t] = (was_employed & ~newly_unemployed) | newly_employed # employment status for række t i array'en opdateres med første part (om person var i arbejde og har False på "blev arbejdsløs") eller anden part (om person er blev nyligt ansat).
            #For en employed person vil en af disse være True og for en unemployed person vil begge disse være False, så employed[t] bliver True kun for de der er i arbejde.

        # Uden for arbejdsmarked hvis stadig i uddannelse
        employed[t] = employed[t] & ~in_education # for personer der er i uddannelse i periode t (anden del betyder "in_education = False) vil employed[t] overwrites med False.

        # --- Humankapital ---
        psi = rng.lognormal(-0.5 * std_of_shock**2, std_of_shock, size=N) # simulerer chokket for hvert individ (kode fra opgavebeskrivelse)

        if t > 0: # for perioder der ikke er den første periode
            h_prev = h[t - 1] # angiver forrige periodes human capital (vil være 0 for periode t = 1)
            h_new = np.where( # angiver opdateret human capital
                employed[t], # hvis employed i periode t er sandt (minder lidt om et if-statement i excel), så:
                h_prev * (1 + Delta_i) * psi, # ...skal h_new være den gamle, plus væksten og chokkets indflydelse som angivet i opgaven
                h_prev * (1 - depreciation) * psi, # ...hvis ikke personen var employed, skal h_new være den gamle, minus indflydelsen fra depreciation og chokket.
            )
            # kun opdatér for dem der ikke er i uddannelse
            h[t] = np.where(in_education, h_prev, h_new) # tilsvarende if-statement: hvis in_education = true, skal h[t] bare være lig med h_prev. Hvis den var false, skal den opdateres til h_new
        else:
            h[t] = h0_i  # ved simuleringens start (dvs. periode t = 0) skal h[t] sættes til den initiale niveau givet ved uddannelsens type.

        # fanger overgangen: individer der lige er færdige med uddannelsen
        # denne periode skal starte med deres uddannelsesspecifikke humankapital
        just_finished = (t > 0) & (S_i == t) # altså for de hvor uddannelseslængden er lig antallet af perioder simuleret
        h[t] = np.where(just_finished, h0_i, h[t]) # ...skal h[t] opdateres til det initiale niveau angivet af uddannelsens type (men er den ikke det i forvejen grundet if/else-statementet lige ovenfor?)

        # --- Indkomst ---
        income[t] = np.where( # income-array'en (fyldt med NaN'er) skal have række t erstattet med student grant for de der har in_education = True. 
            in_education,
            stu_gra,
            np.where(employed[t], h[t], repl_rate * last_job_income), # For de der ikke har in_education = True, skal (nyt if-statement) de have income = human capital, HVIS de har employed[t] = True. Hvis de har employed = False skal de have replacement rate x deres gamle løn.
        )
        income[t] = np.maximum(income[t], ben_floor)  # for de hvis indkomst er faldet under benefit floor grundet replacement rate, får de i stedet benefit floor.
        #Tjek lige om replacement rate ganges på for hver periode uden job, for det virker til at den bare skal gange på seneste løn under job og så forblive dette indtil man få job igen.

        # Opdatér "sidste jobs indkomst" og ever_employed for dem i beskæftigelse
        last_job_income = np.where(employed[t], h[t], last_job_income) # opdaterer række t i last_job_income til at være h[t] for de ansatte og last_job_income for de andre.
        #Dette er vel så egentlig beviset for at ovenstående bekymring vedr. påganget replacement rate, ikke er en realitet, fordi at last_job_income ikke faldet, bare fordi man har været arbejdsløs en periode
        ever_employed = ever_employed | employed[t] # ever employed indikatoren opdateres. True hvis ever_employed i forvejen var true eller hvis employed i periode t er true. False hvis begge er false.

    return {
        "ages": ages,
        "income": income,       # (T, N) array
        "employed": employed,
        "h": h,
        "educ": educ,
    }
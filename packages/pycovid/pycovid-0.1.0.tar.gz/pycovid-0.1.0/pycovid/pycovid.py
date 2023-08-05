import pandas as pd
import numpy as np
import plotly.express as px

def getCovidCases(countries=None, start_date=None, end_date=None, casetype=['confirmed', 'death', 'recovered']):
    df = pd.read_csv('https://raw.githubusercontent.com/RamiKrispin/coronavirus-csv/master/coronavirus_dataset.csv',
            names=["province_state", 'country_region', 'lat', 'long', 'date', 'cases', 'type'], skiprows=1, parse_dates=['date'])
    
    df = df[df.type.isin(casetype)]
    
    if start_date is not None:
        df = df[df.date >= start_date]
    if end_date is not None:
        df = df[df.date <= end_date]
            
    if countries is not None:
        for country in countries:
            if country not in df.country_region.values:
                print("Country: {0} not found in database. Check spelling!".format(country))
            df =  df[(df.country_region.isin(countries))]
            
    iso_df = pd.read_csv('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.csv')
    iso_df = iso_df[['name', 'alpha-3']]
    iso_df.loc[iso_df.name=="United States of America", 'name'] = 'US'
    iso_df.loc[iso_df.name=="China", 'name'] = 'Mainland China'
    iso_df.loc[iso_df.name=="United Kingdom", 'name'] = 'UK'
    iso_df.loc[iso_df.name=="Russian Federation", 'name'] = 'Russia'
    iso_df.loc[iso_df.name=="Korea, Republic of", 'name'] = 'South Korea'
    iso_df.loc[iso_df.name=="Macao", 'name'] = 'Macau'
    iso_df.loc[iso_df.name=="Taiwan, Province of China", 'name'] = 'Taiwan'
    iso_df.loc[iso_df.name=="Viet Nam", 'name'] = 'Vietnam'
    iso_df.loc[iso_df.name=="Iran (Islamic Republic of)", 'name'] = 'Iran'
    iso_df.loc[iso_df.name=="Czechia", 'name'] = 'Czech Republic'
    iso_df.loc[iso_df.name=="Saint Barthélemy", 'name'] = 'Saint Barthelemy'
    iso_df.loc[iso_df.name=="Palestine, State of", 'name'] = 'Palestine'
    iso_df.loc[iso_df.name=="Moldova, Republic of", 'name'] = 'Moldova'
    iso_df.loc[iso_df.name=="Ireland", 'name'] = 'Republic of Ireland'
    iso_df.loc[iso_df.name=="Holy See", 'name'] = 'Vatican City'
               
    df = pd.merge(df, iso_df, left_on="country_region", right_on='name')
    
    return df

def getCovidCasesWide(countries=None, start_date=None, end_date=None, casetype=['confirmed', 'death', 'recovered'], cumsum=False):
    df = pd.read_csv('https://raw.githubusercontent.com/RamiKrispin/coronavirus-csv/master/coronavirus_dataset.csv',
            names=["province_state", 'country_region', 'lat', 'long', 'date', 'cases', 'type'], skiprows=1, parse_dates=['date'])
    
    df = df[df.type.isin(casetype)]
    
    if start_date is not None:
        df = df[df.date >= start_date]
    else:
        if end_date is not None:
            df = df[df.date <= end_date]
            
    if countries is not None:
        for country in countries:
            if country not in df.country_region.values:
                print("Country: {0} not found in database. Check spelling!".format(country))
            df =  df[(df.country_region.isin(countries))]
    
    df = df.pivot_table(index=["date", 'country_region'], columns='type', values='cases', \
                        aggfunc={'date':'first', 'country_region':'first', 'cases':np.sum})\
            .reset_index().fillna(0)
    
    if 'death' not in df.columns:
        df['death'] = 0
    
    if 'recovered' not in df.columns:
        df['recovered'] = 0
        
    df.sort_values(by=['country_region', 'date'], inplace=True)
    
    if cumsum is True:
        df.confirmed = df.groupby('country_region')['confirmed'].transform(pd.Series.cumsum)
        df.recovered = df.groupby('country_region')['recovered'].transform(pd.Series.cumsum)
        df.death = df.groupby('country_region')['death'].transform(pd.Series.cumsum)
        
        

    iso_df = pd.read_csv('https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/slim-3/slim-3.csv')
    iso_df = iso_df[['name', 'alpha-3']]
    iso_df.loc[iso_df.name=="United States of America", 'name'] = 'US'
    iso_df.loc[iso_df.name=="China", 'name'] = 'Mainland China'
    iso_df.loc[iso_df.name=="United Kingdom", 'name'] = 'UK'
    iso_df.loc[iso_df.name=="Russian Federation", 'name'] = 'Russia'
    iso_df.loc[iso_df.name=="Korea, Republic of", 'name'] = 'South Korea'
    iso_df.loc[iso_df.name=="Macao", 'name'] = 'Macau'
    iso_df.loc[iso_df.name=="Taiwan, Province of China", 'name'] = 'Taiwan'
    iso_df.loc[iso_df.name=="Viet Nam", 'name'] = 'Vietnam'
    iso_df.loc[iso_df.name=="Iran (Islamic Republic of)", 'name'] = 'Iran'
    iso_df.loc[iso_df.name=="Czechia", 'name'] = 'Czech Republic'
    iso_df.loc[iso_df.name=="Saint Barthélemy", 'name'] = 'Saint Barthelemy'
    iso_df.loc[iso_df.name=="Palestine, State of", 'name'] = 'Palestine'
    iso_df.loc[iso_df.name=="Moldova, Republic of", 'name'] = 'Moldova'
    iso_df.loc[iso_df.name=="Ireland", 'name'] = 'Republic of Ireland'
    iso_df.loc[iso_df.name=="Holy See", 'name'] = 'Vatican City'


    
    df = pd.merge(df, iso_df, left_on="country_region", right_on='name')

    return df

def getIntervalData(df, interval='30D'):
    
    df.index = df.date

    df = df.groupby([pd.Grouper(freq=interval), 'country_region']).sum().reset_index()
    
    return df.sort_values(by=['country_region', 'date'])

def plot_countries(df=None, grouped_data=False, metric="confirmed"):
    
    if df is None:
        df = getCovidCasesWide()
   
    if grouped_data == False:
        df = df.groupby(['country_region', 'alpha-3']).sum().reset_index()
        
    fig = px.choropleth(df, locations="alpha-3",
                    color=metric, # lifeExp is a column of gapminder
                    hover_name="country_region", # column to add to hover information
                    color_continuous_scale='RdBu_r')
    fig.show()
    
    
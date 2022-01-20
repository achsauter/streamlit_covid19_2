# Core Pkgs

import streamlit as st
import streamlit.components.v1 as stc

# EDA Pkgs
import pandas as pd
import numpy as np
import random
import datetime as dt
from datetime import *

import requests
import io
# Data Viz Pkgs
import matplotlib

#matplotlib.use("Agg")
import altair as alt
#from bokeh.plotting import figure

# Utils
import c19_functions as c19_fkt
import load_data as ld

@st.cache
def load_all():
    df = pd.read_csv("RKI_COVID19.csv")
    return df

def load_all_welt():
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    return df


def load_fallzahlen(df, str_bundesland, bork):  #bundesland oder landkreis    
    #st.write(str_bundesland)
    data = {'IdLandkreis' : df.IdLandkreis,
       'Altersgruppe': df.Altersgruppe,
       'AnzahlFall': df.AnzahlFall,
       'TodesFall': df.AnzahlTodesfall,
       'Meldedatum': pd.to_datetime(df.Meldedatum),
       'Refdatum': pd.to_datetime(df.Refdatum)}
    
    df_return = pd.DataFrame(data)
    if check01 == 'Todesfälle':
        spalte = 2
    else:
        spalte = 1
    if str_bundesland != "all":
        if bork == "kreis":
            str_kreis = get_id_from_kreis(str_bundesland)
            #st.success(str_kreis)
            df_return = df_return[df_return['IdLandkreis'] == str_kreis]
            df_return.drop('IdLandkreis', axis=1, inplace=True)
            #st.dataframe(df_return)
        else:
            id_bl = str(int(get_id_from_bundesland(str_bundesland)))
            #st.success(id_bl)
            #st.success(len(id_bl))
            if len(id_bl) == 1:
                df_return["IdLandkreis"]= df_return["IdLandkreis"].astype(str)
                df_return = df_return[df_return['IdLandkreis'].str.len() == 4]
                df_return = df_return[df_return['IdLandkreis'].str[:1] == id_bl]
            else:  
                df_return["IdLandkreis"]= df_return["IdLandkreis"].astype(str)
                df_return = df_return[df_return['IdLandkreis'].str.len() == 5]
                df_return = df_return[df_return['IdLandkreis'].str[:2] == id_bl]
            #st.dataframe(df_return)
        selected_ort = str_bundesland
    else:
        selected_ort = "Deutschland"
        df_return.drop('IdLandkreis', axis=1, inplace=True)
        #st.success(str_bundesland)

    df_return = df_return.groupby(by=["Meldedatum"]).sum()
    df_return.reset_index(inplace=True)
    df_return['SiebenInz'] = ''
    df_return['Total_Faelle'] = ''
    df_return['Zuwachs'] = ''
    df_return['Todesfall_Sieben_Tage'] = 0
    #st.write(df_return.head())
    if bork == "kreis":
        anz_einw = get_ew_kreis(str_bundesland)
    else:
        anz_einw = get_ew_bundesland(str_bundesland)
    #st.success(anz_einw)
    #st.dataframe(df_return)
    #st.success('Spalte' + str(spalte))
    Gesamt = 0
    for i in range(len(df_return)):
        Anzahl = df_return.iloc[i, spalte]
        Gesamt = Gesamt + Anzahl
        summe = 0

        if i > 6:
            for j in range(i - 6, i +1 ):
                summe = summe + df_return.iloc[j, spalte]
            if check01 == 'Todesfälle':
                df_return.at[i,'Todesfall_Sieben_Tage']=summe/7
            else:
                summe = (summe / anz_einw) * 100000
            #df_return.at[i,'Todesfall_Sieben_Tage'] = 5
            df_return.at[i, 'SiebenInz'] = summe
            if i>45:
                df_return.at[i,'Zuwachs'] = ((df_return.iloc[i, 3] - df_return.iloc[i-6, 3])/df_return.iloc[i-6, 3])*100
            else:
                df_return.at[i,'Zuwachs'] = 0
        else:
            df_return.at[i, 'SiebenInz'] = 0
            df_return.at[i,'Zuwachs'] = 0
        if i>0:
            df_return.at[i, 'Total_Faelle'] = df_return.at[i-1, 'Total_Faelle'] + Anzahl 
        else:
            df_return.at[i, 'Total_Faelle'] = Anzahl 
    
    
    df_return = df_return[df_return['Meldedatum'] >= dt_start]        
    df_return = df_return[df_return['Meldedatum'] <= dt_end] 
    datum = df_return.iloc[len(df_return)-1,0].strftime('%d.%m.%Y')
    st.subheader(selected_ort + " am " + datum )
    
    show_chart(df_return)
    with st.expander("Tabelle"):
        st.dataframe(df_return)        
    return df_return

def get_sieben_tage_inzidenz_last(df,anz_einw, spalte):
    summe = 0
    for i in range(len(df) -7, len(df)):
        summe = summe + df.iloc[i,spalte]
    summe = (summe / anz_einw) * 100000
        
    return summe    


def show_chart(df_show): 
    #st.success(check01)
    if check01 == 'Todesfälle':
        c = alt.Chart(df_show).mark_area(color='yellow').encode(x="Meldedatum", y="Todesfall_Sieben_Tage")
    else:    
        c = alt.Chart(df_show).mark_area(color='darkred').encode(x="Meldedatum", y="SiebenInz", tooltip = ['Meldedatum', 'SiebenInz'])
    st.altair_chart(c, use_container_width=True)
    with st.expander("Anzahl Neue Fälle"):
        if check01 == 'Todesfälle':
            c = alt.Chart(df_show).mark_line(color='darkgreen').encode(x="Meldedatum", y="TodesFall",tooltip = ['Meldedatum', 'TodesFall']) 
        else:
            c = alt.Chart(df_show).mark_line(color='darkgreen').encode(x="Meldedatum", y="AnzahlFall",tooltip = ['Meldedatum', 'AnzahlFall']) 
        st.altair_chart(c, use_container_width=True)
    with st.expander("Anzahl Fälle gesamt"):
        c = alt.Chart(df_show).mark_line(color='darkgreen').encode(x="Meldedatum", y="Total_Faelle",tooltip = ['Meldedatum', 'Total_Faelle']) 
        st.altair_chart(c, use_container_width=True)
    with st.expander("Zuwachs"):
        c = alt.Chart(df_show).mark_line().encode(x="Meldedatum", y="Zuwachs",tooltip = ['Meldedatum', 'Zuwachs'])
        st.altair_chart(c, use_container_width=True)
        
def get_id_from_bundesland(str_name):
    #print(str_name)
    df_ew = pd.read_csv('EW2020.csv')
    df_names = get_bundeslaender()  
    for i in range(len(df_names)):
        if str_name == df_names.iloc[i,0]:
            found = i
    ret_value = df_ew.iloc[92,found+2]
    return ret_value

def get_ew_bundesland(str_name):
    #print(str_name)
    df_ew = pd.read_csv('EW2020.csv')
    if str_name == "all":
        ret_value=0
        for i in range(2,18):
            ret_value = ret_value + df_ew.iloc[91,i]
    else:   
        df_names = get_bundeslaender()  
        for i in range(len(df_names)):
            if str_name == df_names.iloc[i,0]:
                found = i
        ret_value = df_ew.iloc[91,found+2]
    #print(found)
    return ret_value

def get_landkreise(str_bundesland):
    df_ew = pd.read_excel('Einwohner_Landkreise.xlsx')
    df_li = pd.DataFrame(columns =[0, "IdLandkreis"])
    #st.success(len(df_ew))
    for i in range(len(df_ew)):
        df_li = pd.concat([pd.DataFrame([[df_ew.iloc[i,0],df_ew.iloc[i,3]]], columns=df_li.columns), df_li], ignore_index=True)
    #st.dataframe(df_li)
    id_bl = str(int(get_id_from_bundesland(str_bundesland)))
    if len(id_bl) == 1:
                #st.write(df_return.describe())
        df_li["IdLandkreis"]= df_li["IdLandkreis"].astype(str)
                #st.write(df_return.describe())
        df_li = df_li[df_li['IdLandkreis'].str.len() == 4]
                #st.write(df_return.describe())
        df_li = df_li[df_li['IdLandkreis'].str[:1] == id_bl]
                #st.write(df_return.describe())
    else:  
        df_li["IdLandkreis"]= df_li["IdLandkreis"].astype(str)
        df_li = df_li[df_li['IdLandkreis'].str.len() == 5]
        df_li = df_li[df_li['IdLandkreis'].str[:2] == id_bl]  
    df_li.drop('IdLandkreis', axis=1, inplace=True)
    
    #st.dataframe(df_li) 
    return df_li 

def get_ew_kreis(str_name):
    df_ew = pd.read_excel('Einwohner_Landkreise.xlsx')
    for i in range(len(df_ew)):
        if df_ew.iloc[i,0] == str_name:
            ret_value = df_ew.iloc[i,2] 
    return ret_value

def get_id_from_kreis(str_name):
    df_ew = pd.read_excel('Einwohner_Landkreise.xlsx')
    for i in range(len(df_ew)):
        if df_ew.iloc[i,0] == str_name:
            ret_value = df_ew.iloc[i,3] 
    return ret_value



def get_bundeslaender():
    df_ew = pd.read_csv('EW2020.csv')
    my_list = df_ew.columns.values.tolist()
    df_names = pd.DataFrame(my_list)
    #st.dataframe(df_names) 
    df_names.drop(0,inplace=True)
    df_names.drop(1,inplace=True)
    return df_names


def main():
    global check01
    check01 = 'Neue Fälle'
    global dt_start
    dt_start= '{:%Y-%m-%d}'.format(pd.to_datetime('2021-01-01'))
    global dt_end
    dt_end ='{:%Y-%m-%d}'.format(pd.to_datetime('2021-12-01'))
    
    menu = ["Home", "Deutschland", "weltweit","Listen", "About"]   #"Deutschland",

    
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        st.write('Robert Koch-Institut (2021): SARS-CoV-2 Infektionen in Deutschland, Berlin: Zenodo. DOI:10.5281/zenodo.4681153')
        
    if choice == 'Deutschland':
        df = ld.load_from_rki()
        menu2 =  get_bundeslaender()
        #st.dataframe(menu2)
        df2 = pd.DataFrame([["all"]],index=[1])
        df2.sort_index(ascending=True)
        menu2 = menu2.append(df2)
        #st.dataframe(menu2)
        menu2.sort_index(axis = 0, inplace=True)  
        
        check01 = st.sidebar.radio('Anzeige',['Neue Fälle','Todesfälle']) 
        col1, col2 = st.sidebar.columns(2)
        with col1:
            dt_start = '{:%Y-%m-%d}'.format(st.sidebar.date_input('Startdatum',pd.to_datetime('2020-01-23')))
        with col2:
            dt_end = '{:%Y-%m-%d}'.format(st.sidebar.date_input('end date'))
        
        choice_bundesland = st.sidebar.selectbox("Auswahl Bundesland", menu2)
            
        if choice_bundesland == "all":
            df_show = load_fallzahlen(df, "all",'')
        else:
            df_lk = get_bundeslaender()
            #st.dataframe(df_lk)
            
            menu3 =  get_landkreise(choice_bundesland)
            
            df3 = pd.DataFrame([["all"]],index=[1])
            df3.sort_index(ascending=True)
            menu3 = menu3.append(df3)
            #st.dataframe(menu3)
            menu3.sort_index(axis = 0, inplace=True)


            choice_kreis = st.sidebar.selectbox("Auswahl Kreis", menu3)
            if choice_kreis == 'all':
                df_show = load_fallzahlen(df, choice_bundesland,'')
            else:
                df_show = load_fallzahlen(df, choice_kreis,'kreis')
            
        if st.sidebar.checkbox('Liste', key='check02'):
            data = {'IdLandkreis': df.IdLandkreis,
                'AnzahlFall': df.AnzahlFall,
                'Meldedatum': pd.to_datetime(df.Meldedatum)}
            df = pd.DataFrame(data)
            if choice_bundesland == "all":
                df_names = get_bundeslaender()
                
                for i in range(len(df_names)):
                    temp_list = get_landkreise(df_names.iloc[i,0])
                    if i==0:
                        my_list = temp_list
                    else:
                        my_list = pd.concat([temp_list,my_list]) 
            else:
                my_list = get_landkreise(choice_bundesland)    

            #st.dataframe(my_list)
            #st.success(my_list.iloc[12,0])
            df_liste2 = pd.DataFrame()
            for i in range(len(my_list)):
                #st.write(my_list.iloc[i,0])
                einw = get_ew_kreis(my_list.iloc[i,0])
                temp_id = get_id_from_kreis(my_list.iloc[i,0])
                #st.write(temp_id)
                df_new = df[df['IdLandkreis'] == temp_id]
                #st.dataframe(df_new)
                df_return = df_new.groupby(by=["Meldedatum"]).sum()
                #st.dataframe(df_return)
                erg = c19_fkt.get_sieben_tage_inzidenz_last(df_return, einw, 1)
                df_liste2.at[i, 'Landkreis'] = my_list.iloc[i,0]
                #format(df_result.iloc[len(df_result)-1,5],'>15,.0f').replace(",",".")+ '  \n '+
                df_liste2.at[i, 'Inzidenz'] = format(erg,'>15,.1f').replace(",",".")
                #st.write(erg)
            st.dataframe(df_liste2)


    if choice == 'weltweit':
        df = load_all_welt()
        
        df_laender_liste = pd.DataFrame(pd.unique(df.location))
        #menu3 = 'Germany' #pd.DataFrame([["all"]],index=[0])
        menu3 = pd.DataFrame()
        menu3 = menu3.append(df_laender_liste) 
        menu3.sort_index(ascending=True,axis = 0, inplace=True)
        col1, col2 = st.sidebar.columns(2)
        choice_land = st.sidebar.selectbox("Auswahl Land", menu3, index=79)    #Germany
        with col1:
            dt_start = '{:%Y-%m-%d}'.format(st.sidebar.date_input('Startdatum',pd.to_datetime('2020-01-23')))
        with col2:
            dt_end = '{:%Y-%m-%d}'.format(st.sidebar.date_input('end date'))
        #st.dataframe(menu3)
        df_result = df[df['location'] == choice_land] 
        df_result.date = pd.to_datetime(df_result['date'])
             
        del df_result['tests_units']
        # my_list = df_result.columns.values.tolist()
        # st.dataframe(my_list)
        df_result = df_result.sort_values(by='date', ascending=True)
        df_result.fillna(method='ffill', inplace=True)
        df_result['faelle'] = 0
        df_result['todesfaelle'] = 0
        df_result['sieben_faelle'] = 0
        df_result['sieben_todesfaelle'] = 0  
        df_result['verh'] = 0 
        datum = df_result.iloc[len(df_result)-1,3].strftime('%d.%m.%Y')
        df_result = df_result[df_result['date'] >= dt_start]        
        df_result = df_result[df_result['date'] <= dt_end] 
        st.subheader(choice_land + " am " + datum)
        #st.dataframe(df_result)
        for i in range(len(df_result)):
             summe = 0
             summe2 =0
             if i>= 7:
                for j in range(i - 7, i):
                    summe = summe + df_result.iloc[j, 5]
                    summe2 = summe2 + df_result.iloc[j, 8]
                df_result.iat[i,68] = summe/df_result.iloc[len(df_result)-1,47] * 100000 #Einwohner  
                df_result.iat[i,69] = summe2 / 7
             else:
                df_result.iat[i,68]= 0 
                df_result.iat[i,69]= 0
         

        col1, col2 = st.columns(2)
        columns = df_result.columns
        column_index = columns.get_loc('population')
        #st.write("Index of the column population is: ", column_index)
        with col1:
            st.write('Neuinfektionen : ' + format(df_result.iloc[len(df_result)-1,5],'>15,.0f').replace(",",".")+ '  \n '+
                'Todesfälle : ' + format(df_result.iloc[len(df_result)-1,8],'>15,.0f').replace(",",".") + '  \n '+
                'Erstimpfungen : ' + format(df_result.iloc[len(df_result)-1,34],'>15,.0f').replace(",",".") + '  \n '+
                'Zweitimpfungen : ' + format(df_result.iloc[len(df_result)-1,35],'>15,.0f').replace(",",".") + '  \n '+ 
                'Boosterimpfungen : ' + format(df_result.iloc[len(df_result)-1,36],'>15,.0f').replace(",","."))
            st.write('Einwohner : ' + format(df_result.iloc[len(df_result)-1,columns.get_loc('population')],'>15,.0f').replace(",",".")+ '  \n '+
                '7 Tage Inzidenz (heute) : ' + format(df_result.iloc[len(df_result)-1,68],'>15,.1f').replace(",",".")+ '  \n '+
                '7 Tage Inzidenz (Woche) : ' + format(df_result.iloc[len(df_result)-8,68],'>15,.1f').replace(",",".")+ '  \n ' +
                '7 Tage Inzidenz (Monat) : ' + format(df_result.iloc[len(df_result)-31,68],'>15,.1f').replace(",",".")+ '  \n ')  
            c = alt.Chart(df_result).mark_line(color='darkgreen').encode(x='date', y='sieben_faelle',tooltip = ['date', 'sieben_faelle']) 
            st.altair_chart(c, use_container_width=True)
        with col2:
            st.write('Infektionen gesamt: ' + format(df_result.iloc[len(df_result)-1,4],'>15,.0f').replace(",",".") + '  \n '+
                'Todesfälle gesamt : ' + format(df_result.iloc[len(df_result)-1,7],'>15,.0f').replace(",",".") + '  \n '+
                'Erstimpfungen gesamt: ' + format(df_result.iloc[len(df_result)-1,40],'>15,.1f').replace(",",".") + '%' + '  \n '+
                'Impfungen vollständig gesamt: ' + format(df_result.iloc[len(df_result)-1,41],'>15,.1f').replace(",",".") + '%' + '  \n '+
                'Booster gesamt: ' + format(df_result.iloc[len(df_result)-1,42],'>15,.1f').replace(",",".") + '%')
            st.write('Todesfälle (Schnitt der vergangenen 7 Tage)' + '  \n '+
                'Todesfälle (heute) : ' + format(df_result.iloc[len(df_result)-1,69],'>15,.0f').replace(",",".")+ '  \n '+
                'Todesfälle (Woche) : ' + format(df_result.iloc[len(df_result)-8,69],'>15,.0f').replace(",",".")+ '  \n ' +
                'Todesfälle (Monat) : ' + format(df_result.iloc[len(df_result)-31,69],'>15,.0f').replace(",",".")+ '  \n ')  
            c = alt.Chart(df_result).mark_line(color='black').encode(x='date', y='sieben_todesfaelle',tooltip = ['date', 'sieben_todesfaelle']) 
            st.altair_chart(c, use_container_width=True)
            df_result["verh"] = (df_result["total_deaths"]/df_result["total_cases"])*100
                  
        c = alt.Chart(df_result).mark_line(color='black').encode(x='date', y='hosp_patients_per_million',tooltip = ['date', 'hosp_patients_per_million']) 
        st.altair_chart(c, use_container_width=True) 
        c = alt.Chart(df_result).mark_line(color='black').encode(x='date', y='verh',tooltip = ['date', 'verh']) 
        st.altair_chart(c, use_container_width=True)
        
    if choice == 'Listen':
        df_countries = pd.DataFrame(["Germany", "France", "Spain","Italy", "United Kingdom","Netherlands", "Belgium","Portugal", "Austria","Poland", "Czechia","Slovakia", "Slovenia","Hungary", "Estonia", "Lithuania", "Latvia", "Greece","Switzerland","Bulgaria","Romania","Sweden","Finland", "Norway","Denmark", "Luxembourg", "Liechtenstein","Russia","Ireland"],columns=['Land'])
        
        df_countries['Inzidenz'] = 0
        df_countries['Hosp per million'] = 0
        df = load_all_welt()  

        for i in range(len(df_countries)):
            country_name = df_countries.iloc[i,0] 
            df_neu = df[df['location'] == country_name]
            #st.dataframe(df_neu)
            summe = 0
            for j in range(len(df_neu) - 7, len(df_neu)):
                summe = summe + df_neu.iloc[j, 5]
            df_countries.iat[i,1] = format(summe/df_neu.iloc[len(df_neu)-1,48] * 100000,'>15,.1f').replace(",",".")    
            columns = df_neu.columns
            column_index = columns.get_loc('hosp_patients_per_million')
            #st.success(column_index)
            #st.success(len(df_neu))
            df_countries.iat[i,2] = df_neu.iloc[len(df_neu)-4,column_index]
        df_countries.sort_values('Inzidenz', inplace=True, ascending=False)    
        df_countries.reset_index(drop=True, inplace=True) 
        st.dataframe(df_countries,800,1000)
        
    
        
    
    
if __name__ == "__main__":
    main()
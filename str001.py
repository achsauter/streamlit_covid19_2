# Core Pkgs
#from bokeh.models.filters import IndexFilter
import streamlit as st
import streamlit.components.v1 as stc

# EDA Pkgs
import pandas as pd
import numpy as np
import random
import datetime as dt
from datetime import *

# Data Viz Pkgs
import matplotlib

#matplotlib.use("Agg")
import altair as alt
#from bokeh.plotting import figure

# Utils

@st.cache
def load_all():
    df = pd.read_csv("RKI_COVID19.csv")
    # df = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Baden-Württemberg.csv")
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Bayern.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Berlin.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Brandenburg.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Bremen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Hamburg.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Hessen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Mecklenburg-Vorpommern.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Niedersachsen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Nordrhein-Westfalen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Rheinland-Pfalz.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Saarland.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Sachsen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Sachsen-Anhalt.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Schleswig-Holstein.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    # df_load = pd.read_csv("BigData/antwerp/Data/RKI_COVID19_Thüringen.csv")
    # df = pd.merge(df,df_load, how = 'outer')
    return df

def load_all_welt():
    df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    return df
def load_fallzahlen(df, str_bundesland, bork):  #bundesland oder landkreis   
    data = {'Bundesland': df.Bundesland,
       'Landkreis': df.Landkreis,
       'Bundesland' : df.Bundesland,
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
            df_return = df_return[df_return['Landkreis'] == str_bundesland]
        else:    
            df_return = df_return[df_return['Bundesland'] == str_bundesland]
        selected_ort = str_bundesland
    else:
        selected_ort = "Deutschland"
        #st.success(str_bundesland)

    df_return = df_return.groupby(by=["Meldedatum"]).sum()
    df_return.reset_index(inplace=True)
    df_return['SiebenInz'] = ''
    df_return['Total_Faelle'] = ''
    df_return['Zuwachs'] = ''
    df_return['Todesfall_Sieben_Tage'] = 0
    if bork == "kreis":
        anz_einw = get_ew_kreis(str_bundesland)
    else:
        anz_einw = get_ew_bundesland(str_bundesland)
    #st.success(anz_einw)
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
    #st.success(df_return)
    #st.success(type(dt_start))
    #st.success(type(df_return['Meldedatum']))
    df_return = df_return[df_return['Meldedatum'] >= dt_start]        
    df_return = df_return[df_return['Meldedatum'] <= dt_end] 
    datum = df_return.iloc[len(df_return)-1,0].strftime('%d.%m.%Y')
    st.subheader(selected_ort + " am " + datum + ' (' + check01 + ')')
    
    st.write('Neue Fälle : ')
    show_chart(df_return)
    with st.expander("Tabelle"):
        st.dataframe(df_return)        
    return df_return

def get_sieben_tage_inzidenz_last(df,anz_einw, spalte):
    summe = 0
    #st.dataframe(df)
    #st.write(df.describe())
    #st.write(df.iloc[630,0])
    #st.write(len(df) - 7)
    #st.write(len(df))
    #st.write(anz_einw)
    for i in range(len(df) -7, len(df)):
        #st.write(df.iloc[i,0])
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
    c = alt.Chart(df_show).mark_line(color='darkgreen').encode(x="Meldedatum", y="Total_Faelle",tooltip = ['Meldedatum', 'Total_Faelle']) 
    st.altair_chart(c, use_container_width=True)
    c = alt.Chart(df_show).mark_line().encode(x="Meldedatum", y="Zuwachs",tooltip = ['Meldedatum', 'Zuwachs'])
    st.altair_chart(c, use_container_width=True)
        
def get_ew_bundesland(str_name):
    #print(str_name)
    df_ew = pd.read_excel('EW2020.xlsx')
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

def get_ew_kreis(str_name):
    print(str_name)
    df_ew = pd.read_excel('Einwohner_Landkreise.xlsx')
    for i in range(len(df_ew)):
        if df_ew.iloc[i,0] == str_name:
            ret_value = df_ew.iloc[i,2] 
     
    #st.write(ret_value)
    #ret_value = 10
    return ret_value



def get_bundeslaender():
    df_ew = pd.read_excel('EW2020.xlsx')
    my_list = df_ew.columns.values.tolist()
    df_names = pd.DataFrame(my_list)
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
    
    menu = ["Home",  "weltweit", "About"]   #"Deutschland",

    #df = load_all()
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Home':
        pass
    if choice == 'Deutschland':
        df = load_all()
        #if st.sidebar.checkbox("Altersgruppen", 'check01'): 
        #   pass
        #     data = {'Bundesland': df.Bundesland,
        #         'Landkreis': df.Landkreis,
        #         'Bundesland' : df.Bundesland,
        #         'Altersgruppe': df.Altersgruppe,
        #         'AnzahlFall': df.AnzahlFall,
        #         'TodesFall': df.AnzahlTodesfall,
        #         'Meldedatum': pd.to_datetime(df.Meldedatum),
        #         'Refdatum': pd.to_datetime(df.Refdatum)}
        #     df_return = pd.DataFrame(data)
        #     df_grouped =df_return.groupby(['Meldedatum','Altersgruppe'], as_index = False).sum()
        #     #df_grouped.columns =['Altersgruppe', 'Datum','AnzahFall', 'TodesFall']
        #     st.dataframe(df_grouped)
        #     my_list = df_grouped['Altersgruppe'].unique()
        #     #st.dataframe(my_list)
        
            
 
        menu2 =  get_bundeslaender()
        #st.write(menu2)
        #st.success(type(menu2))
        df2 = pd.DataFrame([["all"]],index=[1])
        df2.sort_index(ascending=True)
        menu2 = menu2.append(df2)
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
            #st.dataframe(df_show)
        else:
            df_lk = df[df['Bundesland'] == choice_bundesland]
            menu3 = pd.DataFrame([["all"]],index=[0])
            df_lk_liste = pd.DataFrame(pd.unique(df_lk.Landkreis))
            menu3 = menu3.append(df_lk_liste)
            menu3.sort_index(ascending=True,axis = 0, inplace=True)
            #menu2.sort_index(axis = 0, inplace=True) 
            #menu3 = menu3.append(df_lk)
            #menu3.sort_index(axis = 0, inplace=True)
            choice_kreis = st.sidebar.selectbox("Auswahl Kreis", menu3)
            if choice_kreis == 'all':
                df_show = load_fallzahlen(df, choice_bundesland,'')
            else:
                df_show = load_fallzahlen(df, choice_kreis,'kreis')
        # st.sidebar.header("Datumsauswahl")
        if st.sidebar.checkbox('Liste', key='check02'):
            data = {'Bundesland': df.Bundesland,
                'Landkreis': df.Landkreis,
                'AnzahlFall': df.AnzahlFall,
                'Meldedatum': pd.to_datetime(df.Meldedatum)}
            df = pd.DataFrame(data)
            # if choice_bundesland == 'all':
            #     my_list = df['Bundesland'].unique()
            # else:
            #     my_list = df['Bundesland'].unique()
            # df_liste = pd.DataFrame()
            # for i in range(len(my_list)):
            #     einw = get_ew_bundesland(my_list[i])
            #     df_new = df[df['Bundesland'] == my_list[i]]
            #     df_return = df_new.groupby(by=["Meldedatum"]).sum()
            #     erg = get_sieben_tage_inzidenz_last(df_return, einw, 0)
            #     df_liste.at[i, 'Bundesland'] = my_list[i]
            #     #format(df_result.iloc[len(df_result)-1,5],'>15,.0f').replace(",",".")+ '  \n '+
            #     df_liste.at[i, 'Inzidenz'] = format(erg,'>15,.1f').replace(",",".")
            #     #st.write(erg)
            # st.dataframe(df_liste)
            
            my_list = df['Landkreis'].unique()
            df_liste2 = pd.DataFrame()
            for i in range(len(my_list)):
                #st.write(my_list[i])
                einw = get_ew_kreis(my_list[i])
                df_new = df[df['Landkreis'] == my_list[i]]
                df_return = df_new.groupby(by=["Meldedatum"]).sum()
                erg = get_sieben_tage_inzidenz_last(df_return, einw, 0)
                df_liste2.at[i, 'Landkreis'] = my_list[i]
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
        #st.dataframe(menu3)
        choice_land = st.sidebar.selectbox("Auswahl Land", menu3, index=79)    #Germany
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
        st.subheader(choice_land + " am " + datum)
        #st.dataframe(df_result)
        for i in range(len(df_result)):
             summe = 0
             summe2 =0
             if i>= 7:
                for j in range(i - 6, i+1):
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
            #df_liste3 = pd.DataFrame(columns=['Datum','Verh']) 
            #    df_result.iat[i,columns.get_loc('verh')] = (df_result.iloc[i,7]+df_result.iloc[i,4])
        #st.write(columns.get_loc('verh')-1)
        #st.dataframe(columns)  
        #st.dataframe(df_result)       
        c = alt.Chart(df_result).mark_line(color='black').encode(x='date', y='verh',tooltip = ['date', 'verh']) 
        st.altair_chart(c, use_container_width=True) 
        
        
        
        
        
        
            
    
        
    
    
if __name__ == "__main__":
    main()
#Functions Covid 19 : c19_functions.py
import pandas as pd

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
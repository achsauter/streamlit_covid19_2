
#import streamlit as st

import pandas as pd
import requests
import io
    
def load_from_rki():
    url = "https://media.githubusercontent.com/media/robert-koch-institut/SARS-CoV-2_Infektionen_in_Deutschland/master/Aktuell_Deutschland_SarsCov2_Infektionen.csv" # Make sure the url is the raw version of the file on GitHub
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))
    return df
    
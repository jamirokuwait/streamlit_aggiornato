import json
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsbombpy as sb
from pandas.io.json import json_normalize


calcio = st.file_uploader("Carica il file scegliendolo dal pc", type={
                          "json"})  # file uploader per caricare il json


st.write('visualizzazione del File')
if calcio is not None:
    calcio_df = pd.read_json(calcio)
st.write(calcio_df)

with open('open-data-master/data/matches/16/37.json') as f:
    data = json.load(f)
data
for i in data:
    st.write('ID:', i['match_id'], i['home_team']['home_team_name'],  # carico i dati relativi a squadre e risultato
             i['home_score'], '-', i['away_score'], i['away_team']['away_team_name'])

with open('open-data-master/data/events/2302764.json') as f:
    milliv = json.load(f)  # carico eventi partita specifica


df = pd.json_normalize(milliv, sep='_').assign(match_id="2302764")
df

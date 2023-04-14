import pandas as pd
import streamlit as st
st.set_page_config(layout="wide")

st.title('Premier League 2021-2022')
st.subheader('Players by Goals')
df = pd.read_csv('Es4/premier.csv')
df1 = df.sort_values(by=['G+A'], ascending=False)


# dfplayer = df['Player']
# dflist = dfplayer.values.tolist()
# playerlist = []

# for i in dflist:
#     playerfiltered = i.split("\\")
#     playerlist.append(playerfiltered[0])

# df['Player'] = playerlist
# nation = df['Nation']
# nation

# SETTING THE TITLE
title = "Player dashboard"  # SETTING LAYOUT
#
# using whole page#DISPLAYING THE TITLE
st.title(title)
# DISPLAYING A HORIZONTAL LINE TO SEPERATE CONTENT
st.markdown("---")
# CREATING A SIDEBAR WITH FILTER FOR PLAYERS
st.sidebar.header("Please Filter Here:")
player = st.selectbox(
    "Select player",
    options=df["Player"].unique())  # posso scegliere come opzione ogni valore univoco sulla colonna players

df_selection = df.query(  # seleziona tutta la riga
    # @ si riferisce ad una variabile creata da me,gli sto dicendo di assegnare a df_selections la riga dove avviene la query,che entry ho scelto sulla colonna Players
    "Player == @player"
)
df_selection
# SELECTING THE STATS FROM THE DATA THAT WILL BE DISPLAYED

# seleziono gls dalla riga corrispondente del giocatore
goals = df_selection["Gls"].sum()
assists = df_selection["Ast"].sum()
expectedgoals = df_selection["xG"].sum()
# DISPLAYING THE SELECTED STATS INSIDE COLUMNS
left_column, middle_column, right_column, rightright_column = st.columns(4)
with left_column:
    st.subheader("Goals")
    st.subheader(f"{goals}")
with middle_column:
    st.subheader("Assists")
    st.subheader(f"{assists}")
with right_column:
    st.subheader("Expected goals")
    st.subheader(f"{expectedgoals}")
with rightright_column:
    st.subheader("Player Name")
    st.subheader(f"{player}")

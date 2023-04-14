import json
import unicodedata
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import statsbombpy as sb
# from pandas.io.json import json_normalize
from FCPython import createPitch
# from matplotlib.offsetbox import OffsetImage
# from matplotlib.patches import Arc, Rectangle, ConnectionPatch


st.title('SELECT YOUR CSV')

st.write('CHOOSING FROM STATSBOMB DATA')
calcio = st.file_uploader("Carica il file scegliendolo dal pc", type={"json"})

st.write('MAJOR COMPETITION RECORDED')
if calcio is not None:
    calcio_df = pd.read_json(calcio)
with st.expander('Click for display all competitions available'):
    st.write(calcio_df)
st.write('SEARCHING FOR 2018 FIFA WORLD CUP MATCHES')
st.write(calcio_df[calcio_df.competition_name == 'FIFA World Cup'])


# with open('open-data-master/data/matches/43/3.json') as f:
#     # carica idati delle squadre,match,dati sulle partite generali
#     data = json.load(f)
# # salto questa parte per il retrieve degli id delle partite della competizione
# # st.write('displaying every match,with ID and group')
# for i in data:
#     x = st.write('ID:', i['match_id'],  i['home_team']['home_team_name'],  # carico i dati relativi a squadre e risultato
#                  i['home_score'], '-', i['away_score'], i['away_team']['away_team_name'], '-', i['home_team']['home_team_group'])

with open('7567.json') as f:
    korger = json.load(f)  # carico eventi partita specifica

df = pd.json_normalize(korger, sep='_').assign(match_id="7567")

df['player_name'] = df['player_name'].astype(str)
df['player_name'] = df['player_name'].apply(lambda val: unicodedata.normalize('NFC', val).encode(
    'ascii', 'ignore').decode('utf-8'))
df['player_name'] = df['player_name'].replace('nan', np.nan)


cols = list(df.columns.values)  # Make a list of all of the columns in the df
cols.pop(cols.index('id'))
cols.pop(cols.index('index'))
cols.pop(cols.index('period'))
cols.pop(cols.index('minute'))
cols.pop(cols.index('second'))
cols.pop(cols.index('location'))
cols.pop(cols.index('possession'))
cols.pop(cols.index('tactics_formation'))
cols.pop(cols.index('tactics_lineup'))
cols.pop(cols.index('play_pattern_id'))
cols.pop(cols.index('type_id'))
cols.pop(cols.index('team_id'))
cols.pop(cols.index('player_id'))
cols.pop(cols.index('related_events'))
cols.pop(cols.index('position_id'))
cols.pop(cols.index('possession_team_id'))
df = df[cols+['id', 'index', 'period', 'minute',
              'second', 'possession', 'possession_team_id', 'tactics_formation', 'tactics_lineup', 'play_pattern_id', 'type_id', 'team_id', 'player_id', 'position_id', 'related_events', 'location']]  # addo alla fine

plname_column = df.pop('player_name')
posname_column = df.pop('position_name')

df.insert(1, 'player_name', plname_column)
df.insert(2, 'position_name', posname_column)


home_team = 'South Korea'
away_team = 'Germany'
Actionpass = 'Pass'
Actionshot = 'Shot'
Actionpress = 'Pressure'
p1 = '1st period'
p2 = '2nd period'

# playerskor = df[df.team_name == 'South Korea']
# questo prende tutto il df.unique e drop non funziano sul df intero
# playersger = df[df.team_name == 'Germany']

# applico .unique alla series dei team name,che sono solo 2,per il team che gioca in casa uno index 0
team_1 = df['team_name'].unique()[0]
# scelgo le righe a cui corrisponde team name uguale a team a index 0
mask_1 = df.loc[df['team_name'] == team_1]
# le filtro per valori unici e non nulli
player_names_1 = mask_1['player_name'].dropna().unique()

team_2 = df['team_name'].unique()[1]
mask_2 = df.loc[df['team_name'] == team_2]
player_names_2 = mask_2['player_name'].dropna().unique()


menu_team = st.sidebar.selectbox('Select Team', (team_1, team_2))
menu_action = st.sidebar.selectbox(
    'Select action', (Actionpass, Actionshot, Actionpress))

if menu_team == team_1:
    menu_player = st.sidebar.selectbox('Select Player', player_names_1)
else:
    menu_player = st.sidebar.selectbox('Select Player', player_names_2)

menu_time = st.sidebar.selectbox('Select period', (p1, p2))


pressure = df[df.type_name == 'Pressure']
pressureaway = pressure[pressure.team_name == away_team]
pressurehome = pressure[pressure.team_name == home_team]
pressure1 = pressure[pressure.period == 1]
pressure2 = pressure[pressure.period == 2]

pressure1away = pressure1[pressure1.team_name == away_team]
pressure2away = pressure2[pressure2.team_name == away_team]
pressure1home = pressure1[pressure1.team_name == home_team]
pressure2home = pressure2[pressure2.team_name == home_team]

press1away = pressure1away[pressure1away.player_name == menu_player]
press2away = pressure2away[pressure2away.player_name == menu_player]
press1home = pressure1home[pressure1home.player_name == menu_player]
press2home = pressure2home[pressure2home.player_name == menu_player]


passages = df[df.type_name == 'Pass']
passages1 = passages[passages.period == 1]
passages2 = passages[passages.period == 2]

passages1away = passages1[passages1.team_name == away_team]
passages1home = passages1[passages1.team_name == home_team]
passages2away = passages2[passages2.team_name == away_team]
passages2home = passages2[passages2.team_name == home_team]

pass1away = passages1away[passages1away.player_name == menu_player]
pass2away = passages2away[passages2away.player_name == menu_player]
pass1home = passages1home[passages1home.player_name == menu_player]
pass2home = passages2home[passages2home.player_name == menu_player]

shots = df[df.type_name == 'Shot']  # df tiri selezionando type name shot

shots1 = shots[shots.period == 1]  # df tiri primo e secondo tempo
shots2 = shots[shots.period == 2]

shotshome = shots[shots.team_name == home_team]  # tiri totali casa
shots1home = shots1[shots1.team_name == home_team]  # tiri tot 1 tempo casa
shots2home = shots2[shots2.team_name == home_team]  # tiri tot 2 tempo casa

shotsaway = shots[shots.team_name == away_team]
shots1away = shots1[shots1.team_name == away_team]  # tiri tot 1 tempo ospiti
shots2away = shots2[shots2.team_name == away_team]  # tiri tot 2 tempo ospiti

sht1away = shots1away[shots1away.player_name ==
                      menu_player]  # tiri per giocatore selezionato
sht2away = shots2away[shots2away.player_name == menu_player]
sht1home = shots1home[shots1home.player_name == menu_player]
sht2home = shots2home[shots2home.player_name == menu_player]


golkor = shotshome[shotshome.shot_outcome_name == 'Goal']

st.header('Data visualization by tabs')
with st.expander('Click for display all tabs available'):
    tab11, tab22 = st.tabs(['South Korea', 'Germany'])
    with tab11:

        tab1, tab2, tab3 = st.tabs(['shots', 'pass', 'pressure'])
        with tab1:
            st.subheader('Displaying Korea shots')
            shotshome
        with tab2:
            st.subheader('Displaying Korea pass')
            passages1home
            passages2home
        with tab3:
            st.subheader('Pressure Korea')
            pressurehome
    with tab22:

        tab1, tab2, tab3 = st.tabs(['shots', 'pass', 'pressure'])
        with tab1:
            st.subheader('Displaying Germany shots')
            shotsaway
        with tab2:
            st.subheader('displaying Germany pass')
            passages1away
            passages2away
        with tab3:
            st.subheader('Pressure Germany')
            pressureaway

#
#


# st.header('Goal event')
# golkor
# st.subheader('visualizzo i tiri effettuati dalla Germania')
# shotsger
# st.subheader('visualizzo passaggi Germania')
# passages1ger
# st.subheader('Pressure Germania')
# pressureger


pitch_width = 120
pitch_height = 80

fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')


############# GRAFICO TIRI###################


color = 'blue' if menu_team == home_team else 'red'


if menu_action == Actionshot:

    if menu_time == p1:

        if menu_team == home_team:
            plt.text(49, 75, home_team + ' shots')
            for i, shot in sht1home.iterrows():
                x = shot['location'][0]
                y = shot['location'][1]

                goal = shot['shot_outcome_name'] == 'Goal'
                team_name = shot['team_name']

                circle_size = 2
                circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)

                if goal:
                    shot_circle = plt.Circle(
                        (x, pitch_height-y), circle_size, color='blue')
                    plt.text((x+1), pitch_height-y+1, shot['player_name'])

                else:
                    shot_circle = plt.Circle(
                        (x, pitch_height-y), circle_size, color='blue')
                    shot_circle.set_alpha(.2)
                if menu_team == home_team:
                    ax.add_patch(shot_circle)
        elif menu_team == away_team:
            plt.text(51, 75, away_team + ' shots')
            for i, shot in sht1away.iterrows():
                x = shot['location'][0]
                y = shot['location'][1]

                goal = shot['shot_outcome_name'] == 'Goal'
                team_name = shot['team_name']

                circle_size = 2
                circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)
                if goal:
                    shot_circle = plt.Circle(
                        (pitch_width-x, y), circle_size, color='red')
                    plt.text((pitch_width-x+1), y+1, shot['player_name'])
                else:
                    shot_circle = plt.Circle(
                        (pitch_width-x, y), circle_size, color='red')
                    shot_circle.set_alpha(.2)
                if menu_team == away_team:
                    ax.add_patch(shot_circle)
    elif menu_time == p2:
        if menu_team == home_team:
            plt.text(49, 75, home_team + ' shots')
            for i, shot in sht2home.iterrows():
                x = shot['location'][0]
                y = shot['location'][1]

                goal = shot['shot_outcome_name'] == 'Goal'
                team_name = shot['team_name']

                circle_size = 2
                circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)

                if goal:
                    shot_circle = plt.Circle(
                        (x, pitch_height-y), circle_size, color='blue')
                    plt.text((x+1), pitch_height-y+1, shot['player_name'])

                else:
                    shot_circle = plt.Circle(
                        (x, pitch_height-y), circle_size, color='blue')
                    shot_circle.set_alpha(.2)
                if menu_team == home_team:
                    ax.add_patch(shot_circle)
        elif menu_team == away_team:
            plt.text(51, 75, away_team + ' shots')
            for i, shot in sht2away.iterrows():
                x = shot['location'][0]
                y = shot['location'][1]

                goal = shot['shot_outcome_name'] == 'Goal'
                team_name = shot['team_name']

                circle_size = 2
                circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)
                if goal:
                    shot_circle = plt.Circle(
                        (pitch_width-x, y), circle_size, color='red')
                    plt.text((pitch_width-x+1), y+1, shot['player_name'])
                else:
                    shot_circle = plt.Circle(
                        (pitch_width-x, y), circle_size, color='red')
                    shot_circle.set_alpha(.2)
                if menu_team == away_team:
                    ax.add_patch(shot_circle)
elif menu_action == Actionpass:

    if menu_time == p1:
        if menu_team == away_team:
            plt.text(51, 75, away_team + ' pass')
            for i, pas in pass1away.iterrows():
                x = pas['location'][0]
                y = pas['location'][1]
                x1 = pas['pass_end_location'][0]
                y1 = pas['pass_end_location'][1]
                u = x1-x
                v = y1-y

                # passage = pas['type_name'] == 'Pass'
                # team_name = pas['team_name']
                ax.quiver(x, y, u, v, color=color, width=0.003, headlength=4.5)
        elif menu_team == home_team:
            plt.text(51, 75, home_team + ' pass')
            for i, pas in pass1home.iterrows():
                x = pas['location'][0]
                y = pas['location'][1]
                x1 = pas['pass_end_location'][0]
                y1 = pas['pass_end_location'][1]
                u = x1-x
                v = y1-y

                # passage = pas['type_name'] == 'Pass'
                # team_name = pas['team_name']
                ax.quiver(x, y, u, v, color=color, width=0.003, headlength=4.5)

    elif menu_time == p2:
        if menu_team == home_team:
            plt.text(51, 75, home_team + ' pass')
            for i, pas in pass2home.iterrows():
                x = pas['location'][0]
                y = pas['location'][1]
                x1 = pas['pass_end_location'][0]
                y1 = pas['pass_end_location'][1]
                u = x1-x
                v = y1-y

                passage = pas['type_name'] == 'Pass'
                team_name = pas['team_name']

                ax.quiver(x, y, u, v, color=color, width=0.003, headlength=4.5)
        elif menu_team == away_team:
            plt.text(51, 75, away_team + ' pass')

            for i, pas in pass2away.iterrows():
                x = pas['location'][0]
                y = pas['location'][1]
                x1 = pas['pass_end_location'][0]
                y1 = pas['pass_end_location'][1]
                u = x1-x
                v = y1-y

                passage = pas['type_name'] == 'Pass'
                team_name = pas['team_name']

                ax.quiver(x, y, u, v, color=color, width=0.003, headlength=4.5)
elif menu_action == Actionpress:

    dot_size = 2
    if menu_time == p1:

        if menu_team == home_team:
            plt.text(51, 75, home_team + ' pressing')
            for i, pres in press1home.iterrows():
                x = pres['location'][0]
                y = pres['location'][1]
                dot_size = 2

                dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
                ax.add_patch(dot)

        elif menu_team == away_team:
            plt.text(51, 75, away_team + ' pressing')
            for i, pres in press1away.iterrows():
                x = pres['location'][0]
                y = pres['location'][1]
                dot_size = 2

                dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
                ax.add_patch(dot)
    elif menu_time == p2:
        if menu_team == home_team:
            plt.text(51, 75, home_team + ' pressing')
            for i, pres in press2home.iterrows():
                x = pres['location'][0]
                y = pres['location'][1]
                dot_size = 2
                dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
                if menu_team == home_team:
                    ax.add_patch(dot)
        elif menu_team == away_team:
            plt.text(51, 75, away_team + ' pressing')
            for i, pres in press2away.iterrows():
                x = pres['location'][0]
                y = pres['location'][1]
                dot_size = 2
                dot = plt.Circle((x, y), dot_size, color=color, alpha=0.5)
                if menu_team == away_team:
                    ax.add_patch(dot)

st.subheader('Germany vs South Korea at 2018 FIFA World Cup')
st.write('Select in the sidebar what stat you want to display')
fig.set_size_inches(10, 7)
fig.savefig('korger_shots.png', dpi=300)
st.pyplot(fig)

st.header(menu_player)

df_selection = df.query(
    'player_name == @menu_player')
df_selection1 = df_selection[df_selection.period == 1]
df_selection2 = df_selection[df_selection.period == 2]

df_pass1 = df_selection1[df_selection1.type_name == 'Pass']
df_pass2 = df_selection2[df_selection2.type_name == 'Pass']

df_shot1 = df_selection1[df_selection1.type_name == 'Shot']
df_shot2 = df_selection2[df_selection2.type_name == 'Shot']

with st.expander('Click for display all detailed player stats'):
    if menu_action == Actionpass:
        if menu_time == p1:
            st.subheader('Full pass event about selected player(1st half)')
            df_pass1
        elif menu_time == p2:
            st.subheader('Full pass event about selected player(2nd half)')
            df_pass2
    elif menu_action == Actionshot:
        if menu_time == p1:
            st.subheader('Full shot event about selected player(1st half)')
            df_shot1
        elif menu_time == p2:
            st.subheader('Full shot event about selected player(2nd half)')
            df_shot2
    else:
        if menu_time == p1:
            st.subheader('Full event list about selected player(1st half)')
            df_selection1
        elif menu_time == p2:
            st.subheader('Full event list about selected player(2nd half)')
            df_selection2

# df_selection1
# df_selection2

# def main():
# if __name__ == '__main__':
#     main()

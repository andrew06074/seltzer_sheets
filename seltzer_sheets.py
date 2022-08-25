from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64


image = Image.open('logo.png')
st.image(image)

st.write(""" - Half-point PPR rankings""")
st.write(""" - Filter to your desired scope using the sidebar""")
st.write(""" - Select players using the checkboxs for additional analysis""")

if st.checkbox('See notes'):
    
    file_ = open("tutorial.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
    st.write('Made with ag-grid & streamlit')
    st.write('Data from fantasypros and fantasydata')

draft_rankings = pd.read_csv('FantasyPros_2022_Draft_ALL_Rankings_notes.csv')
past_5_years = pd.read_csv('past_5_year.csv')

draft_rankings_raw = draft_rankings
draft_rankings = draft_rankings[['PLAYER NAME','RK','TEAM','BYE WEEK']]

draft_player_notes = draft_rankings_raw[['PLAYER NAME','NOTES']]

master_draft = pd.merge(draft_rankings,past_5_years,how='left',on='PLAYER NAME')

master_draft = master_draft[['PLAYER NAME','RK','Position','TEAM','BYE WEEK','PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]

master_draft_forag = master_draft[['PLAYER NAME','RK','Position','PPG_2021','PPG_2020','PPG_2019','PPG_2018','PPG_2017']]

master_draft_forag = master_draft_forag[['PLAYER NAME','RK','Position','PPG_2021','PPG_2020','PPG_2019','PPG_2018','PPG_2017']]
master_draft_forag.columns = ['PLAYER NAME','HPPR OVERALL RANK','POS','PPG_2021','PPG_2020','PPG_2019','PPG_2018','PPG_2017']

gb = GridOptionsBuilder.from_dataframe(master_draft_forag)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    master_draft_forag,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=375, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df


#create cols

col1, col2 = st.columns(2)

for intex, row in df.iterrows():
    with col1:
        st.subheader(row['PLAYER NAME'])

        #locate notes for selected player
        returned_search = draft_player_notes.loc[draft_player_notes['PLAYER NAME'] == row['PLAYER NAME']]
        st.write(returned_search['NOTES'].iloc[0])

    with col2:
        st.write('   ')
        st.write('   ')
        st.write('   ')
        st.write('   ')
        st.write('   ')

        #locate previous season for selected player
        return_prev_year_df = master_draft.loc[master_draft['PLAYER NAME'] ==row['PLAYER NAME']]
        return_prev_year_df = return_prev_year_df[['PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]
        player_his_data = return_prev_year_df.iloc[0]

        player_his_data = pd.DataFrame(player_his_data)
        player_his_data = player_his_data.reset_index()
        player_his_data.columns=['Season','Average PPG']
        player_his_data = player_his_data.dropna()

        career_avg = player_his_data['Average PPG'].sum() / player_his_data.shape[0]

        
        fig = px.bar(player_his_data,x='Season',y='Average PPG',width=400, height=300)
        #fig.update_traces(marker_color='blue')

        fig.add_annotation(
            text = ''
            , showarrow=False
            , x = .1
            , y = .3
            , xref='paper'
            , yref='paper' 
            , xanchor='left'
            , yanchor='top'
            , xshift=1
            , yshift=0
            , font=dict(size=14, color="black")
            , align="left"
            ,)

       

        team = master_draft.loc[master_draft['PLAYER NAME'] ==row['PLAYER NAME']]
        team = team['TEAM'].iloc[0]
        bye = master_draft.loc[master_draft['PLAYER NAME'] ==row['PLAYER NAME']]
        bye= bye['BYE WEEK'].iloc[0]

        player_str =  f"""
                <style>
                p.a {{
                font: bold 12px Courier;text-align: center;
                }}
                </style>
                <p class="a">Player: {row['PLAYER NAME']}</p>
                """
        st.markdown(player_str, unsafe_allow_html=True)


        
        team_str = f"""
                <style>
                p.a {{
                font: bold 12px Courier;text-align: center;
                }}
                </style>
                <p class="a">Team: {team}</p>
                """
        st.markdown(team_str, unsafe_allow_html=True)

        average = str(round(career_avg,2))

        avg_str = f"""
                <style>
                p.a {{
                font: bold 12px Courier;text-align: center;
                }}
                </style>
                <p class="a">Average PPG last 5 seasons: {average}</p>
                """
        st.markdown(avg_str, unsafe_allow_html=True)

        bye_str =  f"""
                <style>
                p.a {{
                font: bold 12px Courier;text-align: center;
                }}
                </style>
                <p class="a">Bye week: {bye}</p>
                """
        st.markdown(bye_str, unsafe_allow_html=True)
        st.plotly_chart(fig)
       

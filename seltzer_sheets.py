from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import base64

image = Image.open('logo.png')
st.image(image)
st.write(""" - Filter to your desired scope using the sidebar""")
st.write(""" - Select players using the checkboxs for additional analysis""")
st.write(""" - [Input league settings into BeerSheets and save generated CSV file](https://footballabsurdity.com/beersheet-request-form/)""")

if st.checkbox('Show tutorial'):
    
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

uploaded_file = st.file_uploader("Upload csv generate from BeerSheets", type="csv")

if uploaded_file is None:
    data=pd.read_csv('beer_sheet.csv')
else:
    data = pd.read_csv(uploaded_file)


notes_data = pd.read_csv('FantasyPros_2022_Draft_ALL_Rankings_notes.csv')

last_5_data = pd.read_csv('past_5_year.csv')

data = data[['Name','Pos','Rank','Tier','Tm/Bye','Average','Stdev','ECR','ECR VS. ADP','PS']]
data.columns = ['Player','Position','Rank','Tier','Team/Bye','Value','Stdev','ECR','ECR VS. ADP','Positional Saturation']

qb_df = data.loc[data['Position']=='QB']
rb_df = data.loc[data['Position']=='RB']
wr_df = data.loc[data['Position']=='WR'] 
te_df = data.loc[data['Position']=='TE']



##QB
avg_str = f"""
                <style>
                p.a {{
                font: bold 35px Courier;text-align: center;
                }}
                </style>
                <p class="a">Quarterbacks</p>
                """
st.markdown(avg_str, unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(qb_df)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    qb_df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=400, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

if not df.empty: 
    col1,col2,col3 = st.columns(3)

    with col1:
        fig = px.bar(df,x='Player',y='Value',width=300, height=200)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(df,x='Player',y='ECR VS. ADP',width=300, height=200)
        st.plotly_chart(fig)
    
    with col3:
        fig = px.bar(df,x='Player',y='Positional Saturation',width=300, height=200)
        st.plotly_chart(fig)
    
    for index,row in df.iterrows():
        player_notes = notes_data.loc[notes_data['PLAYER NAME']==row['Player']]
        st.subheader(player_notes['PLAYER NAME'].iloc[0])
        st.write(player_notes['NOTES'].iloc[0])

    df_for_vis = []
    for index,row in df.iterrows():
        last_5_scoped = last_5_data.loc[last_5_data['PLAYER NAME']==row['Player']]
        last_5_scoped = last_5_scoped[['PLAYER NAME','PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]
        last_5_scoped.columns = ['PLAYER NAME','2017','2018','2019','2020','2021']
        df_for_vis.append(last_5_scoped)
        
    df_for_vis = pd.concat(df_for_vis)
    df_for_vis_melted = df_for_vis.melt(id_vars=['PLAYER NAME'],var_name='Season',value_name='Average PPG')
    fig = px.line(df_for_vis_melted,x='Season',y='Average PPG',color='PLAYER NAME')
    st.plotly_chart(fig)


    
        

##RB
avg_str = f"""
                <style>
                p.a {{
                font: bold 35px Courier;text-align: center;
                }}
                </style>
                <p class="a">Runningbacks</p>
                """
st.markdown(avg_str, unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(rb_df)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    rb_df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=400, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

if not df.empty: 
    col1,col2,col3 = st.columns(3)

    with col1:
        fig = px.bar(df,x='Player',y='Value',width=300, height=200)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(df,x='Player',y='ECR VS. ADP',width=300, height=200)
        st.plotly_chart(fig)
    
    with col3:
        fig = px.bar(df,x='Player',y='Positional Saturation',width=300, height=200)
        st.plotly_chart(fig)

    for index,row in df.iterrows():
        player_notes = notes_data.loc[notes_data['PLAYER NAME']==row['Player']]
        st.subheader(player_notes['PLAYER NAME'].iloc[0])
        st.write(player_notes['NOTES'].iloc[0])

    df_for_vis = []
    for index,row in df.iterrows():
        last_5_scoped = last_5_data.loc[last_5_data['PLAYER NAME']==row['Player']]
        last_5_scoped = last_5_scoped[['PLAYER NAME','PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]
        last_5_scoped.columns = ['PLAYER NAME','2017','2018','2019','2020','2021']
        df_for_vis.append(last_5_scoped)
        
    df_for_vis = pd.concat(df_for_vis)
    df_for_vis_melted = df_for_vis.melt(id_vars=['PLAYER NAME'],var_name='Season',value_name='Average PPG')
    fig = px.line(df_for_vis_melted,x='Season',y='Average PPG',color='PLAYER NAME')
    st.plotly_chart(fig)

##WR
avg_str = f"""
                <style>
                p.a {{
                font: bold 35px Courier;text-align: center;
                }}
                </style>
                <p class="a">Widereceivers</p>
                """
st.markdown(avg_str, unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(wr_df)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    wr_df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=400, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

if not df.empty: 
    col1,col2,col3 = st.columns(3)

    with col1:
        fig = px.bar(df,x='Player',y='Value',width=300, height=200)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(df,x='Player',y='ECR VS. ADP',width=300, height=200)
        st.plotly_chart(fig)
    
    with col3:
        fig = px.bar(df,x='Player',y='Positional Saturation',width=300, height=200)
        st.plotly_chart(fig)
    for index,row in df.iterrows():
        player_notes = notes_data.loc[notes_data['PLAYER NAME']==row['Player']]
        st.subheader(player_notes['PLAYER NAME'].iloc[0])
        st.write(player_notes['NOTES'].iloc[0])

    df_for_vis = []
    for index,row in df.iterrows():
        last_5_scoped = last_5_data.loc[last_5_data['PLAYER NAME']==row['Player']]
        last_5_scoped = last_5_scoped[['PLAYER NAME','PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]
        last_5_scoped.columns = ['PLAYER NAME','2017','2018','2019','2020','2021']
        df_for_vis.append(last_5_scoped)
        
    df_for_vis = pd.concat(df_for_vis)
    df_for_vis_melted = df_for_vis.melt(id_vars=['PLAYER NAME'],var_name='Season',value_name='Average PPG')
    fig = px.line(df_for_vis_melted,x='Season',y='Average PPG',color='PLAYER NAME')
    st.plotly_chart(fig)

##TE
avg_str = f"""
                <style>
                p.a {{
                font: bold 35px Courier;text-align: center;
                }}
                </style>
                <p class="a">Tightends</p>
                """
st.markdown(avg_str, unsafe_allow_html=True)

gb = GridOptionsBuilder.from_dataframe(te_df)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()

grid_response = AgGrid(
    te_df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=400, 
    width='100%',
    reload_data=False
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

if not df.empty: 
    col1,col2,col3 = st.columns(3)

    with col1:
        fig = px.bar(df,x='Player',y='Value',width=300, height=200)
        st.plotly_chart(fig)

    with col2:
        fig = px.bar(df,x='Player',y='ECR VS. ADP',width=300, height=200)
        st.plotly_chart(fig)
    
    with col3:
        fig = px.bar(df,x='Player',y='Positional Saturation',width=300, height=200)
        st.plotly_chart(fig)
    for index,row in df.iterrows():
        player_notes = notes_data.loc[notes_data['PLAYER NAME']==row['Player']]
        st.subheader(player_notes['PLAYER NAME'].iloc[0])
        st.write(player_notes['NOTES'].iloc[0])

    df_for_vis = []
    for index,row in df.iterrows():
        last_5_scoped = last_5_data.loc[last_5_data['PLAYER NAME']==row['Player']]
        last_5_scoped = last_5_scoped[['PLAYER NAME','PPG_2017','PPG_2018','PPG_2019','PPG_2020','PPG_2021']]
        last_5_scoped.columns = ['PLAYER NAME','2017','2018','2019','2020','2021']
        df_for_vis.append(last_5_scoped)
        
    df_for_vis = pd.concat(df_for_vis)
    df_for_vis_melted = df_for_vis.melt(id_vars=['PLAYER NAME'],var_name='Season',value_name='Average PPG')
    fig = px.line(df_for_vis_melted,x='Season',y='Average PPG',color='PLAYER NAME')
    st.plotly_chart(fig)
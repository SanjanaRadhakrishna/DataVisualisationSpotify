# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def runApplication():
    # Use a breakpoint in the code line below to debug your script.

    st.set_page_config(layout="wide")
    df = pd.read_csv('dataset/spotify_data.csv')
    clist = df['artist'].unique()

    user = st.selectbox("Select the User:", ['Artist', 'Producer', 'Spotify User'])
    st.write("")
    if user == 'Artist':
        with st.container():
            artist = st.selectbox("Select an Artist:", clist, )
            with st.container():
                # st.header("Performance of {name}".format(name=artist))

                df1 = df[df['artist'] == artist]

                df1 = df1[['date', 'total_streams']]
                df1 = df1.groupby(['date']).sum().reset_index()

                df2 = df[["artist", "title", "total_streams"]]
                f = {'total_streams': 'sum', 'artist': 'first'}
                temp = df2.groupby(['title']).agg(f)
                temp1 = temp.loc[temp['artist'] == artist]
                sorted_df = temp1.sort_values(by=['total_streams'], ascending=False)
                df_first_10 = sorted_df.head(10)
                df_first_10_all_col = df_first_10.reset_index()
                df_first_10_all_col = df_first_10_all_col.reindex(index=df_first_10_all_col.index[::-1])

                col1, col2 = st.columns(2)

                fig = px.line(df1,
                              x="date", y="total_streams", title='Total streams of {artist} over the years:'.format(artist=artist))
                fig.update_traces(line_color='#1ED760')
                col1.plotly_chart(fig, use_container_width=True)

                fig = px.bar(df_first_10_all_col, x='total_streams', y='title', title='Top 10 songs of {artist}:'.format(artist=artist))
                fig.update_traces(marker_color='#1ED760')
                col2.plotly_chart(fig, use_container_width=True)

            with st.container():
                # st.header("Performance of {name}".format(name=artist))

                col1, col2 = st.columns(2)
                df1 = pd.DataFrame(columns=['artist', 'date', 'total_streams'])
                temp = df[df['artist'] == artist]
                temp = temp[['artist', 'date', 'total_streams']]
                f = {'total_streams': 'sum', 'artist': 'first'}
                temp = temp.groupby(['date']).agg(f).reset_index()
                df1 = df1.append(temp)

                artistList = df['artist'].unique()
                artistList = artistList[artistList != artist]
                choices = col1.multiselect('Choose artists:', artistList)
                for choice in choices:
                    temp = df[df['artist'] == choice]

                    temp = temp[['artist', 'date', 'total_streams']]
                    f = {'total_streams': 'sum', 'artist': 'first'}
                    temp = temp.groupby(['date']).agg(f).reset_index()
                    df1 = df1.append(temp)

                fig = px.line(df1,
                              x="date", y="total_streams", color='artist', title='Comparision of {artist} with other artists:'.format(artist=artist))

                col1.plotly_chart(fig, use_container_width=True)

                df3 = df[["artist", "region", "total_streams", "country_code"]]
                df3 = df3.groupby(['artist', 'country_code', 'region']).agg({'total_streams': 'sum'})
                df3 = df3.loc[artist]
                df3 = df3.reset_index()

                fig = go.Figure(data=go.Choropleth(
                    locations=df3["country_code"],
                    z=df3['total_streams'],
                    text=df3["region"],
                    colorscale=[[0, 'rgba(30, 215, 96, 0.5)'], [1, 'rgba(30, 215, 96, 1)']],
                    reversescale=False,
                    # marker_line_color='darkgray',
                    marker_line_width=0.2,
                    # colorbar_tickvals = [0.2, 0.5, 1],
                    zmin=20000000,
                    zmax=400000000,
                    colorbar_len=0.5,
                    colorbar_orientation='h',
                    colorbar_x=0.5,
                    colorbar_y=-0.2,
                    # colorbar_text_color = 'black',
                    colorbar_title='Streams Count',
                    colorbar_tickcolor='rgb(30, 215, 96)'
                    # colorbar_color = 'rgb(255,255,255)'
                    # colorbar_title_color = 'rgb(30, 215, 96)'
                ))

                fig.update_layout(
                    title_text='Stream count of {artist} in various countries:'.format(artist=artist),
                    font=dict(
                        family="Verdana",
                        color="white"
                    ),
                    height=600,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    geo=dict(
                        bgcolor='rgb(0,0,0,0)',
                        showframe=False,
                        showcoastlines=False,
                        landcolor='black',
                        showcountries=True,
                        countrycolor='gray',
                        countrywidth=0.5
                    )
                )

                col2.plotly_chart(fig, use_container_width=True)
    if user == 'Producer':
        with st.container():
            with st.container():
                col1, col2 = st.columns(2)
                choices = col1.multiselect('Choose artists:', df['artist'].unique(), default= None)
                df1 = pd.DataFrame(columns=['artist', 'date', 'total_streams'])
                for choice in choices:
                    temp = df[df['artist'] == choice]

                    temp = temp[['artist', 'date', 'total_streams']]
                    f = {'total_streams': 'sum', 'artist': 'first'}
                    temp = temp.groupby(['date']).agg(f).reset_index()
                    df1 = df1.append(temp)

                fig = px.line(df1,
                              x="date", y="total_streams", color='artist', title='Comparision of selected artists:')

                col1.plotly_chart(fig, use_container_width=True)

                df1 = df[["region", "total_streams", "country_code"]]
                df1 = df1.groupby(['country_code', 'region']).agg({'total_streams': 'sum'})
                df1 = df1.reset_index()

                fig = go.Figure(data=go.Choropleth(
                    locations=df1["country_code"],
                    z=df1['total_streams'],
                    text=df1["region"],
                    colorscale=[[0, 'rgba(30, 215, 96, 0.5)'], [1, 'rgba(30, 215, 96, 1)']],
                    reversescale=False,
                    marker_line_width=0.2,
                    zmin=60000000,
                    zmax=12000000000,
                    colorbar_len=0.5,
                    colorbar_orientation='h',
                    colorbar_x=0.5,
                    colorbar_y=-0.2,
                    colorbar_title='No. of Streams',
                    colorbar_tickcolor='rgb(30, 215, 96)'
                ))

                fig.update_layout(
                    title_text='Spotify global stream count:',
                    font=dict(
                        family="Verdana",
                        color="white"
                    ),
                    height=600,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    geo=dict(
                        bgcolor='rgb(0,0,0,0)',
                        showframe=False,
                        showcoastlines=False,
                        landcolor='black',
                        showcountries=True,
                        countrycolor='gray',
                        countrywidth=0.5
                    )
                )

                col2.plotly_chart(fig, use_container_width=True)

            with st.container():
                col1, col2 = st.columns(2)

                col1.write("")
                col1.write("")
                col1.markdown("Top **100** artists:")
                col1.image('figures/wordCloud.png', use_column_width=True)


                df1 = df[["artist", "region", "total_streams", "country_code"]]
                qn = df1.sort_values(['total_streams']).groupby(['country_code'], sort=False)['artist'].unique()
                qn2 = df1.sort_values(['total_streams']).groupby(['region'], sort=False)['artist'].unique()
                df1 = df1.sort_values(['total_streams']).groupby(['country_code'], sort=False)['artist'].unique()
                for i, v in df1.items():
                    qn[i] = v[0]

                list1 = qn.values.tolist()
                list2 = qn2.index.to_list()
                res = [i + ':\n ' + j for i, j in zip(list2, list1)]

                fig = go.Figure(data=go.Choropleth(
                    locations=qn.index.to_list(),
                    z=[100] * 69,
                    text=res,
                    colorscale=[[0, 'rgba(30, 215, 96, 0.5)'], [1, 'rgba(30, 215, 96, 1)']],
                    reversescale=False,
                    marker_line_width=0.2,
                    zmin=0,
                    zmax=100
                ))

                fig.update_traces(
                    hoverinfo='text',
                    showscale=False
                )

                fig.update_layout(
                    title_text='Top artist in each country:',
                    font=dict(
                        family="Verdana",
                        color="white"
                    ),
                    height=600,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    geo=dict(
                        bgcolor='rgb(0,0,0,0)',
                        showframe=False,
                        showcoastlines=False,
                        landcolor='black',
                        showcountries=True,
                        countrycolor='gray',
                        countrywidth=0.5
                    )
                )

                col2.plotly_chart(fig, use_container_width=True)
    if user == 'Spotify User':
        with st.container():
            with st.container():
                col1, col2 = st.columns(2)
                artist = col1.selectbox("Select an Artist:", clist, )
                df2 = df[["artist", "title", "total_streams"]]
                f = {'total_streams': 'sum', 'artist': 'first'}
                temp = df2.groupby(['title']).agg(f)
                temp1 = temp.loc[temp['artist'] == artist]
                sorted_df = temp1.sort_values(by=['total_streams'], ascending=False)
                df_first_10 = sorted_df.head(10)
                df_first_10_all_col = df_first_10.reset_index()
                df_first_10_all_col = df_first_10_all_col.reindex(index=df_first_10_all_col.index[::-1])
                fig = px.bar(df_first_10_all_col, x="total_streams", y='title', title='Top 10 songs of {artist}:'.format(artist=artist))
                fig.update_traces(marker_color='#1ED760')
                col1.plotly_chart(fig, use_container_width=True)

                df1 = df[["artist", "region", "total_streams", "country_code"]]
                qn = df1.sort_values(['total_streams']).groupby(['country_code'], sort=False)['artist'].unique()
                qn2 = df1.sort_values(['total_streams']).groupby(['region'], sort=False)['artist'].unique()
                df1 = df1.sort_values(['total_streams']).groupby(['country_code'], sort=False)['artist'].unique()
                for i, v in df1.items():
                    qn[i] = v[0]

                list1 = qn.values.tolist()
                list2 = qn2.index.to_list()
                res = [i + ':\n ' + j for i, j in zip(list2, list1)]

                fig = go.Figure(data=go.Choropleth(
                    locations=qn.index.to_list(),
                    z=[100] * 69,
                    text=res,
                    colorscale=[[0, 'rgba(30, 215, 96, 0.5)'], [1, 'rgba(30, 215, 96, 1)']],
                    reversescale=False,
                    marker_line_width=0.2,
                    zmin=0,
                    zmax=100
                ))

                fig.update_traces(
                    hoverinfo='text',
                    showscale=False
                )

                fig.update_layout(
                    title_text='Top artist in each country:',
                    font=dict(
                        family="Verdana",
                        color="white"
                    ),
                    height=600,
                    plot_bgcolor='black',
                    paper_bgcolor='black',
                    geo=dict(
                        bgcolor='rgb(0,0,0,0)',
                        showframe=False,
                        showcoastlines=False,
                        landcolor='black',
                        showcountries=True,
                        countrycolor='gray',
                        countrywidth=0.5
                    )
                )

                col2.plotly_chart(fig, use_container_width=True)

            with st.container():
                col1, col2 = st.columns(2)
                col1.write("")
                col1.write("")
                col1.markdown("Top **100** artists:")
                col1.image('figures/wordCloud.png', use_column_width=True)

                df1 = df[["artist", "title", "total_streams"]]
                f = {'total_streams': 'sum'}
                df1 = df1.groupby(['title']).agg(f)

                df1 = df1.sort_values(by=['total_streams'], ascending=False)
                df_first_10 = df1.head(10)
                df_first_10_all_col = df_first_10.reset_index()
                df_first_10_all_col = df_first_10_all_col.reindex(index=df_first_10_all_col.index[::-1])
                fig = px.bar(df_first_10_all_col, x="total_streams", y='title',title='Top 10 songs of all time:')
                fig.update_traces(marker_color='#1ED760')
                col2.plotly_chart(fig, use_container_width=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runApplication()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

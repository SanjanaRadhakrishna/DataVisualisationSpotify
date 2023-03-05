import pandas as pd
import wordcloud as w
import matplotlib.pyplot as plt
import streamlit as st

df = pd.read_csv('dataset/spotify_data.csv')
df1 = df[["artist", "title", "total_streams"]]
f = {'total_streams': 'sum'}
temp = df1.groupby(['artist']).agg(f)

sorted_df = temp.sort_values(by=['total_streams'], ascending=False)
sorted_df_artists = sorted_df.reset_index()
d = dict(zip(sorted_df_artists['artist'], sorted_df_artists['total_streams']))
wc = w.WordCloud(background_color="black", collocations=False, relative_scaling=1, random_state=1,
                 width=3000, height=2000, colormap="summer").generate_from_frequencies(d)

plt.figure(figsize=[5, 5], facecolor='k')
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.tight_layout(pad=0)
st.pyplot(plt, use_container_width=True)
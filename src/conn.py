import streamlit as st
import joblib
import pandas as pd 
import numpy as np 
import os
import glob
import plotly.express as px
from sklearn.preprocessing import StandardScaler

from search_song import *
from feature_extract_helper import *
import SessionState

session_state = SessionState.get(checkboxed = False)
session_state1 = SessionState.get(checkboxed = False)
session_state2 = SessionState.get(checkboxed = False)


os.chdir(os.getcwd())

song_df = pd.read_csv("src/data/song_df.csv")

song_features = pd.read_csv("src/data/song_features.csv")

SVR_model = joblib.load("models/SVR_model1.pkl")

scaler = joblib.load("models/scaler2.pkl")


st.title("MoodZen")


st.sidebar.image("images/astromusic.jpg",width=250)

song_name = st.sidebar.text_input("Enter Song Name")
artist_name = st.sidebar.text_input("Enter Arists Name (Optional)", '')



if st.sidebar.button("Get Recommendations") or session_state.checkboxed:

    session_state.checkboxed = True
    try:
        song_id, track_name, track_artist, song_url, valence, energy = search_new_song(song_name,artist_name=artist_name)
        st.write("Song Successfully Retrived!")
        col1, col2 = st.beta_columns(2)
        col1.write("Track : ")

        col1.markdown("<a href="+str(song_url)+" target='_blank' style='text-align: center;'>"+ str(track_name) + ' by ' +str(track_artist)+"</a>", unsafe_allow_html=True)
        col2.audio("src/data/temp_music/"+song_id+".wav")


        if song_id in song_df['id'].tolist():
            ratings = list(song_df[song_df['id'] == song_id][['Anger','Sad','Happy','Tender']].values[0])
        
        else: 
            
            features = extract_feature('src/data/temp_music/')
            song_features.append(features)
            features.drop(columns = ['song_name'], inplace = True)

            features['energy'] = energy
            features['valence'] = valence
            features = scaler.transform(features)

            ratings = SVR_model.predict(features)[0]
            
            song_df.loc[len(song_df)] = [track_name, track_artist, 1, ratings[0], ratings[1], ratings[2], ratings[3], energy, valence, song_url, song_id, 1]
            
            song_df.to_csv('src/data/song_df.csv', index = False)

        radar_df = pd.DataFrame(dict(
            r= ratings,
            theta=['Anger','Sad','Happy','Tender']))

        st.subheader("Emotional Ratings")
        fig = px.line_polar(radar_df, r='r', range_r=[0,5], theta='theta', line_close=True)
        st.plotly_chart(fig)

        angry_col, sad_col, happy_col, tender_col = st.beta_columns(4)
        angry_col.markdown("<h1 style='text-align: center;'> &#128544 </h1>", unsafe_allow_html=True)
        angry_col.markdown("<h3 style='text-align: center;'>"+str(np.round(ratings[0],2))+"</h3>", unsafe_allow_html=True)

        sad_col.markdown("<h1 style='text-align: center;'> &#128557 </h1>", unsafe_allow_html=True)
        sad_col.markdown("<h3 style='text-align: center;'>"+str(np.round(ratings[1],2))+"</h3>", unsafe_allow_html=True)

        happy_col.markdown("<h1 style='text-align: center;'> &#128513 </h1>", unsafe_allow_html=True)
        happy_col.markdown("<h3 style='text-align: center;'>"+str(np.round(ratings[2],2))+"</h3>", unsafe_allow_html=True)

        tender_col.markdown("<h1 style='text-align: center;'> &#128524 </h1>", unsafe_allow_html=True)
        tender_col.markdown("<h3 style='text-align: center;'>"+str(np.round(ratings[3],2))+"</h3>", unsafe_allow_html=True)


        st.write(" ")
        check = st.radio("Are these emotional ratings what you expected them to be?", ('Yes', 'No'))

        def cos_sim(a, b=ratings):

            """
        Takes 2 vectors a, b and returns the cosine similarity according 
            to the definition of the dot product
            """
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            return dot_product / (norm_a * norm_b)

        if check == "No" :

            #session_state1.checkboxed = True

            st.write("Please enter what you expected from this song. Our model improves with your help.")
            angry_col1, sad_col1, happy_col1, tender_col1 = st.beta_columns(4)

            angry_val = angry_col1.text_input("Angry Rating", " ")
            ratings[0] = (ratings[0] + float(angry_val))/2.0

            sad_val = sad_col1.text_input("Sad Rating", " ")
            ratings[1] =  (ratings[1] + float(sad_val))/2.0
            
            happy_val = happy_col1.text_input("Happy Rating", " ")
            ratings[2] =  (ratings[2] + float(happy_val))/2.0


            tender_val = tender_col1.text_input("Tender Rating", " ")
            ratings[3] =  (ratings[3] + float(tender_val))/2.0

            # if st.button or session_state2.checkboxed:
            #     session_state2.checkboxed = True

            #     if " " not in (angry_val, sad_val, happy_val, tender_val) :
            #         ratings[0] = (ratings[0] + float(angry_val))/2.0
            #         ratings[1] =  (ratings[1] + float(angry_val))/2.0
            #         ratings[2] =  (ratings[2] + float(angry_val))/2.0
            #         ratings[3] =  (ratings[3] + float(angry_val))/2.0

            
            song_df['similarity_score'] = song_df[['Anger', 'Sad', 'Happy', 'Tender']].apply(lambda x: cos_sim(x),axis=1)
            song_df1 = song_df.copy()
            song_df1 = song_df[song_df1["id"]!=song_id]
            song_df1[['Anger', 'Sad', 'Happy', 'Tender']] = song_df1[['Anger', 'Sad', 'Happy', 'Tender']].apply(lambda x:np.round(x,2),axis=1)

            links = song_df1.sort_values('similarity_score',ascending=False).head(10)['song_url'].tolist()
            
            songs_1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Song Name'].tolist()
            artists_1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Artist'].tolist()

            rat = song_df1.sort_values('similarity_score',ascending=False).head(10)['Anger'].tolist()
            rat1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Sad'].tolist()
            rat2 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Happy'].tolist()
            rat3 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Tender'].tolist()
            frequen = song_df1.sort_values('similarity_score',ascending=False).head(10)['update_frequency'].tolist()

            head_1,head_2,head_3,head_4,head_5,head_6,freq = st.beta_columns(7)
            head_1.markdown("<h4 style='text-align: center;'>"+str('Track')+"</h4>", unsafe_allow_html=True)
            head_2.markdown("<h4 style='text-align: center;'>"+str('Artist')+"</h4>", unsafe_allow_html=True)
            head_3.markdown("<h4 style='text-align: center;'>"+str('Anger')+"</h4>", unsafe_allow_html=True)
            head_4.markdown("<h4 style='text-align: center;'>"+str('Sad')+"</h4>", unsafe_allow_html=True)
            head_5.markdown("<h4 style='text-align: center;'>"+str('Happy')+"</h4>", unsafe_allow_html=True)
            head_6.markdown("<h4 style='text-align: center;'>"+str('Tender')+"</h4>", unsafe_allow_html=True)
            freq.markdown("<h4 style='text-align: center;'>"+str('Updated Freq')+"</h4>", unsafe_allow_html=True)
            st.write('')
            
            l = locals()
            for i in range(10):
                l['song_'+str(i)],l['artist_'+str(i)],l['rat_'+str(i)],l['rat1_'+str(i)],l['rat2_'+str(i)],l['rat3_'+str(i)],l['freq1_'+str(i)] = st.beta_columns(7)

                l['song_'+str(i)].markdown("<a href="+str(links[i])+" target='_blank' style='text-align: center;'>"+ str(songs_1[i])+"</a>", unsafe_allow_html=True)
                
                l['artist_'+str(i)].markdown("<body style='text-align: center;'>"+str(artists_1[i])+"</body>", unsafe_allow_html=True)

                l['rat_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat[i])+"</body>", unsafe_allow_html=True)

                l['rat1_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat1[i])+"</body>", unsafe_allow_html=True)
            
                l['rat2_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat2[i])+"</body>", unsafe_allow_html=True)

                l['rat3_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat3[i])+"</body>", unsafe_allow_html=True)

                l['freq1_'+str(i)].markdown("<body style='text-align: center;'>"+str(frequen[i])+"</body>", unsafe_allow_html=True)
                st.write("")
            song_df.loc[song_df['id']==song_id,'update_frequency']+=1

                

        if check=='Yes':
            st.subheader("Similar Songs")
            st.write("Top 10 songs based on how similar they are to the emotions of searched song.")
            st.write(" ")

            song_df['similarity_score'] = song_df[['Anger', 'Sad', 'Happy', 'Tender']].apply(lambda x: cos_sim(x),axis=1)
            song_df1 = song_df.copy()
            song_df1 = song_df[song_df1["id"]!=song_id]
            song_df1[['Anger', 'Sad', 'Happy', 'Tender']] = song_df1[['Anger', 'Sad', 'Happy', 'Tender']].apply(lambda x:np.round(x,2),axis=1)
            frequen = song_df1.sort_values('similarity_score',ascending=False).head(10)['update_frequency'].tolist()

            links = song_df1.sort_values('similarity_score',ascending=False).head(10)['song_url'].tolist()
            songs_1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Song Name'].tolist()
            artists_1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Artist'].tolist()

            rat = song_df1.sort_values('similarity_score',ascending=False).head(10)['Anger'].tolist()
            rat1 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Sad'].tolist()
            rat2 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Happy'].tolist()
            rat3 = song_df1.sort_values('similarity_score',ascending=False).head(10)['Tender'].tolist()

            head_1,head_2,head_3,head_4,head_5,head_6,freq = st.beta_columns(7)
            head_1.markdown("<h4 style='text-align: center;'>"+str('Track')+"</h4>", unsafe_allow_html=True)
            head_2.markdown("<h4 style='text-align: center;'>"+str('Artist')+"</h4>", unsafe_allow_html=True)
            head_3.markdown("<h4 style='text-align: center;'>"+str('Anger')+"</h4>", unsafe_allow_html=True)
            head_4.markdown("<h4 style='text-align: center;'>"+str('Sad')+"</h4>", unsafe_allow_html=True)
            head_5.markdown("<h4 style='text-align: center;'>"+str('Happy')+"</h4>", unsafe_allow_html=True)
            head_6.markdown("<h4 style='text-align: center;'>"+str('Tender')+"</h4>", unsafe_allow_html=True)
            freq.markdown("<h4 style='text-align: center;'>"+str('Updated Freq')+"</h4>", unsafe_allow_html=True)
            st.write('')
            
            l = locals()
            for i in range(10):
                l['song_'+str(i)],l['artist_'+str(i)],l['rat_'+str(i)],l['rat1_'+str(i)],l['rat2_'+str(i)],l['rat3_'+str(i)],l['freq1_'+str(i)] = st.beta_columns(7)

                l['song_'+str(i)].markdown("<a href="+str(links[i])+" target='_blank' style='text-align: center;'>"+ str(songs_1[i])+"</a>", unsafe_allow_html=True)
                
                l['artist_'+str(i)].markdown("<body style='text-align: center;'>"+str(artists_1[i])+"</body>", unsafe_allow_html=True)

                l['rat_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat[i])+"</body>", unsafe_allow_html=True)

                l['rat1_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat1[i])+"</body>", unsafe_allow_html=True)
            
                l['rat2_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat2[i])+"</body>", unsafe_allow_html=True)

                l['rat3_'+str(i)].markdown("<body style='text-align: center;'>"+str(rat3[i])+"</body>", unsafe_allow_html=True)

                l['freq1_'+str(i)].markdown("<body style='text-align: center;'>"+str(frequen[i])+"</body>", unsafe_allow_html=True)
                st.write('')
            
        song_df.drop(columns = ['similarity_score'], inplace = True)
        song_df.to_csv('src/data/song_df.csv', index = False)
        song_features.to_csv('src/data/song_features.csv', index = False)
        files = glob.glob('src/data/temp_music/*')
        for f in files:
            os.remove(f)


    except:

        if search_new_song(song_name,artist_name = artist_name) != "Song Cannot Be Downloaded Using Spotify API":
            pass
        else:
            st.write("Song Cannot Be Downloaded Using Spotify API")


else:
    st.subheader("About This App")
    st.markdown("Welcome to MoodZen! This project is a music recommendation engine that takes into account the emotions that a particular song evokes. Emotions associated with a song are an abstract concept and can be subjective, that's why our system allows you to update the representation of emotion associated with each song that our model predicted. Over time, as more people use this web app, the model performance will improve and give emotion predictions that are closer to ground truth (or at least what majority of people believe the emotional ratings of songs to be).") 

    st.markdown("For our emotion prediction, we use a Support Vector Regressor (SVR). We predict four emotions:")
    st.markdown('- Anger')
    st.markdown('- Sadness')
    st.markdown('- Happiness')
    st.markdown('- Tenderness')

    st.markdown('Our predictions are a numerical representation of the particular emotion ranging from 1-5. (For example, a song with an anger rating of 4 would probably evoke anger in the listener.) The predictions are purely based on the audio features of the song, **NOT on the lyrics**, extracted using the python library Librosa.')

    st.markdown('The search engine we used is based on Spotify API. Currently we can only give recommendations based on songs that we can download audio snippets of, using the Spotify API, but if a song cannot be downloaded or found, our recommendation system does not support that (12.2.2020).')

    st.markdown('Please feel free to play with our recommendation system, we are very proud of it :)')

    st.markdown('(It will also get better the more you use it ;))")')
    st.subheader("Dataset")
    st.markdown('-- As of 12.2.2020 --')

    st.markdown('The recommendations we will provide are based on the dataset of songs and their emotional features that we have collected. This dataset has been curated by using Spotify’s Top 100 Listened to songs and the ratings associated with them have been measured by our team members.')

    st.markdown('The dataset will update as you search for songs that are not in the dataset and also will update when you are not satisfied with the predictions associated with a particular song.  ')

    st.markdown('We have two main datasets (You can find these in the repository of the project). ')
    st.markdown('One dataset (song_df.csv) consists of songs and their emotional ratings.')
    st.markdown('Another dataset, consists of songs and the features that we extracted from them. ')
    st.subheader("Links")
    st.markdown('GitHub Repository : https://github.com/shaswat01/MoodZen')

    st.markdown('Data Link :  https://github.com/shaswat01/MoodZen/tree/main/src/data ')
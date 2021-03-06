# MoodZen

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/shaswat01/moodzen/main/src/conn.py)

## About This App
Welcome to MoodZen! This project is a music recommendation engine that takes into account the emotions that a particular song evokes. Emotions associated with a song are an abstract concept and can be subjective, that's why our system allows you to update the representation of emotion associated with each song that our model predicted. Over time, as more people use this web app, the model performance will improve and give emotion predictions that are closer to ground truth (or at least what majority of people believe the emotional ratings of songs to be). 

For our emotion prediction, we use a Support Vector Regressor (SVR). We predict four emotions:
- Anger
- Sadness
- Happiness
- Tenderness

Our predictions are a numerical representation of the particular emotion ranging from 1-5. (For example, a song with an anger rating of 4 would probably evoke anger in the listener.) The predictions are purely based on the audio features of the song, **NOT on the lyrics**, extracted using the python library Librosa.

The search engine we used is based on Spotify API. Currently we can only give recommendations based on songs that we can download audio snippets of, using the Spotify API, but if a song cannot be downloaded or found, our recommendation system does not support that (12.2.2020). 

Please feel free to play with our recommendation system, we are very proud of it :)

(It will also get better the more you use it ;))

## Dataset
-- As of 12.2.2020 --

The recommendations we will provide are based on the dataset of songs and their emotional features that we have collected. This dataset has been curated by using Spotify’s Top 100 Listened to songs and the ratings associated with them have been measured by our team members.

The dataset will update as you search for songs that are not in the dataset and also will update when you are not satisfied with the predictions associated with a particular song.  

We have two main datasets (You can find these in the repository of the project). 
One dataset (song_df.csv) consists of songs and their emotional ratings.
Another dataset, consists of songs and the features that we extracted from them. 

### Link

GitHub Repository : https://github.com/shaswat01/MoodZen

Data Link :  https://github.com/shaswat01/MoodZen/tree/main/src/data 

Project Organization
------------

    ├── LICENSE
    ├── README.md         
    ├── src
    │   ├── data       
    │   ├── conn.py     
    │   ├── feature_extract_helper.py 
    │   ├── search_song.py   
    │   └── spotify_api.py
    ├── models
    │   ├── SVR_model1.pkl  
    │   ├── ridge_model.pkl   
    │   └── scaler2.pkl
    ├── notebooks          
    ├── images        
    ├── Aptfile
    ├── requirements.txt   
    ├── setup.sh                     
    └── packages.txt 


--------

# MoodZen

You can play with this app [here](https://share.streamlit.io/shaswat01/moodzen/main/src/conn.py). 

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
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

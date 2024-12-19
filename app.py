import numpy as np
import pandas as pd
import pickle
import requests
import streamlit as st
import random


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2159c514a5bcc21db18586a72678830f&language=en-US')
        data = response.json()

        
        if response.status_code != 200:
            st.error(f"Error fetching movie data: {data.get('status_message', 'Unknown error')}")
            return "https://via.placeholder.com/200x300?text=Error+Fetching+Poster"

        
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/200x300?text=No+Poster+Available"
    except Exception as e:
        print(f"Error fetching poster: {e}")  # Debugging output
        return "https://via.placeholder.com/200x300?text=Error+Fetching+Poster"



with open('movie_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)

movies = pd.DataFrame.from_dict(movies_dict)

with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

movies_list = movies['title'].values


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_indices = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_ids = []
    for i in movie_indices:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_ids.append(movies.iloc[i[0]].id)

    return recommended_movies, recommended_movie_ids



st.set_page_config(page_title='Movie Recommender System', layout='wide')
st.title('🎬 Movie Recommender System')


st.markdown(
    """
    <style>
    .reportview-container {
        background: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


random_movie_index = random.randint(0, len(movies_list) - 1)
random_movie_title = movies_list[random_movie_index]
random_movie_id = movies.iloc[random_movie_index].id


st.header(f"✨ Featured Movie: {random_movie_title}")
st.image(fetch_poster(random_movie_id), width=200)


selected_movie = st.selectbox('🎥 Select a movie:', movies_list.tolist())


if st.button('🔍 Recommend', key='recommend'):
    names, movie_ids = recommend(selected_movie)

   
    cols = st.columns(5)
    for col, name, movie_id in zip(cols, names, movie_ids):
        with col:
            
            print(f"Fetching poster for movie ID: {movie_id}")
            poster_url = fetch_poster(movie_id)
            st.image(poster_url, width=200)
            st.markdown(f"<h5 style='text-align: center;'>{name}</h5>", unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #007BFF;
        color: white;
        font-size: 20px;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

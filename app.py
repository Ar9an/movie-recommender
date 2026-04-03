import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ------------------ DOWNLOAD FILE FUNCTION (FIXED FOR LARGE FILES) ------------------ #
def download_file(url, filename):
    if not os.path.exists(filename):
        with st.spinner(f"Downloading {filename}..."):
            session = requests.Session()

            response = session.get(url, stream=True)

            # Handle large file confirmation (Google Drive)
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    url = url + "&confirm=" + value

            response = session.get(url, stream=True)

            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    if chunk:
                        f.write(chunk)

# ------------------ GOOGLE DRIVE LINKS ------------------ #
MOVIE_DICT_URL = "https://drive.google.com/uc?export=download&id=1612A2FzoBgaD2yYaUkRuBAZGVQamkc85"
SIMILARITY_URL = "https://drive.google.com/uc?export=download&id=1CJDlry_DgLArxMZCY-EW813mbY0Shk4r"

# ------------------ DOWNLOAD FILES BEFORE LOADING ------------------ #
download_file(MOVIE_DICT_URL, "movie_dict.pkl")
download_file(SIMILARITY_URL, "similarity.pkl")

# ------------------ LOAD DATA ------------------ #
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------ FETCH POSTER ------------------ #
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=5992fc7c017821dc1e193d7c8d27c31e&language=en-US'
        data = requests.get(url).json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"

# ------------------ RECOMMEND FUNCTION ------------------ #
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ------------------ STREAMLIT UI ------------------ #
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.title('🎬 Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

# ------------------ BUTTON ------------------ #
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
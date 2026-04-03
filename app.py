import streamlit as st
import pickle
import pandas as pd
import requests
import os


# ------------------ ROBUST DOWNLOAD FUNCTION ------------------ #
def download_file(url, filename):
    if not os.path.exists(filename):
        with st.spinner(f"Downloading {filename}..."):
            try:
                session = requests.Session()

                response = session.get(url, stream=True)

                # Handle Google Drive large file confirmation
                token = None
                for key, value in response.cookies.items():
                    if key.startswith("download_warning"):
                        token = value

                if token:
                    url = url + "&confirm=" + token
                    response = session.get(url, stream=True)

                with open(filename, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

                # Debug file size
                file_size = os.path.getsize(filename)
                st.write(f"{filename} downloaded ({file_size / (1024 * 1024):.2f} MB)")

                # If file too small → likely failed download
                if file_size < 1000000:  # <1MB
                    st.error(f"{filename} download failed (too small). Try Dropbox link.")

            except Exception as e:
                st.error(f"Error downloading {filename}: {e}")


# ------------------ FILE LINKS ------------------ #

# Google Drive links (primary)
MOVIE_DICT_URL = "https://www.dropbox.com/scl/fi/q7l0wa9cxo9n20g8qq7lf/movie_dict.pkl?rlkey=qm76eaw0lek8hys1b45momnq6&dl=1"

SIMILARITY_URL = "https://www.dropbox.com/scl/fi/c23zkap8igie90f64e2g2/similarity.pkl?rlkey=skboelkhvt9a8m68rr9mubu2h&dl=1"

# ------------------ DOWNLOAD FILES ------------------ #
download_file(MOVIE_DICT_URL, "movie_dict.pkl")
download_file(SIMILARITY_URL, "similarity.pkl")

# ------------------ CHECK FILE EXISTS ------------------ #
if not os.path.exists("similarity.pkl") or not os.path.exists("movie_dict.pkl"):
    st.error("Data files not loaded properly.")
    st.stop()

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
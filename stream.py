import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=201dadbac9d90432aa44713682a9eb60&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']



movies_list = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        #fetch the movie poster
        recommend_movies.append(movies.iloc[i[0]].title)
        #fetches the poster from API
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_poster

selected_movie_name = st.selectbox(
    'How you doing ?',
    movies['title'].values
    )
if st.button('Recommend'):
    name,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])
    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])



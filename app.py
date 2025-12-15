import streamlit as st
import pickle
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

# ---------------- FUNCTIONS ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ---------------- UI ----------------

# HERO SECTION
st.markdown(
    """
    <h1 style='text-align:center;'>🎬 AI Movie Recommendation System</h1>
    <p style='text-align:center; color:gray;'>
    Content-Based Filtering using Unsupervised Learning
    </p>
    """,
    unsafe_allow_html=True
)

st.write("")

# SEARCH BAR
movie_list = movies["title"].values
selected_movie = st.selectbox(
    "Search or select a movie you like",
    movie_list
)

# BUTTON
if st.button("🎥 Recommend Movies"):
    names, posters = recommend(selected_movie)

    st.write("")
    st.subheader("✨ Recommended Movies for You")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"**{names[i]}**")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Project Details")
st.sidebar.write("**Project Type:** Movie Recommendation System")
st.sidebar.write("**Learning Type:** Unsupervised Learning")
st.sidebar.write("**Algorithm:** Cosine Similarity")
st.sidebar.write("**Vectorization:** CountVectorizer")
st.sidebar.write("**Dataset:** TMDB 5000 Movies")
st.sidebar.write("**Frontend:** Streamlit")

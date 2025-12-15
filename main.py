from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models (ensure movie_list.pkl and similarity.pkl are in this folder)
movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_titles = movies['title'].tolist()

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/recommend")
def recommend(movie: str):
    movie = movie.lower().strip()
    movie_titles_lower = [m.lower() for m in movie_titles]

    if movie not in movie_titles_lower:
        raise HTTPException(status_code=404, detail="Movie not found")

    index = movie_titles_lower.index(movie)
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_titles = []
    recommended_ids = []
    posters = []

    for idx, _ in distances:
        recommended_titles.append(movies.iloc[idx].title)
        recommended_ids.append(int(movies.iloc[idx].movie_id))
        posters.append("")

    return {
        "titles": recommended_titles,
        "ids": recommended_ids,
        "posters": posters
    }

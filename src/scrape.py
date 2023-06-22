import os
import requests
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from projects import FilmProject, Person

load_dotenv(find_dotenv())

API_READ_ACCESS_TOKEN = os.environ.get("API_READ_ACCESS_TOKEN")
UPCOMING_MOVIES_URL = "https://api.themoviedb.org/3/discover/movie"
DATE_TODAY = datetime.today().date()

HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_READ_ACCESS_TOKEN}"
}

params = {
    "include_adult": False,
    "include_video": False,
    "language": "en-US",
    "sort_by": "popularity.desc",
    "primary_release_date.gte": DATE_TODAY,  # Release data greater than today's date (YYYY-MM-DD)
    "with_crew": "Guy Ritchie"  # Replace with the specific director's name
}

response = requests.get(UPCOMING_MOVIES_URL, params=params, headers=HEADERS)

data = response.json()  # Parse the JSON response

if response.status_code == 200:
    # Example: Extracting movie titles and release dates
    movies = data["results"]
    for movie in movies:
        title = movie["title"]
        release_date = movie["release_date"]
        print(f"Title: {title}, Release Date: {release_date}")
else:
    print(f"Error: {data['status_message']}")

import os
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from bs4 import BeautifulSoup

class UserPreferences:
    def __init__(self):
        self._directors = []
        self._actors = []

    def update_directorlist(self):
        """Checks the online notepad for the latest version of a list of directors and updates the internal list in the class"""

        directorlist_url = os.environ.get("DIRECTORLIST_URL")

        response = requests.get(directorlist_url)
        soup = BeautifulSoup(response.content, features="html.parser")

        # Find the textarea and append all directors to the list
        directors_string = soup.find("div", {"class":"plaintext"}).text
        for director in directors_string.split("\n"):
            if director != "":
                self._directors.append(director)

    def get_directors(self):
        """Returns a list of director names"""
        return self._directors

    def update_actorlist(self):
        """Checks the online notepad for the latest version of a list of actors and updates the internal list in the class"""

        actorlist_url = os.environ.get("ACTORLIST_URL")

        response = requests.get(actorlist_url)
        soup = BeautifulSoup(response.content, features="html.parser")

        # Find the textarea and append all actors to the list
        actors_string = soup.find("div", {"class":"plaintext"}).text
        for actor in actors_string.split("\n"):
            if actor != "":
                self._actors.append(actor)

    def get_actors(self):
        """Returns a list of actor names"""
        return self._actors


if __name__ == "__main__":
    user = UserPreferences()

    # user.update_actorlist()
    # print("Actors from aNotepad:")
    # [print(actor) for actor in user.get_actors()]
    
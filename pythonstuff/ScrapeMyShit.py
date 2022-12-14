from bs4 import BeautifulSoup
import re

###################
#### CONSTANTS ####

#### URLs #########
IMDB_URL = "https://imdb.com"
IMDB_LOGIN_URL = "https://www.imdb.com/ap/signin"

## END CONSTANTS ##
###################

class Scraper:

    def __init__(self, session):
        self._session = session

    def get_IMDb_page_link(self, name_url_ready:str):
        """Searches for the name on IMDb and returns a link to their IMDb page"""

        response = self._session.post(f"{IMDB_URL}/find?q={name_url_ready}&ref_=nv_sr_sm")
        soup = BeautifulSoup(response.text, features="html.parser")
        unique_link = soup.find("a", {"href":re.compile(r"/name/nm")})['href']

        name_link = f"{IMDB_URL}{unique_link}"

        return name_link

    def get_director_projects(self, director_url:str):
        """Looks for projects in production on a director's IMDb page and returns the projects as a dictionary with titles and links"""
        project_dict = {"titles":[], "links":[]}

        directorpage = self._session.get(director_url)
        soup = BeautifulSoup(directorpage.text, "html.parser")

        director_element = soup.find("div", id="filmo-head-director")
        director_credits_element = director_element.find_next_sibling("div") # finds all the productions directed by the current director
        in_production_tags = director_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released

        if not in_production_tags: # director has no upcoming projects :(
            return None

        for tag in in_production_tags:
            if tag.text != "abandoned": # IMDb classifies abondoned productions with the same "in_production" html class smh..
                project_element = tag.find_parent("div")
                
                title = project_element.b.a.text
                link = project_element.b.a["href"]

                project_dict["titles"].append(title)
                project_dict["links"].append(f"{IMDB_URL}{link}")
        
        return project_dict

    def get_actor_projects(self, actor_url:str):
        """Looks for projects in production on an actor's IMDb page and returns the projects as a dictionary with titles and links"""
        project_dict = {"titles":[], "links":[]}

        actorpage = self._session.get(actor_url)
        soup = BeautifulSoup(actorpage.text, "html.parser")

        actor_element = soup.find("div", id="filmo-head-actor")
        if actor_element is None: actor_element = soup.find("div", id="filmo-head-actress") # women are listed as actresses

        actor_credits_element = actor_element.find_next_sibling("div") # finds all the productions acted in by the current actor
        in_production_tags = actor_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released

        if not in_production_tags: # actor has no upcoming projects :(
            return None

        for tag in in_production_tags:
            project_element = tag.find_parent("div")
            
            title = project_element.b.a.text
            link = project_element.b.a["href"]

            project_dict["titles"].append(title)
            project_dict["links"].append(f"{IMDB_URL}{link}")
        
        return project_dict

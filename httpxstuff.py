import asyncio
import httpx
import time

async def get_page(url, client):
    return await client.get(url)

async def get_stuff(urls):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [asyncio.create_task(get_page(url=url, client=client)) for url in urls]
        responses = await asyncio.gather(*tasks)
    return responses

from bs4 import BeautifulSoup
import json

def request_get_stuff(urls):
    with requests.Session() as session:
        responses = [session.get(url) for url in urls]
    return responses

import requests
def main():
    with open("data/url_log.json", "r") as f:
        json_data = json.load(f)
        director_urls = [json_data["Directors"][director] for director in json_data["Directors"]]
        directors = json_data["Directors"]
        # actor_urls = [json_data["Actors"][actor] for actor in json_data["Actors"]]
    
    start_dir = time.time()
    director_responses = asyncio.run(get_stuff(urls=director_urls))
    print(f"Time for directorpages using httpx: {round(time.time()-start_dir, 3)}")
    
    # start_dir2 = time.time()
    # director_responses2 = request_get_stuff(urls=director_urls)
    # print(f"Time for directorpages using requests: {round(time.time()-start_dir2, 3)}")

    for i, (director, director_page) in enumerate(zip(directors, director_responses)):
        soup = BeautifulSoup(director_page.text, "html.parser")
        try:
            director_element = soup.find("div", id="filmo-head-director")
            director_credits_element = director_element.find_next_sibling("div") # finds all the productions directed by the current director
            in_production_tags = director_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released
            print(f"Antall oppkommende produksjoner fra regissør nr {i+1} ({director}): {len(in_production_tags)}")
            with open(f"NOT weird {director}.html", "w") as f:
                f.write(director_page.text)
        except AttributeError:
            with open(f"Weird {director}.html", "w") as f:
                f.write(director_page.text)
            print("Bad httpx, bad...")

    # for i, (director, director_page) in enumerate(zip(directors, director_responses2)):
    #     soup = BeautifulSoup(director_page.text, "html.parser")
    #     try:
    #         director_element = soup.find("div", id="filmo-head-director")
    #         director_credits_element = director_element.find_next_sibling("div") # finds all the productions directed by the current director
    #         in_production_tags = director_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released
    #         print(f"Antall oppkommende produksjoner fra regissør nr {i+1} ({director}): {len(in_production_tags)}")
    #     except AttributeError:
    #         print(director_element)

    # start_act = time.time()
    # actor_responses = asyncio.run(get_stuff(urls=actor_urls))
    # print(f"Time for actor pages: {round(time.time()-start_act, 3)}")

    # for i, actor_page in enumerate(actor_responses):
    #     soup = BeautifulSoup(actor_page.text, "html.parser")

    #     actor_element = soup.find("div", id="filmo-head-actor")
    #     if actor_element is None: actor_element = soup.find("div", id="filmo-head-actress") # women are listed as actresses
    #     actor_credits_element = actor_element.find_next_sibling("div") # finds all the productions directed by the current actor
    #     in_production_tags = actor_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released
    #     print(f"Antall oppkommende produksjoner fra skuespiller nr {i}", len(in_production_tags))

main()

# r = requests.get("https://imdb.com/name/nm0716257/?ref_=fn_al_nm_0")

# r2 = httpx.get("https://imdb.com/name/nm0716257/?ref_=fn_al_nm_0", follow_redirects=True)

# print("Requests:\n", r.text)

# print("\n\nHttpx:\n", r2.text)

# soup = BeautifulSoup(r.text, "html.parser")
# dir_element = soup.find("div", id="filmo-head-director")
# print(dir_element)
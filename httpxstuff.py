import asyncio
import httpx


async def get_page(url, client):
    return await client.get(url)

async def get_stuff(urls):
    async with httpx.AsyncClient() as client:
        tasks = [asyncio.create_task(get_page(url=url, client=client)) for url in urls]
        responses = await asyncio.gather(*tasks)
    # results = [response for response in responses]
    return responses

from bs4 import BeautifulSoup
import json

def main():
    # director_urls = []
    # actor_urls = []
    with open("data/url_log.json", "r") as f:
        json_data = json.load(f)
        director_urls = [json_data["Directors"][director] for director in json_data["Directors"]]
        actor_urls = [json_data["Actors"][actor] for actor in json_data["Actors"]]
    director_responses = asyncio.run(get_stuff(urls=director_urls))
    actor_responses = asyncio.run(get_stuff(urls=actor_urls))

    for i, director_page in enumerate(director_responses):
        soup = BeautifulSoup(director_page.text, "html.parser")

        director_element = soup.find("div", id="filmo-head-director")
        director_credits_element = director_element.find_next_sibling("div") # finds all the productions directed by the current director
        in_production_tags = director_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released
        print(f"Antall oppkommende produksjoner fra regissør nr {i}", len(in_production_tags))

    for i, actor_page in enumerate(actor_responses):
        soup = BeautifulSoup(actor_page.text, "html.parser")

        actor_element = soup.find("div", id="filmo-head-actor")
        if actor_element is None: actor_element = soup.find("div", id="filmo-head-actress") # women are listed as actresses
        actor_credits_element = actor_element.find_next_sibling("div") # finds all the productions directed by the current actor
        in_production_tags = actor_credits_element.find_all("a", class_="in_production") # finds all productions that have not yet been released
        print(f"Antall oppkommende produksjoner fra skuespiller nr {i}", len(in_production_tags))
    # print(results[0])

main()
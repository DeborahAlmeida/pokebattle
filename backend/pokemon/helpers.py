from urllib.parse import urljoin
import requests
from django.conf import settings


def get_pokemon_from_api(poke_name):
    response = requests.get(urljoin(settings.POKE_API_URL, poke_name))
    data = response.json()

    info = {
        "defense": data["stats"][2]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "hp": data["stats"][0]["base_stat"],
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
        "pokemon_id": data["id"]
    }
    return info


def has_pokemon_on_api(poke_names):
    for pokemon_name in poke_names:
        response = requests.get(urljoin(settings.POKE_API_URL, pokemon_name))
        if response.status_code == 404:
            return False
    return True

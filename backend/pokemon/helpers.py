from urllib.parse import urljoin
import requests
from django.conf import settings


def get_pokemon_from_api(poke_id):
    response = requests.get(urljoin(settings.POKE_API_URL, str(poke_id)))
    data = response.json()

    info = {
        "defense": data["stats"][2]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "hp": data["stats"][0]["base_stat"],
        "name": data["name"],
        "img_url": data["sprites"]["front_default"],
    }
    return info

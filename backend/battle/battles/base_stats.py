from pokemon.helpers import get_pokemon_from_api
from battle.models import Team


def get_total_point_pokemon(data_pokemons):
    pokemon_first = get_pokemon_from_api(data_pokemons[0])
    pokemon_second = get_pokemon_from_api(data_pokemons[1])
    pokemon_third = get_pokemon_from_api(data_pokemons[2])
    all_pokemons_data = [
        pokemon_first,
        pokemon_second,
        pokemon_third
    ]
    info = sum_all_pokemons(all_pokemons_data)
    sum_pokemons_valid = sum_all_points(info)
    return sum_pokemons_valid


def sum_all_points(info):
    if (info[0] + info[1] + info[2]) <= 600:
        return True
    else:
        return False


def sum_all_pokemons(pokemons):
    pokemons_sum = []
    for pokemon in pokemons:
        base_stats = sumValid(pokemon)
        pokemons_sum.append(base_stats)
    return pokemons_sum


def sumValid(pokemon):
    sum_result = pokemon["attack"] + pokemon["defense"] + pokemon["hp"]
    return sum_result


def get_pokemons_team(battle, trainer):
    pokemons_team = {
        "pokemon_1": None,
        "pokemon_2": None,
        "pokemon_3": None,
    }
    team = Team.objects.prefetch_related('pokemons').filter(battle=battle, trainer=trainer)
    if team:
        pokemon_team = team[0].teams.all().order_by('order').prefetch_related('pokemon')
        pokemons_team["pokemon_1"] = pokemon_team[0].pokemon
        pokemons_team["pokemon_2"] = pokemon_team[1].pokemon
        pokemons_team["pokemon_3"] = pokemon_team[2].pokemon
        return pokemons_team
    else:
        return False

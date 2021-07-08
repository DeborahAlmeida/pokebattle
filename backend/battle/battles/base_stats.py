from pokemon.helpers import get_pokemon_from_api
from battle.models import PokemonTeam


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
    # pylint: disable=line-too-long
    pkn_teams = PokemonTeam.objects.filter(team__battle=battle,
                                           team__trainer=trainer).select_related('pokemon').order_by('order')
    # pylint: enable=line-too-long

    if pkn_teams:
        pokemons_team["pokemon_1"] = pkn_teams[0].pokemon
        pokemons_team["pokemon_2"] = pkn_teams[1].pokemon
        pokemons_team["pokemon_3"] = pkn_teams[2].pokemon
        return pokemons_team
    else:
        return False

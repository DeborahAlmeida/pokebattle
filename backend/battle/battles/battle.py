from ..models import Battle
from .rounds import roundRunning
from pokemon.helpers import get_pokemon_from_api


def battleRunning(poke_id, pokemons):
    battle_info = Battle.objects.get(id=poke_id)
    poke_info1_creator = get_pokemon_from_api(battle_info.pk1_creator)
    poke_info2_creator = get_pokemon_from_api(battle_info.pk2_creator)
    poke_info3_creator = get_pokemon_from_api(battle_info.pk3_creator)
    # poke_info_creator_list = [poke_info1_creator, poke_info2_creator, poke_info3_creator]
    poke_info1_opponent = get_pokemon_from_api(pokemons[0])
    poke_info2_opponent = get_pokemon_from_api(pokemons[1])
    poke_info3_opponent = get_pokemon_from_api(pokemons[2])

    round_one = [poke_info1_creator, poke_info1_opponent]
    round_two = [poke_info2_creator, poke_info2_opponent]
    round_three = [poke_info3_creator, poke_info3_opponent]

    winner = "nobody"
    opponent = 0
    creator = 0

    battle_rounds = [round_one, round_two, round_three]

    for battle_round in battle_rounds:
        result = roundRunning(battle_round)
        if result == "creator":
            creator = creator + 1
        else:
            opponent = opponent + 1

    if creator > opponent:
        winner = "creator"
    elif creator < opponent:
        winner = "opponent"
    else:
        winner = "creator"

    return winner


def message_error():
    message = "ERROR: PKNs you selected sum more than 600 points, please choose again"
    return message

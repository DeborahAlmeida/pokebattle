from .models import Battle
from .views import get_pokemon_from_api


def roundRunning(info):
    pokemon_creator = info[0]
    pokemon_opponent = info[1]
    winner = "nobody"
    opponent = 0
    creator = 0
    if (pokemon_creator["attack"] > pokemon_opponent["defense"]):
       
        creator = creator + 1
    if (pokemon_creator["attack"] == pokemon_opponent["defense"]):
        creator = creator + 1
        opponent = opponent + 1
    else:
        opponent = opponent + 1

    if (pokemon_opponent["attack"] > pokemon_creator["defense"]):
            opponent = opponent + 1
    if (pokemon_opponent["attack"] == pokemon_creator["defense"]):
        creator = creator + 1
        opponent = opponent + 1
    else:
        creator = creator + 1

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    elif (creator == opponent):
        if (pokemon_opponent["hp"] > pokemon_creator["hp"]):
            winner = "opponent"
            opponent = opponent + 1
        elif (pokemon_opponent["hp"] < pokemon_creator["hp"]):
            winner = "creator"
        else: 
            creator = creator + 1
            opponent = opponent + 1
    
    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    else:
        winner = "creator"

    return winner



def battleRunning(poke_id, pokemons):
    battle_info = Battle.objects.get(id=poke_id)
    poke_info1_creator = get_pokemon_from_api(battle_info.pk1_creator)
    poke_info2_creator = get_pokemon_from_api(battle_info.pk2_creator)
    poke_info3_creator = get_pokemon_from_api(battle_info.pk3_creator)
    poke_info_creator_list = [poke_info1_creator, poke_info2_creator, poke_info3_creator]
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

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    else:
        winner = "creator"

    return winner
        
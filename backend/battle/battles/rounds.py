def run_round(creator_pokemon, opponent_pokemon):
    winner = "nobody"
    result = get_points(creator_pokemon, opponent_pokemon)

    if (result["creator"] >= result["opponent"]):
        winner = "creator_won"
    else:
        winner = "opponent_won"

    return winner


def _run_attack(scoreboard, pokemon_creator, pokemon_opponent):
    if (pokemon_creator.attack > pokemon_opponent.defense):
        scoreboard["creator"] += 1
    elif (pokemon_creator.attack == pokemon_opponent.defense):
        scoreboard["creator"] += 1
        scoreboard["opponent"] += 1
    else:
        scoreboard["opponent"] += 1


def _run_defense(scoreboard, pokemon_creator, pokemon_opponent):
    if (pokemon_opponent.attack > pokemon_creator.defense):
        scoreboard["opponent"] += 1
    elif (pokemon_opponent.attack == pokemon_creator.defense):
        scoreboard["creator"] += 1
        scoreboard["opponent"] += 1
    else:
        scoreboard["creator"] += 1


def _run_hp(scoreboard, pokemon_creator, pokemon_opponent):
    if (pokemon_opponent.hp > pokemon_creator.hp):
        scoreboard["opponent"] += 1
    elif (pokemon_opponent.hp < pokemon_creator.hp):
        scoreboard["creator"] += 1
    else:
        scoreboard["creator"] += 1
        scoreboard["opponent"] += 1


def get_points(pokemon_creator, pokemon_opponent):
    scoreboard = {
        "creator": 0,
        "opponent": 0,
    }

    _run_attack(scoreboard, pokemon_creator, pokemon_opponent)
    _run_defense(scoreboard, pokemon_creator, pokemon_opponent)

    if (scoreboard["creator"] != scoreboard["opponent"]):
        return scoreboard
    else:
        _run_hp(scoreboard, pokemon_creator, pokemon_opponent)

    return scoreboard

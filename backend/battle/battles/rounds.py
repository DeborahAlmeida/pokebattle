def roundRunning(info):
    winner = "nobody"
    pokemon_creator = info[0]
    pokemon_opponent = info[1]

    result = runningBattle(pokemon_creator, pokemon_opponent)
    if (result["creator"] > result["opponent"]):
        winner = "creator"
    elif (result["creator"] < result["opponent"]):
        winner = "opponent"
    else:
        winner = "creator"
    return winner


def runningBattle(pokemon_creator, pokemon_opponent):
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
        creator = creator + 1
    elif (creator < opponent):
        opponent = opponent + 1
    elif (creator == opponent):
        if (pokemon_opponent["hp"] > pokemon_creator["hp"]):
            opponent = opponent + 1
        elif (pokemon_opponent["hp"] < pokemon_creator["hp"]):
            creator = creator + 1
        else:
            creator = creator + 1
            opponent = opponent + 1

    result = {
        "creator": creator,
        "opponent": opponent,
    }
    return result

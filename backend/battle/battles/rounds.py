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

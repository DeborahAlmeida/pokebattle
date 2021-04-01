def roundRunning(info):
    pokemon_creator = info[0]
    pokemon_opponent = info[1]
    winner = "nobody"
    opponent = 0
    creator = 0
    if (pokemon_creator["attack"] > pokemon_opponent["defense"] ):
       
        creator = creator + 1
        winnerRoundOne = "creator"
    if (pokemon_creator["attack"] == pokemon_opponent["defense"] ):
        creator = creator + 1
        opponent = opponent + 1
        winnerRoundOne = "nobody"
    else:
        winnerRoundOne = "opponent"
        opponent = opponent + 1

    if (pokemon_opponent["attack"] > pokemon_creator["defense"] ):
            winnerRoundTwo = "opponent"
            opponent = opponent + 1
    if (pokemon_opponent["attack"] == pokemon_creator["defense"] ):
        creator = creator + 1
        opponent = opponent + 1
        winnerRoundTwo = "nobody"
    else:
        winnerRoundTwo = "creator"
        creator = creator + 1

    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    elif (creator == opponent):
        if (pokemon_opponent["hp"] > pokemon_creator["hp"] ):
            winner = "opponent"
            opponent = opponent + 1
        elif (pokemon_opponent["hp"] < pokemon_creator["hp"] ):
            winner = "creator"
        else: 
            creator = creator + 1
            opponent = opponent + 1
            winnerRoundTwo = "nobody"
    
    if (creator > opponent):
        winner = "creator"
    elif (creator < opponent):
        winner = "opponent"
    else:
        winner = "creator"

    return winner



def battleRunning(poke_id, pokemons):
    battleInfo = Battle.objects.get(id = poke_id)
    pokeInfo1_creator = get_pokemon_from_api(battleInfo.pk1_creator)
    pokeInfo2_creator = get_pokemon_from_api(battleInfo.pk2_creator)
    pokeInfo3_creator = get_pokemon_from_api(battleInfo.pk3_creator)
    pokeInfoCreatorList = [pokeInfo1_creator, pokeInfo2_creator, pokeInfo3_creator]
    pokeInfo1_opponent = get_pokemon_from_api(pokemons[0])
    pokeInfo2_opponent = get_pokemon_from_api(pokemons[1])
    pokeInfo3_opponent = get_pokemon_from_api(pokemons[2])

    roundOne = [pokeInfo1_creator, pokeInfo1_opponent]
    roundTwo = [pokeInfo2_creator, pokeInfo2_opponent]
    roundThree = [pokeInfo3_creator, pokeInfo3_opponent]

    winner = "nobody"
    opponent = 0
    creator = 0

    battleRounds = [roundOne, roundTwo, roundThree ]

    for battleRound in battleRounds: 
        result = roundRunning(battleRound)
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
        
from battle.models import Battle
from battle.battles.rounds import roundRunning
from battle.models import PokemonTeam, Team

def battleRunning(team):
    battle_info = team.battle
    pokemon_team_opponent = PokemonTeam.objects.filter(team=team)
    team_creator = Team.objects.get(battle=battle_info, trainer=battle_info.creator)
    pokemon_team_creator = PokemonTeam.objects.filter(team=team_creator)
    winner = get_points(pokemon_team_opponent, pokemon_team_creator)
    return winner

def get_points(pokemons_creator, pokemons_opponent):
    battle_rounds = [
        [pokemons_creator[0].pokemon, pokemons_opponent[0].pokemon],
        [pokemons_creator[1].pokemon, pokemons_opponent[1].pokemon],
    ]
    winner = ""
    result = []
    for battle_round in battle_rounds:
        result_round = roundRunning(battle_round)
        result.append(result_round)
    if result[0] == result[1]:
        winner = result[0]
    else:
        result_draw = roundRunning([pokemons_creator[2].pokemon, pokemons_opponent[2].pokemon])
        winner = result_draw
    return winner


def validate_sum_pokemons(pokemons):
    total_points = 0
    for pokemon in pokemons:
        pokemon_point = pokemon.attack + pokemon.defense + pokemon.hp
        total_points += pokemon_point
    return total_points <= 600


def setWinner(winner, battle):
    if winner == 'creator':
        Battle.objects.filter(pk=battle.pk).update(winner=battle.creator)
    else:
        Battle.objects.filter(pk=battle.pk).update(winner=battle.opponent)

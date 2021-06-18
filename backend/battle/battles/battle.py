from battle.battles.rounds import run_round
from battle.battles.email import result_battle
from pokemon.models import Pokemon
from pokemon.helpers import get_pokemon_from_api


def run_battle(battle):
    teams = battle.teams.all()
    assert teams.count() == 2, "Unexpected error. Battle has more than two teams."
    team_winner = get_winner_for(teams[0], teams[1])
    return team_winner


def get_winner_for(team_creator, team_opponent):
    creator_pokemons = team_creator.pokemons.all()
    opponent_pokemons = team_opponent.pokemons.all()

    creator_won = 0
    opponent_won = 0
    for creator_pokemon, opponent_pokemon in zip(creator_pokemons, opponent_pokemons):
        winner_key = run_round(creator_pokemon, opponent_pokemon)
        if winner_key == "creator_won":
            creator_won += 1
        else:
            opponent_won += 1

    if creator_won > opponent_won:
        return team_creator

    return team_opponent


def validate_sum_pokemons(pokemons):
    pokemons_saved = []
    total_api_pokemon_point = 0
    pokemons_not_saved = []
    total_points = 0
    for pokemon in pokemons:
        on_database = verify_pokemon_exists_on_database(pokemon)
        if not on_database:
            pokemons_not_saved.append(pokemon)
            each_api_pokemon_point = sum_point_from_api(pokemon)
            total_api_pokemon_point += each_api_pokemon_point
        else:
            pokemons_saved.append(on_database)
    for pokemon in pokemons_saved:
        pokemon_point = sum_points_pokemon_on_database(pokemon)
        total_points += pokemon_point
    if total_api_pokemon_point:
        total_points += total_api_pokemon_point
    if total_points <= 600:
        for pokemon in pokemons_not_saved:
            create_pokemon_on_database(pokemon)
    return total_points <= 600


def verify_pokemon_exists_on_database(pokemon):
    on_database = Pokemon.objects.filter(pokemon_id=pokemon)
    return on_database


def sum_point_from_api(pokemon):
    data = get_pokemon_from_api(pokemon)
    return data['attack'] + data['defense'] + data['hp']


def sum_points_pokemon_on_database(pokemon):
    return pokemon[0].attack + pokemon[0].defense + pokemon[0].hp


def create_pokemon_on_database(pokemon):
    data_from_api_save = get_pokemon_from_api(pokemon)
    Pokemon.objects.create(pokemon_id=pokemon, name=data_from_api_save['name'],
                           attack=data_from_api_save['attack'],
                           defense=data_from_api_save['defense'],
                           hp=data_from_api_save['hp'])


def set_winner(winner, battle):
    battle.winner = winner
    battle.save()
    result_battle(battle)


def get_pokemon_object(pokemon_id):
    pokemon_object = Pokemon.objects.get(pokemon_id=pokemon_id)
    return pokemon_object

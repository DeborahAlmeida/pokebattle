from battle.battles.rounds import run_round
from battle.battles.email import result_battle
from pokemon.models import Pokemon
from pokemon.helpers import get_pokemon_from_api


def run_battle(battle):
    teams = list(battle.teams.all())
    assert len(teams) == 2, "Unexpected error. Battle has more than two teams."
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
    total_points = 0
    for pokemon in pokemons:
        total_points += sum_point_from_api(pokemon)
    return total_points <= 600


def verify_pokemon_is_saved(pokemons):
    for pokemon in pokemons:
        on_database = verify_pokemon_exists_on_database(pokemon)
        if not on_database:
            create_pokemon_on_database(pokemon)


def verify_pokemon_exists_on_database(pokemon):
    on_database = Pokemon.objects.filter(name=pokemon)
    return on_database


def sum_point_from_api(pokemon):
    data = get_pokemon_from_api(pokemon)
    return data['attack'] + data['defense'] + data['hp']


def sum_points_pokemon_on_database(pokemon):
    return pokemon[0].attack + pokemon[0].defense + pokemon[0].hp


def create_pokemon_on_database(pokemon):
    data_from_api_save = get_pokemon_from_api(pokemon)
    Pokemon.objects.create(pokemon_id=data_from_api_save['pokemon_id'], name=pokemon,
                           attack=data_from_api_save['attack'],
                           defense=data_from_api_save['defense'],
                           hp=data_from_api_save['hp'],
                           img_url=data_from_api_save['img_url'], )


def set_winner(winner, battle):
    battle.winner = winner
    battle.save()
    result_battle(battle)


def get_pokemon_object(pokemon_id):
    pokemon_object = Pokemon.objects.get(pokemon_id=pokemon_id)
    return pokemon_object

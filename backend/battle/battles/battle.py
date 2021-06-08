from battle.models import Battle
from battle.battles.rounds import run_round
from battle.models import PokemonTeam, Team
from battle.battles.email import result_battle


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
    total_points = 0
    for pokemon in pokemons:
        pokemon_point = pokemon.attack + pokemon.defense + pokemon.hp
        total_points += pokemon_point
    return total_points <= 600


def set_winner(winner, battle):
    battle.winner = winner
    battle.save()
    result_battle(battle)

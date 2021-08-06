from battle.battles.battle import validate_sum_pokemons, verify_pokemon_is_saved

from pokemon.helpers import verify_pokemon_exists_api


def verify_if_data_is_valid(data):
    message_error = None

    if 'battle' not in data:
        message_error = 'ERROR: Select a valid battle'
        return message_error

    if data['trainer'] not in (data['battle'].creator, data['battle'].opponent):
        message_error = ("ERROR: You do not have permission for this action.")
        return message_error

    if ('pokemon_1' or 'pokemon_2' or 'pokemon_3') not in data:
        message_error = 'ERROR: Select all pokemons'
        return message_error

    if ('position_pkn_1' or 'position_pkn_2' or 'position_pkn_3') not in data:
        message_error = 'ERROR: Select all positions'
        return message_error

    pokemons_exist = verify_pokemon_exists_api(
        [data['pokemon_1'], data['pokemon_2'], data['pokemon_3']])

    if not pokemons_exist:
        message_error = 'ERROR: Type the correct pokemons name'
        return message_error

    valid_pokemons = validate_sum_pokemons(
        [data['pokemon_1'], data['pokemon_2'], data['pokemon_3']])

    if not valid_pokemons:
        message_error = 'ERROR: Pokemons sum more than 600 points. Select again'
        return message_error

    if data['position_pkn_1'] in (data['position_pkn_2'], data['position_pkn_3']):
        message_error = 'ERROR: You cannot add the same position'
        return message_error

    if data['position_pkn_2'] == data['position_pkn_3']:
        message_error = 'ERROR: You cannot add the same position'
        return message_error

    verify_pokemon_is_saved(
            [
                data['pokemon_1'],
                data['pokemon_2'],
                data['pokemon_3']
            ]
        )
    return True

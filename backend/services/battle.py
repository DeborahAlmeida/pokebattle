from users.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from pokemon.helpers import verify_pokemon_exists_api

from battle.battles.email import send_invite_email
from battle.battles.battle import validate_sum_pokemons


def validate_if_creator_and_opponent_has_different_contenders(creator, opponent):
    if creator == opponent:
        return False
    return True


def fetch_opponent_or_create_if_doenst_exist(opponent_email):
    try:
        opponent = User.objects.get(email=opponent_email)
        opponent.is_guest = False
    except User.DoesNotExist:
        opponent = User.objects.create(email=opponent_email)
        opponent.is_guest = True
        random_password = get_random_string(length=64)
        opponent.set_password(random_password)
        opponent.save()
    return opponent


def send_invite_email_or_create_password_email(opponent, creator):
    if opponent.is_guest:
        invite_form = PasswordResetForm(data={"email": opponent.email})
        invite_form.is_valid()
        invite_form.save(
            domain_override=settings.HOST,
            subject_template_name='registration/guest_email_subject.txt',
            email_template_name='registration/guest_email.html',
            from_email=settings.FROM_EMAIL,)
    else:
        send_invite_email(opponent, creator)


def verify_pokemons_fields_has_missing_values(data):
    if ('pokemon_1' or 'pokemon_2' or 'pokemon_3') not in data:
        message_error = 'ERROR: Select all pokemons'
        return message_error
    return True


def verify_positions_fields_has_missing_values(data):
    if ('position_pkn_1' or 'position_pkn_2' or 'position_pkn_3') not in data:
        message_error = 'ERROR: Select all positions'
        return message_error
    return True


def verify_fields_has_wrong_pokemon_name(data):
    pokemons_exist = verify_pokemon_exists_api(
        [data['pokemon_1'], data['pokemon_2'], data['pokemon_3']])

    if not pokemons_exist:
        message_error = 'ERROR: Type the correct pokemons name'
        return message_error
    return True


def verify_pokemon_sum_is_valid(data):
    valid_pokemons = validate_sum_pokemons(
        [data['pokemon_1'], data['pokemon_2'], data['pokemon_3']])

    if not valid_pokemons:
        message_error = 'ERROR: Pokemons sum more than 600 points. Select again'
        return message_error
    return True


def verify_positions_fields_has_duplicate_values(data):
    positions = {
        int(data['position_pkn_1']),
        int(data['position_pkn_2']),
        int(data['position_pkn_3'])}
    if positions != {1, 2, 3}:
        message_error = 'ERROR: You cannot add the same position'
        return message_error
    return True

from users.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import PasswordResetForm
from battle.battles.email import send_invite_email
from django.conf import settings


def validate_if_creator_and_opponent_are_different(creator, opponent):
    if creator == opponent:
        return False
    return True


def validate_if_opponent_is_valid(opponent_email):
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


def create_battle(self, opponent, creator):
    if opponent.is_guest:
        invite_form = PasswordResetForm(data={"email": opponent.email})
        invite_form.is_valid()
        invite_form.save(
            self, subject_template_name='registration/guest_email_subject.txt',
            email_template_name='registration/guest_email.html',
            from_email=settings.FROM_EMAIL,)
    else:
        send_invite_email(opponent, creator)
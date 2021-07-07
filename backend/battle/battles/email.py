from templated_email import send_templated_mail
from django.conf import settings
from users.models import User


def result_battle(battle):
    send_templated_mail(
        template_name='results_battle',
        from_email=settings.FROM_EMAIL,
        recipient_list=[battle.creator, battle.opponent],
        context={
            'winner': battle.winner,
        },
    )


def send_invite_email(opponent, creator):
    user_on_database = User.objects.filter(email=opponent)
    opponent_email = None
    if not user_on_database:
        opponent_email = opponent
    else:
        opponent_email = user_on_database[0].email
    send_templated_mail(
        template_name='invite_challenge',
        from_email=settings.FROM_EMAIL,
        recipient_list=[opponent_email],
        context={
            'creator': creator.email,
        },
    )

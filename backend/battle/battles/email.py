from templated_email import send_templated_mail
from django.conf import settings


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
    send_templated_mail(
        template_name='invite_challenge',
        from_email=settings.FROM_EMAIL,
        recipient_list=[opponent.email],
        context={
            'creator': creator.email,
        },
    )

from templated_email import send_templated_mail
from django.conf import settings


def result_battle(battle):
    send_templated_mail(
        template_name='results_battle',
        from_email=settings.EMAIL,
        recipient_list=[battle.creator, battle.opponent],
        context={
            'winner': battle.winner,
        },
    )

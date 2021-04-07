import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from ..models import Battle
from templated_email import send_templated_mail


def result_battle():
    battle_info = Battle.objects.latest('id')
    if battle_info.winner == 'creator':
        winner = battle_info.creator
    else:
        winner = battle_info.opponent


    send_templated_mail(
        template_name='results_battle',
        from_email='deborahmendonca6@gmail.com',
        recipient_list=['deborah.mendonca@vinta.com.br'],
        context={
            'winner': winner,
            'full_name':'teste',
            'signup_date':'06/04/2021'
        },
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
        )
       
        
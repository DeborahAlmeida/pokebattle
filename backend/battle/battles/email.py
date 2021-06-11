from templated_email import send_templated_mail


def result_battle(battle):
    send_templated_mail(
        template_name='results_battle',
        from_email='deborahmendonca6@gmail.com',
        recipient_list=[battle.creator, battle.opponent],
        context={
            'winner': battle.winner,
        },
    )

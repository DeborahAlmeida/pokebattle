from celery.utils.log import get_task_logger

from battle.models import Battle
from battle.battles.battle import run_battle, set_winner

from pokebattle import celery_app

logger = get_task_logger(__name__)


@celery_app.task
def run_battle_and_send_result_email(battle_id):
    logger.info("About to solve Battle %d", battle_id)
    battle = Battle.objects.get(id=battle_id)
    team_winner = run_battle(battle)
    set_winner(team_winner.trainer, battle)
    logger.info("Solved Battle %d", battle_id)

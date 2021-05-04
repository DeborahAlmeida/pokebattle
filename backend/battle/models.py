from django.conf import settings
from django.db import models
from pokemon.models import Pokemon


class Battle(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="", related_name="creator_battles")
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="" , related_name="opponent_battles")
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="" , related_name="battle_win", null=True)

 
class Team(models.Model):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="teams")
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teams")
    pokemons = models.ManyToManyField(
        Pokemon, related_name="teams", through="PokemonTeam"
    )


class PokemonTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="teams")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="+")
    order = models.PositiveIntegerField()
    class Meta:
        ordering = ['order']
        unique_together = [('team', 'pokemon')]

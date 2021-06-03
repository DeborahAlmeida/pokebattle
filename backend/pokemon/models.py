# from django.conf import settings
from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    attack = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    hp = models.IntegerField(null=True)

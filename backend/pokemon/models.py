# from django.conf import settings
from django.db import models


class Pokemon(models.Model):
    pokemon_id = models.IntegerField()
    name = models.CharField(max_length=100, )
    attack = models.IntegerField()
    defense = models.IntegerField()
    hp = models.IntegerField()
    img_url = models.CharField(max_length=255, blank=True, )

from django.conf import settings
from django.db import models
from django.utils import timezone




from urllib.parse import urljoin

import requests
#from progress.bar import ChargingBar

class Gamer(models.Model):
    name = models.CharField(max_length=200)
    

    def publish(self):
        self.save()

    def __str__(self):
        return self.name



class Battle(models.Model):
    '''
    url = urljoin(settings.POKE_API_URL, "?limit=20")
    response = requests.get(url)
    data = response.json()
    POKEMONS = []
    for pokemon in data["results"]:
        POKEMONS.append((pokemon["name"],pokemon["name"]))
    '''
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+',  null=True)
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', null=True)
    pk1_creator = models.CharField(max_length=200, null=True)
    pk2_creator = models.CharField(max_length=200, null=True)
    pk3_creator = models.CharField(max_length=200,  null=True)
    pk1_opponent = models.CharField(max_length=200,  null=True)
    pk2_opponent = models.CharField(max_length=200,  null=True)
    pk3_opponent = models.CharField(max_length=200,  null=True)
    winner = models.CharField(max_length=200, null=True)
    def publish(self):
        self.save()


class Status(models.Model):
    #id = models.AutoField(primary_key=True)
    sequence = models.IntegerField()

    def publish(self):
        self.save()

class Round(models.Model):
    #status = models.ForeignKey(settings.STATUS_MODEL, on_delete=models.CASCADE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='winner_gamer_round', null=True)
    id_batalha = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='batalha_id', null=True)
    pk11 = models.CharField(max_length=200, verbose_name='Pokemon 1:', null=True)
    pk21 = models.CharField(max_length=200, verbose_name='Pokemon 2:', null=True)
    pk31 = models.CharField(max_length=200, verbose_name='Pokemon 3:', null=True)
    pk12 = models.CharField(max_length=200, verbose_name='Pokemon 1:', null=True)
    pk22 = models.CharField(max_length=200, verbose_name='Pokemon 2:', null=True)
    pk32 = models.CharField(max_length=200, verbose_name='Pokemon 3:', null=True)
    def publish(self):
        self.save()

 #status(1,2,3), vencedor, id_batalha, pk1-1, pk2-1, pk3-1, pk-1-2, pk-2-2, pk3-2


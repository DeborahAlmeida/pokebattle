from django.conf import settings
from django.db import models

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    attack = models.CharField(max_length=200, null=True)
    defense = models.CharField(max_length=200, null=True)
    hp = models.CharField(max_length=200, null=True)

    def publish(self):
        self.save()

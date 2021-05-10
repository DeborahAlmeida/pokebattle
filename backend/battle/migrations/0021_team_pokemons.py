# Generated by Django 3.2 on 2021-05-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '__first__'),
        ('battle', '0020_pokemonteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='pokemons',
            field=models.ManyToManyField(related_name='teams', through='battle.PokemonTeam', to='pokemon.Pokemon'),
        ),
    ]

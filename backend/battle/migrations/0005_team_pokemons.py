# Generated by Django 3.2 on 2021-04-30 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
        ('battle', '0004_pokemonteam'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='pokemons',
            field=models.ManyToManyField(related_name='teams', through='battle.PokemonTeam', to='pokemon.Pokemon'),
        ),
    ]

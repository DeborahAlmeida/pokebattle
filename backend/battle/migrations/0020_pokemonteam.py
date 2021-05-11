# Generated by Django 3.2 on 2021-05-04 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '__first__'),
        ('battle', '0019_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='PokemonTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='pokemon.pokemon')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='battle.team')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('team', 'pokemon')},
            },
        ),
    ]
# Generated by Django 3.2 on 2021-05-20 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonteam',
            name='order',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
# Generated by Django 3.2 on 2021-06-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0002_alter_pokemonteam_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonteam',
            name='order',
            field=models.PositiveIntegerField(default=False),
            preserve_default=False,
        ),
    ]
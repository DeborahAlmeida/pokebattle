# Generated by Django 2.2.19 on 2021-04-02 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0016_auto_20210326_1059'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Gamer',
        ),
        migrations.RemoveField(
            model_name='round',
            name='id_batalha',
        ),
        migrations.RemoveField(
            model_name='round',
            name='winner',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.DeleteModel(
            name='Round',
        ),
    ]
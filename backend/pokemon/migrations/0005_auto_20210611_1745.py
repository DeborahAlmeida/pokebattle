# Generated by Django 3.2 on 2021-06-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0004_auto_20210601_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='attack',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='defense',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='hp',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='name',
            field=models.CharField(default=False, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='pokemon_id',
            field=models.IntegerField(default=False),
            preserve_default=False,
        ),
    ]

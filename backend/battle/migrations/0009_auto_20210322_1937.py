# Generated by Django 2.2.19 on 2021-03-22 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0008_auto_20210322_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='player1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='What is your name?'),
        ),
        migrations.AlterField(
            model_name='battle',
            name='player2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Choose your opponent:'),
        ),
    ]

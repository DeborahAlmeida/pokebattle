# Generated by Django 3.2 on 2021-05-04 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('battle', '0017_auto_20210402_0037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='pk1_creator',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='pk1_opponent',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='pk2_creator',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='pk2_opponent',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='pk3_creator',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='pk3_opponent',
        ),
        migrations.AlterField(
            model_name='battle',
            name='creator',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='creator_battles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='battle',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='battle',
            name='opponent',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='opponent_battles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='battle',
            name='winner',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='battle_win', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 2.2.19 on 2021-03-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0009_auto_20210322_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
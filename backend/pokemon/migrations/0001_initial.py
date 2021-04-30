# Generated by Django 3.2 on 2021-04-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('attack', models.CharField(max_length=200, null=True)),
                ('defense', models.CharField(max_length=200, null=True)),
                ('hp', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]

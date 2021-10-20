# Generated by Django 3.2.7 on 2021-10-20 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_gameplayed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameplayed',
            name='pandl',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameplayed',
            name='status',
            field=models.CharField(default='loose', max_length=10),
        ),
        migrations.AlterField(
            model_name='games',
            name='starttime',
            field=models.TimeField(),
        ),
    ]

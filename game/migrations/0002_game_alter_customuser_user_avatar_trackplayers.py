# Generated by Django 4.0.4 on 2022-05-04 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=100)),
                ('creator', models.CharField(default='NULL', max_length=50)),
                ('number', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_avatar',
            field=models.ImageField(default='NULL', upload_to='user_avatars'),
        ),
        migrations.CreateModel(
            name='TrackPlayers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
    ]

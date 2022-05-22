# Generated by Django 4.0.4 on 2022-05-22 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_room_public_alter_customuser_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_avatar',
            field=models.ImageField(default='user_avatars/profimg/DEFAULT_10.png', upload_to='user_avatars'),
        ),
    ]
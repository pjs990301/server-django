# Generated by Django 4.0.6 on 2022-07-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_users_userid_alter_users_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='userId',
            field=models.CharField(default='userId', max_length=20),
        ),
        migrations.AlterField(
            model_name='users',
            name='userName',
            field=models.CharField(default='userName', max_length=10),
        ),
    ]

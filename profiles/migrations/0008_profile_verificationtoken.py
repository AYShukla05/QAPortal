# Generated by Django 4.0.1 on 2022-04-02 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_remove_profile_verificationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='verificationToken',
            field=models.UUIDField(default=222449),
        ),
    ]

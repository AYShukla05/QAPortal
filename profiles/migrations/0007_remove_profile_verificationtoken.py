# Generated by Django 4.0.1 on 2022-04-02 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_verificationtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verificationToken',
        ),
    ]
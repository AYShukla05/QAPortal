# Generated by Django 4.0.1 on 2022-03-23 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profileImage',
            field=models.ImageField(blank=True, default='images\\profileImages\\mehdi.png', null=True, upload_to='images/profileImages'),
        ),
    ]

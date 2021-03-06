# Generated by Django 4.0.1 on 2022-03-29 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='subscribeId',
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscribedUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscribedUser', to='profiles.profile'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='profiles.profile'),
        ),
    ]

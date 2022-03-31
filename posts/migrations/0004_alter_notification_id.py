# Generated by Django 4.0.1 on 2022-03-30 07:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_notification_isread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
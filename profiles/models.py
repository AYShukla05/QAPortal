from django.db import models

# Create your models here.


import uuid
from django.contrib.auth.models import User

from QAPortal.settings import BASE_DIR


# def upload_path(instance, filename):
#     return BASE_DIR.join(["ProfileImage", filename])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profileImage = models.ImageField(
        blank=True,
        null=True,
        upload_to="images/profileImages",
        default="images\profileImages\mehdi.png",
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    username = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=1000)

    def __str__(self):
        return self.username

    @property
    def getSubscribed(self):
        subscribed = self.subscription_set.all()
        return subscribed


class Subscription(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    subscribeId = models.CharField(max_length=500, null=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.owner.name

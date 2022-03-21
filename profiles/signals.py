from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings


from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=instance,
            username=user.username,
            name=user.username,
            password=user.password,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance.user
    user = profile
    if created == False:
        # user.name = profile.name
        user.username = profile.username
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


# post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

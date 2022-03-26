from rest_framework import serializers
from profiles.models import Profile, Subscription
from posts.models import Comment, Post, Notification
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class ProfileSerializer(serializers.ModelSerializer):
    profileImage = serializers.ImageField()

    class Meta:
        model = Profile
        fields = ['user', 'profileImage', 'username', 'name', 'email', 'id']


class PostSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = Comment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    post = PostSerializer(many=False)

    class Meta:
        model = Notification
        fields = "__all__"

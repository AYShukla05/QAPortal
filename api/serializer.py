from rest_framework import serializers
from profiles.models import  Profile, Subscription
from posts.models import Comment, Post, Notification
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#             required=True,
#             validators=[UniqueValidator(queryset=User.objects.all())]
#             )

#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         # fields = ('username', 'password', 'password2', 'email', 'name')
#         fields = "__all__"
#         extra_kwargs = {
#             'name': {'required': True},
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs

#     def create(self, validated_data):
#         # user = User.objects.create(
#         #     username=validated_data['username'],
#         #     email=validated_data['email'],
#         #     name=validated_data['name'],
#         # )
#         print("Validated Data", validated_data)
#         user = User.objects.create()
#         user.set_password(validated_data['password'])
#         user.save()

#         return user




class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

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

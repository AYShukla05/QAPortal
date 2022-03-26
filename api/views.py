# Create your views here.
import datetime
from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from profiles.models import Profile, Subscription
from posts.models import Post, Comment, Vote, Notification
from .serializer import (
    CommentSerializer,
    NotificationSerializer,
    PostSerializer,
    ProfileSerializer,
    SubscriptionSerializer,
)

# from api import serializer


@csrf_exempt
@api_view(["POST"])
def createUser(request):
    data = request.data
    try:
        print("\n\n\nData", data)
        user = User.objects.create(username=data["username"], email=data["email"])
        password = data["password"]
        password1 = data["confirm-password"]
        if password == password1:
            user.set_password(data["password"])
        user.save()
        profile = Profile.objects.create(
            user=user,
            name=data["name"],
            username=user.username,
            email=user.email,
            password=user.password,
            profileImage=data["profileImage"],
        )
        if profile.profileImage == "":
            profile.profileImage = "images\profileImages\mehdi.png"
        profile.save()

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    except IntegrityError:
        raise ValidationError()


@api_view(["GET"])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getPost(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    commentserializer = CommentSerializer(comments, many=True)
    serializer = PostSerializer(post)
    response = {"Post": serializer.data, "Comments": commentserializer.data}
    return Response(response)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def createPost(request):
    post = Post.objects.create()
    data = request.data
    post.owner = request.user.profile
    post.title = data["title"]
    post.body = data["body"]
    post.save()

    serializer = PostSerializer(post)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["PUT"])
def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    data = request.data
    post.title = data["title"]
    post.body = data["body"]
    post.save()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.profile == post.owner:
        post.delete()
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addVote(request, pk):
    post = Post.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    vote, created = Vote.objects.get_or_create(
        owner=user,
        post=post,
    )

    vote.value = data["value"]
    vote.save()
    post.getVoteCount

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def addComment(request, pk):
    postObj = Post.objects.get(id=pk)
    data = request.data
    comment = Comment.objects.create(
        owner=request.user.profile, post=postObj, body=data["body"]
    )
    comment.save()
    today = datetime.datetime.now()
    date_time = today.strftime("%H:%M:%S, %m/%d/%Y ")
    notification = Notification.objects.create(
        owner=postObj.owner,
        post=postObj,
        messages=comment.owner.name
        + " commented on your "
        + postObj.title
        + " at "
        + date_time
        # + "on" + date.date()
    )
    notification.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getComments(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def editComment(request, pk):
    comment = Comment.objects.get(id=pk)
    data = request.data
    comment.body = data["body"]
    comment.save()
    serializer = CommentSerializer(comment, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def getProfile(request, pk):
    profile = Profile.objects.get(pk=pk)
    posts = Post.objects.filter(owner=profile)
    comments = Comment.objects.filter(owner=profile)
    profileserializer = ProfileSerializer(profile, many=False)
    postserializer = PostSerializer(posts, many=True)
    commentserializer = CommentSerializer(comments, many=True)
    response = {
        "Profile": profileserializer.data,
        "Posts": postserializer.data,
        "Comments": commentserializer.data,
    }
    return Response(response)


@api_view(["GET"])
def profile(request):
    profile = request.user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@csrf_exempt
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfile(request, pk):
    data = request.data

    if request.user.check_password(data["password"]):
        profile = Profile.objects.get(id=pk)
        if request.user.profile == profile:
            profile.name = data["name"]
            profile.username = data["username"]
            profile.email = data["email"]
            profile.profileImage = data["profileImage"]
            if profile.profileImage == "":
                profile.profileImage = "images\profileImages\mehdi.png"

            profile.save()
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def changePassword(request):
    user = request.user
    profile = user.profile
    data = request.data
    if request.user.check_password(data["password"]):
        user.set_password(data["newPassword"])
        user.save()

    profile = request.user.profile
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.user.profile == profile:
        profile.delete()
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getMyProfile(request):
    try:
        profile = request.user.profile
        posts = Post.objects.filter(owner=profile)
        comments = Comment.objects.filter(owner=profile)
        profileserializer = ProfileSerializer(profile, many=False)
        postserializer = PostSerializer(posts, many=True)
        commentserializer = CommentSerializer(comments, many=True)
        response = {
            "Profile": profileserializer.data,
            "Posts": postserializer.data,
            "Comments": commentserializer.data,
        }
        return Response(response)
    except Exception as e:
        raise Exception(e)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def subscribe(request):
    id = request.data["id"]
    subscription, created = Subscription.objects.get_or_create(
        owner=request.user.profile,
        subscribeId=id,
    )
    if created:
        subscription.save()
    else:
        subscription.delete()
    serializer = SubscriptionSerializer(subscription, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getSubscribed(request):
    profile = request.user.profile
    subscriptions = Subscription.objects.filter(owner=profile)
    profiles = []
    for subscription in subscriptions:
        profile = Profile.objects.filter(id=subscription.subscribeId)
        if profile:
            profiles.append(profile[0])
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def getNotifications(request):
    profile = request.user.profile
    notifications = Notification.objects.filter(owner=profile)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

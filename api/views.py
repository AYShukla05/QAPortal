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
    # RegisterSerializer,
    SubscriptionSerializer,
)
# from api import serializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer
# @permission_classes([AllowAny])
@csrf_exempt
@api_view(["POST"])
def createUser(request):
    data = request.data
    print(data)
    try:
        print("\n\n\n\nData\n\n\n\n", data)
        user = User.objects.create()
        # user.name = data["name"]
        user.username = data["username"]
        user.email = data["email"]
        password = data["password"]
        password1 = data["password1"]
        if password == password1:
            user.set_password(data["password"])
        user.save()
        profile = Profile.objects.create(
            user=user,
            name=data["name"],
            username=user.username,
            email=user.email,
            profile_image=data['profileImage'],
            password=user.password,
        )
        profile.save()
        print("Id", user.id)
        print("Username", user.username)
        # print("Name", user.name)
        print("Email", user.email)
        print("Password", user.password)

        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    except:
        raise ValidationError()


@api_view(["GET"])
# @permission_classes([IsAuthenticated,AllowAny])
# @permission_classes([AllowAny])
def getPosts(request):
    print("Request Header", request.headers)
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
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
    # post.owner = Profile.objects.get(id="314f8a33-2afd-40d5-bb33-2f755b8009c2")
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
    print("Request")
    print(request, ".......", pk)
    post = Post.objects.get(id=pk)
    user = request.user.profile
    # user = Profile.objects.get(id="871e8510-903c-4c5c-9d6b-5f16d735ea16")
    data = request.data
    print("Data")
    print(data)
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
    print(request)
    postObj = Post.objects.get(id=pk)
    data = request.data
    print(data)
    comment = Comment.objects.create()
    comment.owner = request.user.profile
    comment.post = postObj
    comment.body = data["body"]
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
# @permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
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
    profile = Profile.objects.get(id=pk)
    if request.user.profile == profile:
        data = request.data
        profile.name = data["name"]
        profile.username = data["username"]
        profile.email = data["email"]
        profile.password = data["password"]
        profile.password1 = data["password1"]
        profile.save()
        user = profile.user
        user.set_password(profile.password)
        user.save()
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.user.profile == profile:
        profile.delete()
    return Response()


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
        # print(response)
        return Response(response)
    except Exception as e:
        raise APIException(e)


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
